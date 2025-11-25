# llm_feature_extractor.py
import requests
import json
import pandas as pd
from sentence_transformers import SentenceTransformer

class LLMFeatureExtractor:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def extract_movie_features(self, overview):
        """Use LLM to extract structured features from movie overview"""
        prompt = f"""
        You are a movie expert. Extract the core themes, genres, and emotional tone from this movie overview.
        Output format: JSON with keys [genre, themes, tone, target_audience]
        
        Input: {overview}
        Output: """
        
        # Use Hugging Face Inference API or local model
        response = self.call_llm_api(prompt)
        return self.parse_llm_response(response)
    
    def call_llm_api(self, prompt):
        """Call Phi-3.5 or Qwen API"""
        # Implementation for Hugging Face Inference API
        API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
        headers = {"Authorization": "Bearer YOUR_HF_TOKEN"}
        
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 200, "temperature": 0.1}
        }
        
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()[0]['generated_text']
    
    def generate_embedding(self, structured_features):
        """Convert structured features to embedding vector"""
        feature_text = f"Genre: {structured_features['genre']}. Themes: {structured_features['themes']}. Tone: {structured_features['tone']}"
        return self.model.encode(feature_text)
