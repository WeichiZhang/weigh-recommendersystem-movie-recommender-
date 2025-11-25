# rag_two_tower.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RAGTwoTowerRecommender:
    def __init__(self, enhanced_movies_df):
        self.movies_df = enhanced_movies_df
        self.llm_embeddings = np.array(self.movies_df['llm_embedding'].tolist())
        self.traditional_embeddings = np.array(self.movies_df['traditional_embedding'].tolist())
    
    def recommend(self, user_query, top_k=10, alpha=0.7):
        """Hybrid recommendation using both LLM and traditional embeddings"""
        # Process user query with LLM
        user_llm_embedding = self.process_user_query(user_query)
        
        # Calculate similarities
        llm_similarities = cosine_similarity([user_llm_embedding], self.llm_embeddings)[0]
        traditional_similarities = cosine_similarity([user_llm_embedding], self.traditional_embeddings)[0]
        
        # Hybrid scoring (as shown in Slide 7)
        hybrid_scores = (alpha * llm_similarities + 
                        (1 - alpha) * traditional_similarities)
        
        # Get top recommendations
        top_indices = np.argsort(hybrid_scores)[-top_k:][::-1]
        
        return self.movies_df.iloc[top_indices][['title', 'genres', 'llm_themes', 'llm_tone']]
    
    def process_user_query(self, query):
        """Convert user natural language query to embedding"""
        extractor = LLMFeatureExtractor()
        features = extractor.extract_movie_features(query)
        return extractor.generate_embedding(features)
