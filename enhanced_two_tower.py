import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
from llm_feature_extractor import LLMFeatureExtractor
from rag_query_processor import RAGQueryProcessor

class EnhancedTwoTowerRecommender:
    def __init__(self, movies_df: pd.DataFrame):
        """
        Enhanced Two-Tower recommender with LLM+RAG capabilities
        """
        self.movies_df = movies_df
        self.feature_extractor = LLMFeatureExtractor()
        self.query_processor = RAGQueryProcessor()
        
        # Precompute LLM embeddings if not already present
        if 'llm_embedding' not in self.movies_df.columns:
            self._enhance_movie_data()
    
    def _enhance_movie_data(self):
        """Add LLM features and embeddings to movie data"""
        print("Enhancing movie data with LLM features...")
        
        llm_features = []
        llm_embeddings = []
        
        for _, movie in self.movies_df.iterrows():
            features = self.feature_extractor.extract_movie_features(
                movie.get('overview', ''), 
                movie.get('title', '')
            )
            embedding = self.feature_extractor.generate_embedding(features)
            
            llm_features.append(features)
            llm_embeddings.append(embedding)
        
        self.movies_df['llm_features'] = llm_features
        self.movies_df['llm_embedding'] = llm_embeddings
        
        # Extract feature columns for easier access
        self.movies_df['llm_genres'] = self.movies_df['llm_features'].apply(lambda x: x['genres'])
        self.movies_df['llm_themes'] = self.movies_df['llm_features'].apply(lambda x: x['themes'])
        self.movies_df['llm_tone'] = self.movies_df['llm_features'].apply(lambda x: x['tone'])
    
    def recommend_from_query(self, user_query: str, top_k: int = 10, 
                           use_llm: bool = True, alpha: float = 0.7) -> pd.DataFrame:
        """
        Generate recommendations from natural language query
        """
        # Process user query
        search_criteria = self.query_processor.process_user_query(user_query)
        
        if use_llm:
            # Use LLM-enhanced recommendations
            recommendations = self._llm_enhanced_recommend(search_criteria, top_k, alpha)
        else:
            # Use traditional recommendations (baseline)
            recommendations = self._traditional_recommend(search_criteria, top_k)
        
        # Add explanations
        recommendations = self._add_explanations(recommendations, search_criteria)
        
        return recommendations, search_criteria
    
    def _llm_enhanced_recommend(self, search_criteria: Dict, top_k: int, alpha: float) -> pd.DataFrame:
        """LLM-enhanced hybrid recommendations"""
        user_vector = search_criteria['search_vector']
        
        # Calculate similarities
        llm_embeddings = np.array(self.movies_df['llm_embedding'].tolist())
        llm_similarities = cosine_similarity([user_vector], llm_embeddings)[0]
        
        # If traditional embeddings exist, use hybrid scoring
        if 'traditional_embedding' in self.movies_df.columns:
            traditional_embeddings = np.array(self.movies_df['traditional_embedding'].tolist())
            traditional_similarities = cosine_similarity([user_vector], traditional_embeddings)[0]
            
            # Hybrid scoring (Slide 7)
            hybrid_scores = (alpha * llm_similarities + (1 - alpha) * traditional_similarities)
        else:
            hybrid_scores = llm_similarities
        
        # Apply genre filters
        filtered_scores = self._apply_filters(hybrid_scores, search_criteria)
        
        # Get top recommendations
        top_indices = np.argsort(filtered_scores)[-top_k:][::-1]
        recommendations = self.movies_df.iloc[top_indices].copy()
        recommendations['similarity_score'] = filtered_scores[top_indices]
        
        return recommendations
    
    def _traditional_recommend(self, search_criteria: Dict, top_k: int) -> pd.DataFrame:
        """Traditional recommendations (baseline)"""
        user_vector = search_criteria['search_vector']
        
        if 'traditional_embedding' in self.movies_df.columns:
            traditional_embeddings = np.array(self.movies_df['traditional_embedding'].tolist())
            similarities = cosine_similarity([user_vector], traditional_embeddings)[0]
        else:
            # Fallback to LLM embeddings
            llm_embeddings = np.array(self.movies_df['llm_embedding'].tolist())
            similarities = cosine_similarity([user_vector], llm_embeddings)[0]
        
        filtered_scores = self._apply_filters(similarities, search_criteria)
        top_indices = np.argsort(filtered_scores)[-top_k:][::-1]
        
        recommendations = self.movies_df.iloc[top_indices].copy()
        recommendations['similarity_score'] = filtered_scores[top_indices]
        
        return recommendations
    
    def _apply_filters(self, scores: np.ndarray, search_criteria: Dict) -> np.ndarray:
        """Apply genre filters to scores"""
        filtered_scores = scores.copy()
        
        # Penalize excluded genres
        excluded_genres = search_criteria['excluded_genres']
        if excluded_genres:
            for idx, movie in self.movies_df.iterrows():
                movie_genres = movie.get('llm_genres', []) or movie.get('genres', [])
                if any(excluded_genre in str(movie_genres).lower() for excluded_genre in excluded_genres):
                    filtered_scores[idx] *= 0.1  # Heavy penalty
        
        return filtered_scores
    
    def _add_explanations(self, recommendations: pd.DataFrame, search_criteria: Dict) -> pd.DataFrame:
        """Add LLM-generated explanations to recommendations"""
        explanations = []
        match_reasons_list = []
        
        for _, movie in recommendations.iterrows():
            match_reasons = self._find_match_reasons(movie, search_criteria)
            explanation = self.query_processor.generate_explanation(
                movie['title'], search_criteria, match_reasons
            )
            explanations.append(explanation)
            match_reasons_list.append(match_reasons)
        
        recommendations['explanation'] = explanations
        recommendations['match_reasons'] = match_reasons_list
        
        return recommendations
    
    def _find_match_reasons(self, movie: pd.Series, search_criteria: Dict) -> List[str]:
        """Find reasons why movie matches user criteria"""
        reasons = []
        
        # Check genre matches
        movie_genres = movie.get('llm_genres', [])
        preferred_genres = search_criteria['preferred_genres']
        if any(genre in movie_genres for genre in preferred_genres):
            matching_genres = [genre for genre in preferred_genres if genre in movie_genres]
            reasons.append(f"{', '.join(matching_genres)} elements")
        
        # Check theme matches
        movie_themes = movie.get('llm_themes', [])
        preferred_themes = search_criteria['preferred_themes']
        if any(theme in movie_themes for theme in preferred_themes):
            reasons.append(f"thematic depth")
        
        # Check tone matches
        movie_tone = movie.get('llm_tone', '')
        preferred_tone = search_criteria['preferred_tone']
        if movie_tone == preferred_tone and preferred_tone != 'neutral':
            reasons.append(f"{movie_tone} atmosphere")
        
        return reasons if reasons else ["high-quality storytelling"]
