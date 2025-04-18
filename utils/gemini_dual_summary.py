import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_gemini_summaries(labels, confidence):
    if not GEMINI_API_KEY:
        return ("Gemini API key not found.", "Gemini API key not found.")

    label_str = ", ".join(labels) if labels else "None"
    base_prompt = (
        f"A brain MRI scan was analyzed using an AI model. The detected tumor types were: {label_str}. "
        f"The average confidence of the model was {confidence:.2f}%."
    )

    summary_prompt = (
        base_prompt + "\n\nWrite a brief and professional summary of these findings, suitable as a short impression in a diagnostic report."
    )

    report_prompt = (
        base_prompt + "\n\nWrite a formal clinical report paragraph for a radiologist. Be concise, avoid speculative conclusions, and stay factual."
    )

    def query_gemini(prompt):
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            response = requests.post(f"{url}?key={GEMINI_API_KEY}", headers=headers, data=json.dumps(payload))
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text'].strip()
        except Exception as e:
            return "❌ Summary generation failed."

    summary = query_gemini(summary_prompt)
    report = query_gemini(report_prompt)
    return summary, report
