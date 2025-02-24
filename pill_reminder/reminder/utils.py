import cv2
import easyocr
import re
from google.generativeai import GenerativeModel
import google.generativeai as genai
import os

def preprocess_image(image_path):
    """Enhance image quality for OCR."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.GaussianBlur(image, (5, 5), 0)
    processed = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY, 11, 2)
    return processed

def extract_text_from_image(processed_image):
    """Extract text from preprocessed image using EasyOCR."""
    reader = easyocr.Reader(['en'])
    extracted_text = " ".join(reader.readtext(processed_image, detail=0, paragraph=True))
    return extracted_text

def clean_text(text):
    """Clean extracted text by removing special characters and extra spaces."""
    text = re.sub(r'[^A-Za-z0-9.,/\+\-\n ]+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def refine_text_with_gemini(text):
    """Refine extracted prescription text using Gemini AI."""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=GEMINI_API_KEY)

    prompt = f"""
    Here is an OCR-extracted medical prescription:

    RAW TEXT:
    {text}

    Your task:
    1. Correct spelling and formatting.
    2. Structure the prescription properly.
    3. Suggest appropriate medicine timings (e.g., morning, after meals, bedtime).

    Provide only the cleaned prescription.
    """
    model = GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text if response else "Error: Gemini API did not return a response."