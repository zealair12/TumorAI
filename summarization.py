# summarization.py
from transformers import pipeline

def get_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")

from transformers import pipeline
import streamlit as st

@st.cache_resource
def get_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_report(summarizer, report_text):
    # Guardrail prompt
    prompt = (
        "Summarize this radiology report in a concise, medically accurate way. "
        "Focus on key findings and avoid general or irrelevant anatomical details.\n\n"
        f"Report:\n{report_text.strip()}"
    )
    
    if len(report_text.strip().split()) < 15:
        return "⚠️ Please enter a full radiology report. This input is too short for meaningful summarization."

    result = summarizer(prompt, max_length=150, min_length=30, do_sample=False)
    return result[0]["summary_text"]
