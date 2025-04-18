import streamlit as st
from PIL import Image
import numpy as np
import os
from segmentation import load_segmentation_model, segment_image
from interpreter import interpret_mask
from summarization import get_summarizer, summarize_report
from report import create_pdf_report
from emailer import send_email

st.set_page_config(page_title="TumorAI", layout="centered")

st.title("🧠 TumorAI")

try:
    summarizer = get_summarizer()
except Exception as e:
    st.error("❌ Failed to load summarization model.")
    st.stop()

uploaded = st.file_uploader("📤 Upload an MRI slice", type=["png", "jpg", "jpeg"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Input MRI Slice", use_container_width=True)

    try:
        seg_model = load_segmentation_model()
    except Exception as e:
        st.error("❌ Failed to load segmentation model.")
        st.stop()

    try:
        mask = segment_image(seg_model, img)
    except Exception as e:
        st.error("❌ Error during segmentation. Please try another image.")
        st.stop()

    unique_vals = np.unique(mask)
    class_labels = {
        1: "Edema",
        2: "Enhancing Tumor",
        3: "Necrotic Core"
    }
    found_labels = [class_labels[c] for c in unique_vals if c in class_labels]
    if found_labels:
        st.write(f"🔍 Tumor classes detected: {', '.join(found_labels)}")
    else:
        st.write("✅ No tumor classes detected.")

    interpretation_text = interpret_mask(mask)
    st.markdown("**📝 Notes:**")
    st.write(interpretation_text)

    try:
        mask_color = Image.fromarray(mask.astype(np.uint8) * 85).convert("RGB").resize(img.size)
        img_rgb = img.convert("RGB")
        mask_overlay_np = (np.array(img_rgb) * 0.6 + np.array(mask_color) * 0.4).astype(np.uint8)
        mask_overlay = Image.fromarray(mask_overlay_np)
        st.image(mask_overlay, caption="Segmentation Overlay", use_container_width=True)
    except Exception as e:
        st.error("❌ Failed to create mask overlay.")

    st.markdown("---")
    st.subheader("📄 Generate Report")
    report_text = st.text_area("Paste the clinical report")
    guideline_input = st.text_area("Add clinical guideline notes (optional)")

    if report_text:
        try:
            summary = summarize_report(summarizer, report_text)
            st.markdown("**AI Summary:**")
            st.write(summary)
        except Exception as e:
            st.error("❌ Failed to generate summary.")

    if st.button("📄 Generate PDF Report"):
        out_pdf = "TumorAI_Report.pdf"
        try:
            create_pdf_report(img, mask_overlay, summary, guideline_input, report_text, out_pdf)
            with open(out_pdf, "rb") as file:
                st.download_button("⬇️ Download Report PDF", data=file, file_name=out_pdf, mime="application/pdf")
        except Exception as e:
            st.error("❌ Failed to generate PDF report.")

        st.markdown("---")
        recipient = st.text_input("📧 Enter recipient email")
        if st.button("📤 Send Report via Email"):
            if not recipient:
                st.warning("Please enter a recipient email address.")
            else:
                try:
                    send_email(recipient, "TumorAI Report", "Attached is the generated tumor segmentation report.", out_pdf)
                except Exception as e:
                    st.error("❌ Failed to send email. Please check credentials or recipient address.")