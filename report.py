from docx import Document
from docx.shared import Inches
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
from PIL import Image
import os

def create_pdf_report(image, mask, summary, guideline, full_report_text, out_path):
    # Create a temporary canvas
    c = canvas.Canvas(out_path, pagesize=letter)
    width, height = letter
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Tumor Segmentation Report")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(50, y, "📅 Report Generated via TumorAI")
    y -= 40

    # Save segmentation mask to temp image
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        mask.save(tmp.name)
        mask_path = tmp.name

    # Add mask image to PDF
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Tumor Segmentation Mask")
    y -= 10
    c.drawImage(mask_path, 50, y - 300, width=400, preserveAspectRatio=True, mask='auto')
    y -= 320

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
    c.drawString(50, y, "🧾 Suggested Clinical Guideline")
    y -= 20
    text_obj = c.beginText(50, y)
    text_obj.setFont("Helvetica", 12)
    for line in guideline.split("\n"):
        text_obj.textLine(line)
    c.drawText(text_obj)
    y = text_obj.getY() - 20

    # Add full clinical report
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "📝 Full Clinical Report")
    y -= 20
    text_obj = c.beginText(50, y)
    text_obj.setFont("Helvetica", 12)
    for line in full_report_text.split("\n"):
        text_obj.textLine(line)
    c.drawText(text_obj)

    c.save()

    # Cleanup temp file
    os.remove(mask_path)