# Data loading and ChromaDB setup
"""
Data processing module for Netflix recommendation chatbot
Handles dataset loading, cleaning, and ChromaDB initialization
"""
import os
import shutil
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
import streamlit as st
from config import *


class DataProcessor:
    def __init__(self):
        self.df = None
        self.client = None
        self.collection = None
        self.embedding_model = None
    
    @st.cache_data
    def load_and_clean_data(_self, dataset_path=DATASET_PATH):
        """Load and clean Netflix dataset"""
        try:
            df = pd.read_csv(dataset_path)
            
            # Keep only rows with non-empty overviews
            df = df.dropna(subset=["overview"])
            df = df[df["overview"].str.strip() != ""]
            
            # Reset index
            df = df.reset_index(drop=True)
            
            return df
        except FileNotFoundError:
            st.error(f"Dataset file not found at {dataset_path}")
            return None
        except Exception as e:
            st.error(f"Error loading dataset: {str(e)}")
            return None
    
    def initialize_chromadb(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Create database directory if it doesn't exist
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(path=DB_PATH)
            
            # Create or get collection
            self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)
            
            return True
        except Exception as e:
            st.error(f"Error initializing ChromaDB: {str(e)}")
            return False
    
    @st.cache_resource
    def load_embedding_model(_self):
        """Load sentence transformer model"""
        try:
            return SentenceTransformer(EMBEDDING_MODEL)
        except Exception as e:
            st.error(f"Error loading embedding model: {str(e)}")
            return None
    
    def setup_database(self):
        """Complete database setup process"""
        # Load data
        self.df = self.load_and_clean_data()
        if self.df is None:
            return False
        
        # Initialize ChromaDB
        if not self.initialize_chromadb():
            return False
        
        # Load embedding model
        self.embedding_model = self.load_embedding_model()
        if self.embedding_model is None:
            return False
        
        # Check if data already exists in collection
        if self.collection.count() > 0:
            st.info("Using existing database with {} documents".format(self.collection.count()))
            return True
        
        # Add data to ChromaDB
        return self.populate_database()
    
    def populate_database(self):
        """Add data to ChromaDB in batches"""
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_batches = len(self.df) // BATCH_SIZE + (1 if len(self.df) % BATCH_SIZE != 0 else 0)
            
            for i in range(0, len(self.df), BATCH_SIZE):
                batch = self.df.iloc[i:i+BATCH_SIZE]
                texts = batch["overview"].tolist()
                
                # Generate embeddings
                embeddings = self.embedding_model.encode(texts).tolist()
                
                # Add to collection
                self.collection.add(
                    ids=[str(x) for x in batch.index],
                    documents=texts,
                    embeddings=embeddings,
                    metadatas=batch.to_dict("records")
                )
                
                # Update progress
                current_batch = (i // BATCH_SIZE) + 1
                progress = current_batch / total_batches
                progress_bar.progress(progress)
                status_text.text(f"Processing batch {current_batch}/{total_batches}")
            
            progress_bar.empty()
            status_text.empty()
            
            st.success(f"✅ Database initialized with {self.collection.count()} documents")
            return True
            
        except Exception as e:
            st.error(f"Error populating database: {str(e)}")
            return False
    
    def get_collection(self):
        """Return the ChromaDB collection"""
        return self.collection
    
    def get_stats(self):
        """Return dataset statistics"""
        if self.df is None:
            return None
        
        stats = {
            "total_items": len(self.df),
            "movies": len(self.df[self.df['category'] == 'Movie']) if 'category' in self.df.columns else 0,
            "series": len(self.df[self.df['category'] == 'TV Show']) if 'category' in self.df.columns else 0,
            "genres": self.df['genre'].nunique() if 'genre' in self.df.columns else 0
        }
        return stats