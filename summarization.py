# summarization.py
from transformers import pipeline

def get_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")

def summarize_report(summarizer, text):
    prompt = (
        "Summarize this radiology report in a concise, medically accurate way. "
        "Focus on key findings and avoid general or irrelevant anatomical details:\n\n"
    )
    input_text = prompt + text
    input_len = len(text.split())
    max_len = max(50, int(input_len * 1.2))
    min_len = max(20, int(input_len * 0.5))

    result = summarizer(
        input_text,
        max_length=max_len,
        min_length=min_len,
        do_sample=False
    )
    return result[0]["summary_text"]

