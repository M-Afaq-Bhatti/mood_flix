# RAG pipeline and Gemini integration
"""
Recommendation engine module for Netflix chatbot
Handles RAG pipeline and Gemini AI integration
"""
import google.generativeai as genai
import streamlit as st
from config import *


class RecommendationEngine:
    def __init__(self, collection):
        self.collection = collection
        self.model = None
        self.initialize_gemini()
    
    def initialize_gemini(self):
        """Initialize Gemini AI model"""
        try:
            if not GEMINI_API_KEY:
                st.error("🔑 Gemini API key not found! Please set GEMINI_API_KEY in your .env file")
                return False
            
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel(GEMINI_MODEL)
            return True
            
        except Exception as e:
            st.error(f"Error initializing Gemini: {str(e)}")
            return False
    
    def search_content(self, query, n_results=5):
        """Search for content in ChromaDB based on query"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results
        except Exception as e:
            st.error(f"Error searching content: {str(e)}")
            return None
    
    def generate_emotion_based_recommendations(self, emotion, n_results=10):
        """Generate recommendations based on selected emotion"""
        try:
            # Get emotion-specific query from config
            emotion_query = EMOTION_QUERIES.get(emotion, "general entertainment content")
            
            # Search in ChromaDB
            results = self.search_content(emotion_query, n_results)
            if not results or not results["documents"][0]:
                return "Sorry, I couldn't find suitable recommendations for your mood."
            
            # Build context for Gemini
            context = self.build_context(results)
            
            # Generate recommendations using Gemini
            recommendations = self.generate_with_gemini(emotion, emotion_query, context)
            
            return recommendations
            
        except Exception as e:
            st.error(f"Error generating recommendations: {str(e)}")
            return "Sorry, I encountered an error while generating recommendations."
    
    def build_context(self, results):
        """Build context string from search results"""
        context = ""
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            title = meta.get('title', 'Unknown Title')
            category = meta.get('category', 'Unknown Category')
            genre = meta.get('genre', 'Unknown Genre')
            year = meta.get('year', 'Unknown Year')
            rating = meta.get('rating', 'Not Rated')
            
            context += f"""
Title: {title}
Type: {category}
Genre: {genre}
Year: {year}
Rating: {rating}
Overview: {doc[:300]}...

---
"""
        return context
    
    def generate_with_gemini(self, emotion, emotion_query, context):
        """Generate recommendations using Gemini AI"""
        try:
            prompt = f"""
You are Netflix's premium AI recommendation assistant. A user is feeling {emotion.replace('😊', '').replace('😢', '').replace('😡', '').replace('😴', '').replace('💪', '').replace('😱', '').replace('💔', '').replace('🤔', '').replace('😂', '').replace('😌', '').replace('🔥', '').replace('🧠', '').strip()} and wants content recommendations.

User's Current Mood: {emotion}
Content Preference: {emotion_query}

Here are the top matching titles from Netflix's catalog:
{context}

INSTRUCTIONS:
1. Recommend exactly 5 titles from the provided context
2. For each recommendation, provide:
   - Title and type (Movie/TV Show)
   - Why it matches their current mood
   - Brief engaging description (2-3 sentences)
   - What makes it special or unique

3. Format your response in a warm, personalized tone
4. Start with acknowledging their mood
5. Use emojis appropriately to match the mood
6. End with an encouraging note about enjoying their viewing experience

Make the recommendations feel personal and thoughtful, as if coming from a close friend who knows their taste perfectly.
"""

            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            st.error(f"Error with Gemini API: {str(e)}")
            return f"I understand you're feeling {emotion}, but I'm having trouble accessing my recommendation engine right now. Please try again in a moment!"
    
    def get_content_details(self, title_query):
        """Get detailed information about a specific title"""
        try:
            results = self.search_content(title_query, n_results=1)
            if results and results["documents"][0]:
                meta = results["metadatas"][0][0]
                doc = results["documents"][0][0]
                
                details = {
                    "title": meta.get('title', 'Unknown'),
                    "category": meta.get('category', 'Unknown'),
                    "genre": meta.get('genre', 'Unknown'),
                    "year": meta.get('year', 'Unknown'),
                    "rating": meta.get('rating', 'Not Rated'),
                    "overview": doc
                }
                return details
            return None
        except Exception as e:
            st.error(f"Error getting content details: {str(e)}")
            return None
