from celery import shared_task
from .utils import preprocess_image, extract_text_from_image, clean_text, refine_text_with_gemini
from pill_reminder.settings import supabase

@shared_task
def process_prescription(image_path, user_id):
    try:
        # Preprocess the image
        processed_image = preprocess_image(image_path)

        # Extract text using OCR
        extracted_text = extract_text_from_image(processed_image)

        # Clean and refine the extracted text
        cleaned_text = clean_text(extracted_text)
        refined_text = refine_text_with_gemini(cleaned_text)

        # Save the prescription data to Supabase
        supabase.table('prescriptions').insert({
            'user_id': user_id,
            'image_url': image_path,
            'prescription_data': refined_text
        }).execute()

        # Optionally, parse the refined text to extract medicine details
        # and save reminders to the 'reminders' table in Supabase
    except Exception as e:
        print(f"Error processing prescription: {e}")