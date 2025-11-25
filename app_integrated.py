from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from enhanced_two_tower import EnhancedTwoTowerRecommender
from data_processing import load_and_process_data  # Your existing data processing

app = Flask(__name__)

# Load data using your existing pipeline
print("Loading movie data...")
movies_df, ratings_df = load_and_process_data()
print("Data loaded successfully!")

# Initialize enhanced recommender
print("Initializing Enhanced Two-Tower Recommender with LLM+RAG...")
recommender = EnhancedTwoTowerRecommender(movies_df)
print("Enhanced recommender ready!")

@app.route('/')
def home():
    """Serve the enhanced interface"""
    return render_template('index_enhanced.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    """Enhanced recommendation endpoint"""
    try:
        data = request.get_json()
        
        if 'query' in data:
            # Enhanced LLM+RAG recommendations
            user_query = data['query']
            recommendations, search_criteria = recommender.recommend_from_query(
                user_query, top_k=10, use_llm=True, alpha=0.7
            )
            
            # Convert to JSON format
            result = {
                'query': user_query,
                'search_criteria': search_criteria,
                'recommendations': [],
                'type': 'enhanced'
            }
            
            for _, movie in recommendations.iterrows():
                result['recommendations'].append({
                    'title': movie.get('title', 'Unknown'),
                    'score': float(movie.get('similarity_score', 0)),
                    'genres': movie.get('llm_genres', []),
                    'themes': movie.get('llm_themes', []),
                    'tone': movie.get('llm_tone', ''),
                    'explanation': movie.get('explanation', ''),
                    'year': movie.get('year', '')
                })
            
            return jsonify(result)
            
        elif 'user_id' in data:
            # Fallback to traditional recommendations for user ID
            user_id = data['user_id']
            # You can implement user-based enhanced recommendations here
            return jsonify({'error': 'User-based enhanced recommendations not implemented yet'})
            
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/traditional_recommend', methods=['POST'])
def traditional_recommend():
    """Traditional recommendations for comparison"""
    # Your existing traditional Two-Tower logic
    pass

if __name__ == '__main__':
    app.run(debug=True, port=5001)
