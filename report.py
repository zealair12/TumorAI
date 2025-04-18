from docx import Document
from docx.shared import Inches
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import tempfile
from PIL import Image
import os

def create_pdf_report(image, mask, summary, guideline, full_report_text, out_path):
    c = canvas.Canvas(out_path, pagesize=letter)
    width, height = letter
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "🧠 TumorAI Report")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(50, y, "📅 Generated via TumorAI")
    y -= 40

    # Save both images to temp files
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_input:
        image.save(tmp_input.name)
        input_path = tmp_input.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_mask:
        mask.save(tmp_mask.name)
        mask_path = tmp_mask.name

    # Add uploaded image
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Uploaded MRI Slice")
    y -= 10
    c.drawImage(ImageReader(input_path), 50, y - 220, width=300, height=220, preserveAspectRatio=True)
    y -= 240

    # Add segmentation mask image
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Segmentation Overlay")
    y -= 10
    c.drawImage(ImageReader(mask_path), 50, y - 220, width=300, height=220, preserveAspectRatio=True)
    y -= 240

    # Add summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Model Summary")
    y -= 20
    text_obj = c.beginText(50, y)
    text_obj.setFont("Helvetica", 12)
    for line in summary.split("\n"):
        text_obj.textLine(line)
    c.drawText(text_obj)
    y = text_obj.getY() - 20

    # Add guideline
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "🧾 Clinical Guideline")
    y -= 20
    text_obj = c.beginText(50, y)
    text_obj.setFont("Helvetica", 12)
    for line in guideline.split("\n"):
        text_obj.textLine(line)
    c.drawText(text_obj)
    y = text_obj.getY() - 20

    # Add full report
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "📝 Full Clinical Report")
    y -= 20
    text_obj = c.beginText(50, y)
    text_obj.setFont("Helvetica", 12)
    for line in full_report_text.split("\n"):
        text_obj.textLine(line)
    c.drawText(text_obj)

    c.save()

    # Cleanup temp files
    os.remove(mask_path)
    os.remove(input_path)