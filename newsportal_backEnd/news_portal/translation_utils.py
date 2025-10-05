import requests
import json
from django.conf import settings # Use Django settings for API key

# --- CONFIGURATION ---
# IMPORTANT: Since you are using a Django project, you should store the 
# API_KEY and API_URL in your settings.py file, NOT hardcoded here.
# Use the exact key you verified!
API_URL = settings.TRANSLATION_API_URL
API_KEY = settings.TRANSLATION_API_KEY 
# Note: Ideally, set this in settings.py: 
# TRANSLATION_API_KEY = "translate_to_hindi_Coderbot"
# And then use: settings.TRANSLATION_API_KEY 

def translate_to_hindi(english_text: str) -> str:
    """Sends a request to your local Hindi Translation API."""
    
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": API_KEY, 
    }
    
    payload = {
        "text": english_text
    }
    
    try:
        # Use a timeout in case the local API server is slow or down
        response = requests.post(API_URL, headers=headers, json=payload, timeout=5)
        response.raise_for_status() # Raise an exception for errors (401, 404)
        
        # Extract the translation
        translation = response.json().get("translation", english_text)
        return translation
        
    except requests.exceptions.RequestException as e:
        # Fallback: Log the error and return the original English text
        print(f"ERROR: Translation API failed. Returning English text. Details: {e}")
        return english_text

# --- Example of usage in your Django views or models ---
# from .translation_utils import translate_to_hindi
# 
# def get_hindi_title(english_title):
#     return translate_to_hindi(english_title)