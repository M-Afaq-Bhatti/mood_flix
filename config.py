# Configuration and constants
"""
Configuration file for Netflix Recommendation Chatbot
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.0-flash"

# Database Configuration
DB_PATH = "database/netflix_db"
COLLECTION_NAME = "netflix_movies"

# Data Configuration
DATASET_PATH = "data/netflix_content.csv"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
BATCH_SIZE = 500

# Emotion to Query Mapping
EMOTION_QUERIES = {
    "😊 Happy": "uplifting comedy movies and feel-good series that bring joy and laughter",
    "😢 Sad": "heartwarming and comforting movies that provide emotional healing",
    "😡 Angry": "action-packed thrillers and intense dramas to release tension",
    "😴 Relaxed": "calm and peaceful documentaries or light-hearted romantic comedies",
    "💪 Motivated": "inspirational biographical movies and success stories",
    "😱 Excited": "exciting adventure movies and suspenseful thrillers",
    "💔 Heartbroken": "romantic dramas and emotional love stories for healing",
    "🤔 Thoughtful": "thought-provoking documentaries and philosophical dramas",
    "😂 Playful": "fun animated movies and comedy series for entertainment",
    "😌 Peaceful": "nature documentaries and meditation-inducing slow-paced films",
    "🔥 Energetic": "high-energy action movies and fast-paced adventure series",
    "🧠 Curious": "educational documentaries and mystery series to satisfy curiosity"
}

# Streamlit Configuration
PAGE_TITLE = "Netflix AI Recommender"
PAGE_ICON = "🎬"
LAYOUT = "wide"

# UI Colors and Styling
NETFLIX_RED = "#E50914"
NETFLIX_DARK = "#141414"
NETFLIX_GRAY = "#564D4D"