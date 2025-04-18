from transformers import pipeline
import streamlit as st
import torch

@st.cache_resource
def get_summarizer():
    return pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6",
        framework="pt",  # Force PyTorch
        device=0 if torch.cuda.is_available() else -1
    )

def summarize_report(summarizer, report_text):
    prompt = (
        "Summarize this radiology report in a concise, medically accurate way. "
        "Focus on key findings and avoid general or irrelevant anatomical details.\n\n"
        f"Report:\n{report_text.strip()}"
    )

    if len(report_text.strip().split()) < 15:
        return "⚠️ Please enter a full radiology report. This input is too short for meaningful summarization."

    result = summarizer(prompt, max_length=150, min_length=30, do_sample=False)
    return result[0]["summary_text"]
