from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from openai import OpenAI
import speech_recognition as sr
import spacy
import logging
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Voice Assistant API",
    description="A simple AI voice assistant backend with NLP and database integration.",
    version="1.0.0",
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB setup
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING", "mongodb://localhost:27017/")
try:
    client = MongoClient(MONGO_CONNECTION_STRING, serverSelectionTimeoutMS=5000)  # 5-second timeout
    client.server_info()  # Test the connection
    db = client["voice_assistant"]
    interactions_collection = db["interactions"]
    logger.info("Connected to MongoDB successfully.")
except ServerSelectionTimeoutError as e:
    logger.error(f"MongoDB connection error: {e}")
    interactions_collection = None  # Disable database functionality if connection fails

# OpenAI setup
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)


# Pydantic model for text input
class TextInput(BaseModel):
    text: str

# Function for basic intent recognition using keyword matching
def recognize_intent(text: str) -> str:
    text = text.lower()
    if "weather" in text:
        return "get_weather"
    elif "time" in text:
        return "get_time"
    elif "joke" in text:
        return "tell_joke"
    else:
        return "unknown_intent"


# Function for advanced intent recognition using OpenAI
def recognize_intent_with_openai(text: str) -> str:
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that recognizes intents from user input."},
                {"role": "user", "content": f"Recognize the intent of the following text: {text}"},
            ],
            max_tokens=50,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return "unknown_intent"

# Function to log interactions to MongoDB
def log_interaction(text: str, intent: str):
    if interactions_collection is None:
        logger.warning("MongoDB not connected. Skipping interaction logging.")
        return
    interaction = {
        "text": text,
        "intent": intent,
        "timestamp": datetime.now(),
    }
    interactions_collection.insert_one(interaction)
    logger.info(f"Logged interaction: {interaction}")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Vedanta's AI Voice Assistant API!"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Intent recognition endpoint
@app.post("/recognize-intent")
def recognize_intent_endpoint(input: TextInput, use_openai: bool = False):
    """
    Endpoint to recognize intent from text input.
    - If `use_openai` is True, it uses OpenAI for intent recognition.
    - Otherwise, it uses simple keyword matching.
    """
    logger.info(f"Received request: {input.text}")

    if use_openai and OPENAI_API_KEY:
        intent = recognize_intent_with_openai(input.text)
    else:
        intent = recognize_intent(input.text)

    logger.info(f"Recognized intent: {intent}")
    log_interaction(input.text, intent)

    return {"intent": intent}

# Voice input endpoint with OpenAI intent recognition
@app.post("/voice-input")
def voice_input_endpoint():
    text = speech_to_text()
    if not text:
        raise HTTPException(status_code=400, detail="Could not recognize speech.")

    # Use OpenAI to recognize intent
    intent = recognize_intent_with_openai(text) if OPENAI_API_KEY else "unknown_intent"
    logger.info(f"Recognized intent from speech: {intent}")

    # Log the interaction
    log_interaction(text, intent)

    return {"recognized_text": text, "intent": intent}

# Function to convert speech to text
def speech_to_text() -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        logger.info("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            logger.info(f"Recognized speech: {text}")
            return text
        except sr.UnknownValueError:
            logger.error("Google Speech Recognition could not understand the audio.")
            return ""
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech Recognition service; {e}")
            return ""
        
@app.get("/interactions")
def get_interactions():
    if interactions_collection is None:
        raise HTTPException(status_code=500, detail="MongoDB not connected.")

    interactions = list(interactions_collection.find({}, {"_id": 0}))
    return {"interactions": interactions}