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
    if len(report_text.strip().split()) < 1:
        return "⚠️ Please enter a full radiology report. This input is too short for meaningful summarization."

    result = summarizer(
        report_text.strip(),
        max_length=150,
        min_length=30,
        do_sample=False
    )
    return result[0]["summary_text"]
