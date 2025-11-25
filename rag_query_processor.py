import numpy as np
from typing import Dict, List
from llm_feature_extractor import LLMFeatureExtractor

class RAGQueryProcessor:
    def __init__(self):
        self.feature_extractor = LLMFeatureExtractor()
    
    def process_user_query(self, query: str) -> Dict:
        """
        Process natural language user query into structured search criteria
        """
        # Simulate LLM query understanding - replace with actual API call
        search_criteria = self._simulate_query_understanding(query)
        return search_criteria
    
    def _simulate_query_understanding(self, query: str) -> Dict:
        """
        Simulate LLM query processing - in production, call actual LLM API
        """
        query_lower = query.lower()
        
        # Extract intent
        intent = self._extract_intent(query_lower)
        
        # Extract genres
        preferred_genres = self._extract_genres(query_lower)
        excluded_genres = self._extract_exclusions(query_lower)
        
        # Extract themes and tone
        preferred_themes = self._extract_themes(query_lower)
        preferred_tone = self._extract_tone_preference(query_lower)
        
        return {
            "original_query": query,
            "intent": intent,
            "preferred_genres": preferred_genres,
            "excluded_genres": excluded_genres,
            "preferred_themes": preferred_themes,
            "preferred_tone": preferred_tone,
            "search_vector": self._generate_search_vector(preferred_genres, preferred_themes, preferred_tone)
        }
    
    def _extract_intent(self, query: str) -> str:
        """Extract user's search intent"""
        if any(word in query for word in ['scary', 'horror', 'frightening', 'creepy']):
            return 'horror'
        elif any(word in query for word in ['funny', 'comedy', 'laugh', 'humor']):
            return 'comedy'
        elif any(word in query for word in ['romantic', 'love', 'relationship']):
            return 'romance'
        elif any(word in query for word in ['action', 'adventure', 'exciting']):
            return 'action'
        elif any(word in query for word in ['thoughtful', 'drama', 'emotional']):
            return 'drama'
        else:
            return 'general'
    
    def _extract_genres(self, query: str) -> List[str]:
        """Extract preferred genres from query"""
        genres = []
        genre_map = {
            'action': ['action', 'adventure', 'exciting'],
            'comedy': ['comedy', 'funny', 'humor'],
            'drama': ['drama', 'emotional', 'serious'],
            'thriller': ['thriller', 'suspense', 'mystery'],
            'sci-fi': ['sci-fi', 'science fiction', 'space'],
            'romance': ['romance', 'love', 'relationship'],
            'horror': ['horror', 'scary', 'frightening']
        }
        
        for genre, keywords in genre_map.items():
            if any(keyword in query for keyword in keywords):
                genres.append(genre)
        
        return genres
    
    def _extract_exclusions(self, query: str) -> List[str]:
        """Extract genres to exclude"""
        exclusions = []
        if 'no superhero' in query or 'not superhero' in query:
            exclusions.append('action')
        if 'no horror' in query or 'not scary' in query:
            exclusions.append('horror')
        if 'no romance' in query:
            exclusions.append('romance')
        
        return exclusions
    
    def _extract_themes(self, query: str) -> List[str]:
        """Extract preferred themes"""
        themes = []
        theme_keywords = {
            'friendship': ['friend', 'buddy'],
            'family': ['family', 'parent'],
            'adventure': ['adventure', 'journey'],
            'mystery': ['mystery', 'secret'],
            'coming of age': ['growing up', 'young adult'],
            'crime': ['crime', 'detective']
        }
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in query for keyword in keywords):
                themes.append(theme)
        
        return themes
    
    def _extract_tone_preference(self, query: str) -> str:
        """Extract tone preference"""
        if any(word in query for word in ['dark', 'gritty', 'serious']):
            return 'dark'
        elif any(word in query for word in ['light', 'fun', 'happy']):
            return 'lighthearted'
        elif any(word in query for word in ['suspenseful', 'tense']):
            return 'suspenseful'
        else:
            return 'neutral'
    
    def _generate_search_vector(self, genres: List[str], themes: List[str], tone: str) -> np.ndarray:
        """Generate search vector from structured criteria"""
        search_text = f"Genres: {', '.join(genres)}. Themes: {', '.join(themes)}. Tone: {tone}"
        return self.feature_extractor.embedding_model.encode(search_text)
    
    def generate_explanation(self, movie_title: str, user_criteria: Dict, match_reasons: List[str]) -> str:
        """
        Generate natural language explanation for recommendation
        """
        reasons_text = ", ".join(match_reasons)
        
        explanations = [
            f"**{movie_title}** matches your preference for {reasons_text}.",
            f"Recommended **{movie_title}** because it aligns with your interest in {reasons_text}.",
            f"Based on your search, **{movie_title}** fits well with {reasons_text}."
        ]
        
        return np.random.choice(explanations)
