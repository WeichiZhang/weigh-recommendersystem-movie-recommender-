import requests
import json
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import os
from typing import Dict, List, Optional

class LLMFeatureExtractor:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize LLM feature extractor with SentenceTransformer for embeddings
        """
        self.embedding_model = SentenceTransformer(model_name)
        self.hf_token = os.getenv('HF_API_TOKEN', 'your_huggingface_token_here')
    
    def extract_movie_features(self, overview: str, title: str = "") -> Dict:
        """
        Extract structured features from movie overview using LLM-like processing
        In production, this would call Phi-3.5 or Qwen API
        """
        if pd.isna(overview) or overview == "":
            return self._get_default_features(title)
        
        # Simulate LLM processing - in real implementation, call HF API
        features = self._simulate_llm_processing(overview, title)
        return features
    
    def _simulate_llm_processing(self, overview: str, title: str) -> Dict:
        """
        Simulate LLM feature extraction - replace with actual API calls in production
        """
        overview_lower = overview.lower()
        
        # Genre detection
        genres = self._detect_genres(overview_lower)
        
        # Theme extraction
        themes = self._extract_themes(overview_lower)
        
        # Tone analysis
        tone = self._analyze_tone(overview_lower)
        
        # Target audience
        audience = self._determine_audience(overview_lower, genres)
        
        return {
            "genres": genres,
            "themes": themes,
            "tone": tone,
            "target_audience": audience,
            "processed_overview": overview[:200] + "..." if len(overview) > 200 else overview
        }
    
    def _detect_genres(self, text: str) -> List[str]:
        """Detect genres from text content"""
        genres = []
        genre_keywords = {
            'action': ['action', 'fight', 'battle', 'adventure', 'mission'],
            'comedy': ['comedy', 'funny', 'humor', 'laugh', 'joke'],
            'drama': ['drama', 'emotional', 'relationship', 'family', 'life'],
            'thriller': ['thriller', 'suspense', 'mystery', 'tension', 'crime'],
            'sci-fi': ['sci-fi', 'science fiction', 'space', 'future', 'alien'],
            'romance': ['romance', 'love', 'relationship', 'couple'],
            'horror': ['horror', 'scary', 'terror', 'fear', 'ghost'],
            'documentary': ['documentary', 'real', 'true story', 'biography']
        }
        
        for genre, keywords in genre_keywords.items():
            if any(keyword in text for keyword in keywords):
                genres.append(genre)
        
        return genres if genres else ['drama']  # Default fallback
    
    def _extract_themes(self, text: str) -> List[str]:
        """Extract themes from text content"""
        themes = []
        theme_keywords = {
            'friendship': ['friend', 'buddy', 'companion'],
            'love': ['love', 'romance', 'relationship'],
            'betrayal': ['betray', 'treason', 'deception'],
            'revenge': ['revenge', 'vengeance', 'retaliation'],
            'justice': ['justice', 'law', 'court'],
            'survival': ['survive', 'survival', 'alive'],
            'identity': ['identity', 'who am i', 'self-discovery'],
            'technology': ['technology', 'computer', 'AI', 'robot']
        }
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in text for keyword in keywords):
                themes.append(theme)
        
        return themes if themes else ['human experience']
    
    def _analyze_tone(self, text: str) -> str:
        """Analyze the tone of the text"""
        tone_indicators = {
            'dark': ['dark', 'grim', 'bleak', 'tragic', 'death'],
            'lighthearted': ['funny', 'happy', 'joy', 'light', 'comedy'],
            'serious': ['serious', 'dramatic', 'intense', 'emotional'],
            'suspenseful': ['suspense', 'mystery', 'thriller', 'tension'],
            'inspirational': ['inspire', 'hope', 'triumph', 'success']
        }
        
        for tone, indicators in tone_indicators.items():
            if any(indicator in text for indicator in indicators):
                return tone
        
        return 'neutral'
    
    def _determine_audience(self, text: str, genres: List[str]) -> str:
        """Determine target audience"""
        if 'horror' in genres or 'thriller' in genres:
            return 'adult'
        elif 'comedy' in genres or 'animation' in genres:
            return 'family'
        elif 'romance' in genres:
            return 'teen-adult'
        else:
            return 'general'
    
    def _get_default_features(self, title: str) -> Dict:
        """Return default features when overview is missing"""
        return {
            "genres": ["drama"],
            "themes": ["human experience"],
            "tone": "neutral",
            "target_audience": "general",
            "processed_overview": f"Movie: {title}"
        }
    
    def generate_embedding(self, features: Dict) -> np.ndarray:
        """Generate embedding from structured features"""
        feature_text = self._features_to_text(features)
        embedding = self.embedding_model.encode(feature_text)
        return embedding
    
    def _features_to_text(self, features: Dict) -> str:
        """Convert features to text for embedding generation"""
        genres = ", ".join(features['genres'])
        themes = ", ".join(features['themes'])
        return f"Genres: {genres}. Themes: {themes}. Tone: {features['tone']}. Audience: {features['target_audience']}"

# Production version with actual LLM API (uncomment when you have API access)
"""
class ProductionLLMExtractor(LLMFeatureExtractor):
    def extract_movie_features(self, overview: str, title: str = "") -> Dict:
        API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        
        prompt = f"""
        You are a movie expert. Extract: genre, themes, tone, target_audience from this movie overview.
        Output format: JSON with keys [genres, themes, tone, target_audience]
        
        Movie: {title}
        Overview: {overview}
        
        Output:
        """
        
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 200, "temperature": 0.1}
        }
        
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                llm_output = result[0].get('generated_text', '{}')
                return self._parse_llm_response(llm_output)
        except Exception as e:
            print(f"LLM API error: {e}")
        
        return self._get_default_features(title)
    
    def _parse_llm_response(self, llm_output: str) -> Dict:
        # Extract JSON from LLM response
        try:
            # Find JSON in the response
            start = llm_output.find('{')
            end = llm_output.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = llm_output[start:end]
                return json.loads(json_str)
        except:
            pass
        
        return self._get_default_features("")
"""
