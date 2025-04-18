from docx import Document
from docx.shared import Inches
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import tempfile
from PIL import Image
import os

def wrap_text(text, max_width):
    import textwrap
    lines = text.split("\n")
    wrapped = []
    for line in lines:
        wrapped.extend(textwrap.wrap(line, width=max_width))
    return wrapped

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

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_input:
        image.save(tmp_input.name)
        input_path = tmp_input.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_mask:
        mask.save(tmp_mask.name)
        mask_path = tmp_mask.name

    # Uploaded Image
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Uploaded MRI Slice")
    y -= 10
    c.drawImage(ImageReader(input_path), 50, y - 220, width=300, height=220, preserveAspectRatio=True)
    y -= 240

    # Mask Overlay
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Segmentation Overlay")
    y -= 10
    c.drawImage(ImageReader(mask_path), 50, y - 220, width=300, height=220, preserveAspectRatio=True)
    y -= 240

    # Summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Model Summary")
    y -= 20
    text_obj = c.beginText(50, y)
    text_obj.setFont("Helvetica", 12)
    for line in wrap_text(summary, 90):
        text_obj.textLine(line)
    c.drawText(text_obj)
    y = text_obj.getY() - 20

    # Guideline
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "🧾 Clinical Guideline")
    y -= 20
    text_obj = c.beginText(50, y)
    text_obj.setFont("Helvetica", 12)
    for line in wrap_text(guideline, 90):
        text_obj.textLine(line)
    c.drawText(text_obj)
    y = text_obj.getY() - 20

    # Full Report
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "📝 Full Clinical Report")
    y -= 20
    text_obj = c.beginText(50, y)
    text_obj.setFont("Helvetica", 12)
    for line in wrap_text(full_report_text, 90):
        text_obj.textLine(line)
    c.drawText(text_obj)

    c.save()
    os.remove(mask_path)
    os.remove(input_path)