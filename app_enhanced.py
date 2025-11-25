from flask import Flask, request, jsonify
from enhanced_two_tower import EnhancedTwoTowerRecommender
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load your movie data
movies_df = pd.read_csv('your_movies_data.csv')  # Replace with your actual data
recommender = EnhancedTwoTowerRecommender(movies_df)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        user_query = data.get('query', '')
        
        # Get enhanced recommendations
        recommendations, search_criteria = recommender.recommend_from_query(
            user_query, top_k=10, use_llm=True, alpha=0.7
        )
        
        # Convert to JSON-serializable format
        rec_list = []
        for _, movie in recommendations.iterrows():
            rec_list.append({
                'title': movie['title'],
                'similarity_score': float(movie['similarity_score']),
                'llm_themes': movie.get('llm_themes', []),
                'llm_tone': movie.get('llm_tone', ''),
                'explanation': movie.get('explanation', '')
            })
        
        # Simulate metrics (replace with actual evaluation)
        metrics = {
            'precision': 0.78 + np.random.random() * 0.1,
            'recall': 0.42 + np.random.random() * 0.1,
            'ndcg': 0.82 + np.random.random() * 0.1,
            'improvement': 25
        }
        
        return jsonify({
            'query': user_query,
            'search_criteria': search_criteria,
            'recommendations': rec_list,
            'metrics': metrics
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
