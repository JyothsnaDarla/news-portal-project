import os
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Set a secret API key (Change this to your own strong key)
# Reads key from environment variable (best practice) or defaults to "letmein"
API_KEY = os.environ.get("TRANSLATE_API_KEY", "translate_to_hindi_Coderbot")

# --- Project Glossary ---
PROJECT_GLOSSARY = {
    "Dashboard": "डैशबोर्ड",
    "Workflow": "वर्कफ़्लो",
    "API Key": "एपीआई कुंजी",
    "Commit": "कमिट",
    "Welcome to our platform": "हमारे प्लेटफॉर्म पर आपका स्वागत है",
}

def apply_glossary(text: str) -> str:
    """Replaces English terms with their Hindi equivalent before sending to the model."""
    for en_term, hi_term in PROJECT_GLOSSARY.items():
        text = text.replace(en_term, hi_term)
    return text
# --- End Glossary ---


# Choose Hugging Face model
MODEL = "Helsinki-NLP/opus-mt-en-hi" 

print(f"Loading model: {MODEL}...")
try:
    # Model and Tokenizer loading happens only once when the server starts
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL)
    translator = pipeline("translation", model=model, tokenizer=tokenizer)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    
app = FastAPI()

origins = [
    "http://localhost:3000", # The address where your React app runs
    "http://127.0.0.1:3000", # The common alternative address for React
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Allows connections from your frontend
    allow_credentials=True,
    allow_methods=["*"],            
    allow_headers=["*"],
)
# --- END CORS BLOCK ---
class Req(BaseModel):
    text: str

@app.post("/translate")
def translate(req: Req, x_api_key: str | None = Header(None)):
    if x_api_key != API_KEY:
        # 401 Unauthorized error for security
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # 1. Apply custom project terminology
    pre_processed_text = apply_glossary(req.text)
    
    # 2. Run the translation pipeline
    out = translator(pre_processed_text, max_length=512)
    
    return {"translation": out[0]["translation_text"]}