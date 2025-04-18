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
    word_count = len(report_text.strip().split())
    max_len = min(150, word_count + 20)

    result = summarizer(
        report_text.strip(),
        max_length=max_len,
        min_length=min(30, word_count),
        do_sample=False
    )
    return result[0]["summary_text"]

