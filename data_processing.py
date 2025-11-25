# Enhanced data processing with LLM features
def enhance_movie_data_with_llm(movies_df):
    extractor = LLMFeatureExtractor()
    
    enhanced_movies = []
    for _, movie in movies_df.iterrows():
        # Get LLM structured features
        features = extractor.extract_movie_features(movie['overview'])
        
        # Generate embedding from structured features
        embedding = extractor.generate_embedding(features)
        
        enhanced_movie = {
            'movieId': movie['movieId'],
            'title': movie['title'],
            'genres': movie['genres'],
            'llm_genre': features['genre'],
            'llm_themes': features['themes'],
            'llm_tone': features['tone'],
            'llm_embedding': embedding.tolist(),
            'traditional_embedding': movie['embedding']  # Keep original
        }
        enhanced_movies.append(enhanced_movie)
    
    return pd.DataFrame(enhanced_movies)
