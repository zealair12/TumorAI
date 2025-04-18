from pptx import Presentation
from pptx.util import Inches
from PIL import Image
import io

def create_pdf_report(img, overlay, summary, guideline, full_report_text, output_path):
    prs = Presentation()
    slide_layout = prs.slide_layouts[5]  # blank layout
    slide = prs.slides.add_slide(slide_layout)

    # Add title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(8), Inches(0.5))
    title_frame = title_box.text_frame
    title_frame.text = "🧠 TumorBoard AI Report"

    # Add original image
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    slide.shapes.add_picture(img_byte_arr, Inches(0.5), Inches(1), height=Inches(2.5))

    # Add overlay image
    overlay_byte_arr = io.BytesIO()
    overlay.save(overlay_byte_arr, format='PNG')
    overlay_byte_arr.seek(0)
    slide.shapes.add_picture(overlay_byte_arr, Inches(5), Inches(1), height=Inches(2.5))

    # Add text content
    body_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.7), Inches(9), Inches(3.5))
    body = body_box.text_frame

    body.add_paragraph("Full Clinical Report")
    body.add_paragraph(full_report_text)

    body.add_paragraph("AI-Generated Summary")
    body.add_paragraph(summary)

    body.add_paragraph("Guideline Recommendation")
    body.add_paragraph(guideline)

    # Save to output
    prs.save(output_path)