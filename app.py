# Enhanced main application
from rag_two_tower import RAGTwoTowerRecommender
from evaluation_metrics import RecSysEvaluator

def main():
    # Load your existing data
    movies_df = load_movie_data()
    
    # Enhance with LLM features
    enhanced_movies = enhance_movie_data_with_llm(movies_df)
    
    # Initialize RAG-enhanced recommender
    recommender = RAGTwoTowerRecommender(enhanced_movies)
    
    # Example usage
    user_query = "I want a scary movie with psychological tension, no supernatural elements"
    recommendations = recommender.recommend(user_query, top_k=10)
    
    print("RAG-Enhanced Recommendations:")
    for idx, movie in recommendations.iterrows():
        print(f"- {movie['title']} (Themes: {movie['llm_themes']}, Tone: {movie['llm_tone']})")
    
    # Evaluate system
    evaluator = RecSysEvaluator(test_data)
    metrics = evaluator.evaluate_all(recommendations['movieId'].tolist(), ground_truth_movies)
    print(f"Evaluation Metrics: {metrics}")
