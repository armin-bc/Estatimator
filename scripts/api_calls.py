import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

import scripts.constants as const

# Load API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "API key not found. Please set 'GOOGLE_API_KEY' in your .env file."
    )

# Configuration
genai.configure(api_key=api_key)
model = genai.GenerativeModel(const.MODEL)


def call_gemini_with_retry(prompt: str, pmi_pdf_path=None, max_tokens=8192) -> str:
    if not prompt or not prompt.strip():
        raise ValueError("Prompt must not be empty!")
    content = [prompt]

    if pmi_pdf_path:
        pmi_pdf = genai.upload_file(path=pmi_pdf_path, display_name="PMI_PDF")
        content.append(pmi_pdf)

    for attempt in range(1, const.MAX_RETRIES + 1):
        try:
            print(f"Call AI (Attempt {attempt}/{const.MAX_RETRIES}) ...")

            response = model.generate_content(
                content,
                generation_config={
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": max_tokens,
                    "response_mime_type": "text/plain",
                },
            )
            return response.text

        except Exception as e:
            print(
                f"Error at AI call (Attempt {attempt}/{const.MAX_RETRIES}): {type(e).__name__}: {e}"
            )
            if attempt < const.MAX_RETRIES:
                time.sleep(const.RETRY_DELAY)
            else:
                raise


def generate_response(prompt: str, pmi_pdf_path=None) -> str:
    print("Request: Generating response...")
    raw_response = call_gemini_with_retry(prompt, pmi_pdf_path)
    with open("response.json", "w", encoding="utf-8") as f:
        f.write(raw_response)
    return raw_response
