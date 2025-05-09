import io
import sys
import os
import streamlit as st
from PIL import Image
import numpy as np
from segmentation import load_segmentation_model, segment_image
from report import create_pdf_report
from streamlit_option_menu import option_menu
from utils.notifications import send_slack_message
from dotenv import load_dotenv
from utils.gemini_dual_summary import generate_gemini_summaries

load_dotenv()
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")

st.set_page_config(page_title="TumorAI", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Courier New', monospace;
        background-color: #121212;
        color: #e0e0e0 !important;
    }
    h1, h2, h3, h4, h5, h6,
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stFileUploader label,
    .css-10trblm,
    .stMarkdown,
    .stAlert,
    .stDataFrame,
    .stCaption,
    .stDownloadButton,
    .stButton>button,
    .stInfo,
    .stSubheader {
        font-family: 'Courier New', monospace !important;
        color: #e0e0e0 !important;
    }
    .reportview-container .main .block-container{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stButton>button {
        animation: pulse 1.8s infinite;
        border-radius: 8px;
        font-weight: bold;
    }
    @keyframes pulse {
        0% {box-shadow: 0 0 0 0 rgba(0,255,100,0.7);}
        70% {box-shadow: 0 0 0 10px rgba(0,255,100, 0);}
        100% {box-shadow: 0 0 0 0 rgba(0,255,100, 0);}
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        menu_title="TumorAI Navigation",
        options=["Home", "Upload & Analyze", "Generate Report"],
        icons=["house", "cloud-upload", "file-earmark-text"],
        default_index=1,
        styles={
            "container": {"background-color": "#1c1c1c"},
            "icon": {"color": "#e0e0e0"},
            "nav-link": {"color": "#e0e0e0", "font-size": "16px", "font-family": "Courier New, monospace"},
            "nav-link-selected": {"background-color": "#4CAF50", "color": "#ffffff", "font-weight": "bold"}
        }
    )

if selected == "Home":
    st.title("🧠 TumorAI")
    st.markdown("""
    ## Welcome to TumorAI
    TumorAI is an intelligent assistant that performs tumor segmentation on brain MRI slices.
    Upload a scan, visualize detected regions, and generate a professional PDF report.

    ### 📱 Try it instantly
    Scan any of the QR codes below with your phone to launch the app and test it live:
    """)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("QR-Code.png", caption="Main App Access", use_column_width=True)
    with col2:
        st.image("QR-Code2.png", caption="Slack-integrated Link", use_column_width=True)
    with col3:
        st.image("QR-Code3.png", caption="Gemini Report Demo", use_column_width=True)
    col4, col5 = st.columns(2)
    with col4:
        st.image("QR-Code4.png", caption="Light Mode Entry", use_column_width=True)
    with col5:
        st.image("QR-Code5.png", caption="Alt Sample Access", use_column_width=True)

elif selected == "Upload & Analyze":
    uploaded = st.file_uploader("📄 Upload an MRI slice", type=["png", "jpg", "jpeg"])

    st.markdown("### Need a test image?")
    with st.expander("Use one of our sample MRI scans"):
        sample_col1, sample_col2 = st.columns(2)
        with sample_col1:
            if st.button("Load Sample Image 1"):
                with open("sample_images/example4.jpg", "rb") as f:
                    uploaded = io.BytesIO(f.read())

        with sample_col2:
            if st.button("Load Sample Image 2"):
                with open("sample_images/example3.jpg", "rb") as f:
                    uploaded = io.BytesIO(f.read())


    if not uploaded:
        st.info("👆 Upload or select an MRI slice to begin analysis")
        st.stop()

    if uploaded:
        img = Image.open(uploaded) if isinstance(uploaded, str) else Image.open(uploaded)
        st.image(img, caption="Input MRI Slice", use_container_width=True)

        try:
            seg_model = load_segmentation_model()
        except Exception as e:
            st.error("❌ Failed to load segmentation model.")
            st.stop()

        try:
            preds = seg_model.predict(np.expand_dims(np.stack([np.array(img.resize((128, 128)).convert("L")) / 255.0] * 4, axis=-1), axis=0))
            mask = np.argmax(preds[0], axis=-1).astype(np.uint8)
            confidence_map = np.max(preds[0], axis=-1)
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
            st.success(f"🔍 Tumor structures detected: {', '.join(found_labels)}")
        else:
            st.info("✅ No tumor structures detected.")

        try:
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

            avg_confidence = np.mean(confidence_map[mask > 0]) * 100 if np.any(mask > 0) else 0
            st.image(mask_overlay, caption=f"Segmentation Overlay (Confidence: {avg_confidence:.2f}%)", use_container_width=True)

            st.session_state.overlay = mask_overlay
            st.session_state.image = img
            st.session_state.found_labels = found_labels
            st.session_state.avg_confidence = avg_confidence
        except Exception as e:
            st.error("❌ Failed to create color-coded overlay.")


elif selected == "Generate Report":
    st.subheader("📄 Generate Report")

    if "image" not in st.session_state or "overlay" not in st.session_state:
        st.warning("Please upload and analyze an image first in the 'Upload & Analyze' tab.")
        st.stop()

    guideline_input = st.text_area("Add clinical guideline notes (optional)")

    if st.button("📄 Generate PDF Report"):
        out_pdf = "TumorAI_Report.pdf"
        try:
            with st.spinner("Generating clinical summary with Gemini..."):
                summary_text, report_text = generate_gemini_summaries(
                    st.session_state.get("found_labels", []),
                    st.session_state.get("avg_confidence", 0)
                )

            create_pdf_report(
                st.session_state.get("image"),
                st.session_state.get("overlay"),
                summary_text,
                guideline_input,
                report_text,
                out_pdf
            )

            with open(out_pdf, "rb") as file:
                st.download_button("⬇️ Download Report PDF", data=file, file_name=out_pdf, mime="application/pdf")

            slack_message = "🧠 TumorAI has successfully generated a tumor segmentation report for review."
            slack_success = send_slack_message(SLACK_WEBHOOK, slack_message)
            if slack_success:
                st.success("Slack alert sent.")
            else:
                st.warning("Slack alert failed.")

        except Exception as e:
            st.error("❌ Failed to generate PDF report.")
            st.exception(e)
