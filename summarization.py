import streamlit as st
from transformers import pipeline

@st.cache_resource

def get_summarizer():
    try:
        return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    except Exception as e:
        st.warning("⚠️ Summarizer model failed to load. Using offline fallback.")
        return lambda text, max_length=150, min_length=30, do_sample=False: [{"summary_text": "Summarizer unavailable. Please download the report and summarize manually."}]

def summarize_report(summarizer, report_text):
    word_count = len(report_text.strip().split())
    if word_count < 15:
        st.warning("⚠️ Your input might be too short for a meaningful summary.")

    result = summarizer(
        report_text.strip(),
        max_length=150,
        min_length=30,
        do_sample=False
    )
    return result[0]["summary_text"]
