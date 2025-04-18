# 🧠 TumorAI: Brain Tumor Segmentation & Reporting System

TumorAI is a streamlined, showcase-ready diagnostic tool that performs tumor segmentation on brain MRI slices using deep learning. It visualizes tumor structures, generates clinical-style reports, and sends automatic alerts to professional channels such as Slack. This project was designed and implemented for the Vanderbilt AI Showcase with emphasis on innovation, automation, and medical impact.

---

## 🎯 Niche Problem

Brain tumors are time-sensitive conditions that often require radiologists and neurosurgeons to manually inspect MRI scans, segment abnormal regions, and document observations. This process can:

- Be **labor-intensive** and prone to human error
- Delay **treatment planning** in resource-limited settings
- Require specialist interpretation, which may not be locally available

TumorAI addresses these challenges by providing an **AI-first assistant** that automatically:

- Segments key tumor regions (Edema, Enhancing Tumor, Necrotic Core)
- Overlays color-coded results for clarity
- Calculates confidence scores
- Outputs a **professionally styled PDF report**
- Sends alert messages to clinical channels (e.g. Slack)
- Uses **Google Gemini** to generate both a brief summary and a full clinical write-up

---

## 🧠 Model Training & Technology Stack

TumorAI's segmentation model is built on a U-Net architecture, a convolutional neural network designed for biomedical image segmentation. Here's how it works:

### 🔍 U-Net Overview:
- **Encoder**: captures spatial features using convolution + pooling
- **Bottleneck**: compresses representation (abstract tumor signal)
- **Decoder**: reconstructs segmentation masks with upsampling + skip connections

### ⚙️ Technical Details:
- Framework: TensorFlow (Keras API)
- Image size: 128×128 grayscale slices (4-channel stacked)
- Optimizer: Adam
- Loss: Categorical cross-entropy
- Postprocessing: Argmax and confidence map extraction

### 📊 Training Dataset:
- [BraTS 2020](https://www.med.upenn.edu/sbia/brats2020/data.html)
- Multimodal MRI scans (T1, T2, FLAIR)
- Ground truth segmentations for 3 tumor types:
  - Edema (1)
  - Enhancing Tumor (2)
  - Necrotic Core (3)

![U-Net Architecture](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*QHGSWRuU8jR1GTR2j3V7YA.png)

> The U-Net model is effective for medical image segmentation due to its ability to preserve fine-grained localization using skip connections.

---

## 🖥️ Features

### ✅ Upload & Analyze
- Upload any MRI slice (JPG/PNG)
- See segmentation overlaid on the original scan
- Confidence level shown in the UI

### ✅ Report Generation
- Add optional clinical guideline notes
- Gemini automatically creates:
  - A brief **Model Summary** (short impression)
  - A **Full Clinical Report** (detailed factual write-up)
- PDF includes original image, overlay, summary, notes, and full write-up
- Download directly from the app

### ✅ Slack Automation
- Automatically notify clinical stakeholders with:
  - Tumor report status
  - Alerts when new scans are analyzed

---

## 🤖 Automation & Workflow Potential

TumorAI is not just a demo — it lays the foundation for real-world clinical workflows such as:

- **Automatic triaging**: Prioritize patients with likely tumors
- **Remote diagnostics**: Send reports to doctors via Slack, email, or EHR systems
- **Data audit pipelines**: Track scans and reports for documentation

Future integrations may include:
- Uploading to **Google Drive** or **FHIR-based hospital systems**
- Real-time analysis of DICOM datasets
- Integration with platforms like **Hugging Face Spaces** or **Render**

---

## 🛠️ Installation

```bash
# Clone the repo
https://github.com/zealair12/tumorai
cd tumorai

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run tumorai_app.py
```

---

## 🔒 Secrets Configuration
Create a `.env` file (not pushed to GitHub):

```
SLACK_WEBHOOK=https://hooks.slack.com/services/XXX/YYY/ZZZ
GEMINI_API_KEY=your-google-api-key-here
```

Or add to **Streamlit Secrets** if hosted on Streamlit Cloud:

```toml
SLACK_WEBHOOK = "https://hooks.slack.com/services/XXX/YYY/ZZZZ"
GEMINI_API_KEY = "your-google-api-key-here"
```

---

## 📎 Citations

- Menze BH, et al. "The Multimodal Brain Tumor Image Segmentation Benchmark (BRATS)." IEEE Transactions on Medical Imaging (2015).
- Ronneberger O, Fischer P, Brox T. "U-Net: Convolutional Networks for Biomedical Image Segmentation." MICCAI (2015).
- Kumar A. "Brain Tumor Segmentation using U-Net." GitHub Repository: https://github.com/abhi-kumar/Brain-Tumor-Segmentation-Unet

---

## 🧪 License & Ethics
> ⚠️ This tool is for **educational and demonstration purposes only**. It is not FDA-approved for clinical use. Any medical decisions should be made by licensed professionals.

---

## 💡 Creator
Built for the **Vanderbilt AI Showcase** by Zeal