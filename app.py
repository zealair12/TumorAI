import streamlit as st
from PIL import Image
import numpy as np
import os
from segmentation import load_segmentation_model, segment_image
from report import create_pdf_report

st.set_page_config(page_title="TumorAI", layout="centered")

st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Georgia', serif;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 TumorAI")

uploaded = st.file_uploader("📤 Upload an MRI slice", type=["png", "jpg", "jpeg"])

if not uploaded:
    st.info("👆 Upload an MRI slice to begin analysis")
    st.stop()

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
        st.write(f"🔍 Tumor structures detected: {', '.join(found_labels)}")
    else:
        st.write("✅ No tumor structures detected.")

    try:
        # Color-coded mask overlay
        color_map = {
            1: (255, 255, 0),   # Yellow - Edema
            2: (255, 0, 0),     # Red - Enhancing Tumor
            3: (0, 0, 255)      # Blue - Necrotic Core
        }
        color_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
        for label, color in color_map.items():
            color_mask[mask == label] = color

        base_img = img.convert("RGB").resize(mask.shape[::-1])
        overlay_np = (np.array(base_img) * 0.6 + color_mask * 0.4).astype(np.uint8)
        mask_overlay = Image.fromarray(overlay_np)

        st.image(mask_overlay, caption="Segmentation Overlay", use_container_width=True)
    except Exception as e:
        st.error("❌ Failed to create color-coded overlay.")

    st.markdown("---")
    st.subheader("📄 Generate Report")
    guideline_input = st.text_area("Add clinical guideline notes (optional)")

    if st.button("📄 Generate PDF Report"):
        out_pdf = "TumorAI_Report.pdf"
        try:
            create_pdf_report(img, mask_overlay, "Tumor structures detected: " + ", ".join(found_labels), guideline_input, "N/A", out_pdf)
            with open(out_pdf, "rb") as file:
                st.download_button("⬇️ Download Report PDF", data=file, file_name=out_pdf, mime="application/pdf")
        except Exception as e:
            st.error("❌ Failed to generate PDF report.")