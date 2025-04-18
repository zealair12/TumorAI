🧠 TumorAI: Brain Tumor Segmentation & Reporting Assistant

TumorAI is a streamlined, showcase-ready diagnostic tool that performs tumor segmentation on brain MRI slices using deep learning. It visualizes tumor structures, generates clinical-style reports, and sends automatic alerts to professional channels such as Slack. This project was designed and implemented for the Vanderbilt AI Showcase with emphasis on innovation, automation, and medical impact.

🎯 Niche Problem

Brain tumors are time-sensitive conditions that often require radiologists and neurosurgeons to manually inspect MRI scans, segment abnormal regions, and document observations. This process can:

Be labor-intensive and prone to human error

Delay treatment planning in resource-limited settings

Require specialist interpretation, which may not be locally available

TumorAI addresses these challenges by providing an AI that automatically:

Segments key tumor regions (Edema, Enhancing Tumor, Necrotic Core)

Overlays color-coded results for clarity

Calculates confidence scores

Outputs a professionally styled PDF report

Sends alert messages to clinical channels (e.g. Slack)

This tool is a prototype of how medical workflows can be automated and accelerated, especially in under-resourced clinics or global health contexts.

🧠 Model Training

The segmentation model was based on a pre-trained U-Net-style architecture optimized for brain tumor segmentation using the BraTS (Brain Tumor Segmentation) 2020 dataset. Key features:

Input: T1-weighted or T2-weighted axial brain MRI slice

Output: Multiclass pixel mask with 3 classes

Architecture: U-Net with batch normalization and dropout regularization

Training source: Adapted from publicly available TensorFlow-based models, specifically this repo

Labels:

1: Edema (yellow)

2: Enhancing Tumor (red)

3: Necrotic Core (blue)

Model predictions are post-processed using color-coded overlays and confidence maps. This approach was chosen to mimic how a human radiologist might annotate tumors in a clinical setting.

🖥️ Features

✅ Upload & Analyze

Upload any MRI slice (JPG/PNG)

See segmentation overlaid on the original scan

Confidence level shown in the UI

✅ Report Generation

Add optional clinical guideline notes

Generate a professional PDF report with diagnosis overlay

Download directly from the app

✅ Slack Automation

Automatically notify clinical stakeholders with:

Tumor report summary

Alerts when new scans are analyzed

🤖 Automation & Workflow Potential

With TumorAI, I am attempting to lay the foundation for real-world clinical workflows such as:

Automatic triaging: Prioritize patients with likely tumors

Remote diagnostics: Send reports to doctors via Slack, email, or EHR systems

Data audit pipelines: Track scans and reports for documentation

Future integrations may include:

Uploading to Google Drive or FHIR-based hospital systems

Real-time analysis of DICOM datasets

Integration with platforms like Hugging Face Spaces or Render

🛠️ Installation

# Clone the repo
https://github.com/zealair12/tumorai
cd tumorai

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run tumorai_app.py

🔒 Secrets Configuration

Create a .env file (not pushed to GitHub):

SLACK_WEBHOOK=https://hooks.slack.com/services/XXX/YYY/ZZZ

Or add to Streamlit Secrets if hosted on Streamlit Cloud:

SLACK_WEBHOOK = "https://hooks.slack.com/services/XXX/YYY/ZZZ"

📎 Citations

Menze BH, et al. "The Multimodal Brain Tumor Image Segmentation Benchmark (BRATS)." IEEE Transactions on Medical Imaging (2015).

Ronneberger O, Fischer P, Brox T. "U-Net: Convolutional Networks for Biomedical Image Segmentation." MICCAI (2015).

Kumar A. "Brain Tumor Segmentation using U-Net." GitHub Repository: https://github.com/abhi-kumar/Brain-Tumor-Segmentation-Unet

🧪 License & Ethics

⚠️ This tool is for educational and demonstration purposes only. It is not FDA-approved for clinical use. Any medical decisions should be made by licensed professionals.

💡 Creator

Built for the Vanderbilt AI Showcase by Zeal.

