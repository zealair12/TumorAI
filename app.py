import streamlit as st
from PIL import Image
import numpy as np
import io
from segmentation import load_segmentation_model, segment_image
from summarization import get_summarizer, summarize_report
from report import create_pdf_report
from emailer import send_email
from interpreter import interpret_mask

st.title("TumorAI")

# Initialize components
seg_model = load_segmentation_model()
summarizer = get_summarizer()

def display_overlay(img, mask):
    from PIL import Image
    import numpy as np

    # Color mask from class labels
    class_colors = {0:(0,0,0), 1:(255,255,0), 2:(255,0,0), 3:(0,0,255)}
    h, w = mask.shape
    color_mask = np.zeros((h, w, 3), dtype=np.uint8)
    for cls, col in class_colors.items():
        color_mask[mask == cls] = col

    # Resize color mask to match original image size
    color_mask_resized = Image.fromarray(color_mask).resize(img.size, Image.NEAREST)

    # Blend images (convert both to RGBA)
    overlay = Image.blend(img.convert("RGBA"), color_mask_resized.convert("RGBA"), alpha=0.4)
    return overlay


# 1. Upload and segment
uploaded = st.file_uploader("1. Upload MRI slice (brain)", type=["png","jpg","jpeg","dcm"])
mask_overlay = None
mask = None
if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Input slice", use_container_width=True)

    # Get segmentation mask
    mask = segment_image(seg_model, img)

    # Check mask classes
    unique_vals = np.unique(mask)
    class_labels = {
        1: "Edema",
        2: "Enhancing Tumor",
        3: "Necrotic Core"
    }

    found_labels = [class_labels[c] for c in unique_vals if c in class_labels]
    if found_labels:
        st.write(f"Tumor classes detected in this slice: {', '.join(found_labels)}")
    else:
        st.write("✅ No tumor classes detected.")



    if any(c in unique_vals for c in [1,2,3]):
        st.success("✅ UNet segmentation appears to have run correctly.")
    else:
        st.error("⚠️ No tumor classes detected — check that your model loaded correctly!")
    
    interpretation_text = interpret_mask(mask)
    st.markdown("**Notes:**")
    st.write(interpretation_text)

    mask_overlay = display_overlay(img, mask)
    st.image(mask_overlay, caption="Segmentation Overlay", use_container_width=True)

# 2. Summarize report
report_text = st.text_area(
    "📝 Paste the clinical report to summarize",
    help="Paste any radiology or exam report. You can submit with Ctrl+Enter or tap the button below.")
summary = None
if report_text:
    summary = summarize_report(summarizer, report_text)
    st.markdown("**Summary:**")
    st.write(summary)

# 3. Guidelines
guidelines = {
    "Glioma": "Use Temozolomide and consider resection when feasible.",
    "Meningioma": "Monitor small tumors; surgical removal for symptomatic cases.",
    "Metastasis": "Whole-brain radiation therapy followed by targeted therapy."
}

guideline_input = st.text_area("Optional: Add your clinical guideline or recommendation notes")


# 4. Generate PDF & Email
if st.button("4. Generate PDF Report") and mask_overlay and summary:
    out_pdf = "report.pdf"
    create_pdf_report(img, mask_overlay, summary, guideline_input, report_text, out_pdf)

    with open(out_pdf, "rb") as f:
        st.download_button("Download PDF", data=f, file_name="TumorReport.pdf", mime="application/pdf")
    
    recipient = st.text_input("Recipient email for automatic send")
    if recipient and st.button("Send via Email"):
        send_email(
            sender="you@hospital.org",
            recipient=recipient,
            subject="TumorBoard Report",
            body="Please find attached the segmented MRI report.",
            attachment_path=out_pdf,
            smtp_server="smtp.hospital.org",
            smtp_port=465,
            username="you@hospital.org",
            password="YOUR_SMTP_PASSWORD"
        )
        st.success("Email sent!")