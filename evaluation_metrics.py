import numpy as np
from typing import List, Dict, Any
from sklearn.metrics import ndcg_score

class RecSysEvaluator:
    def __init__(self, test_data: Dict[str, List[str]]):
        """
        Initialize evaluator with test data
        test_data: {user_id: [list_of_ground_truth_movie_ids]}
        """
        self.test_data = test_data
    
    def precision_at_k(self, recommendations: List[str], ground_truth: List[str], k: int = 5) -> float:
        """Calculate Precision@K"""
        if k == 0:
            return 0.0
        
        relevant_count = len(set(recommendations[:k]) & set(ground_truth))
        return relevant_count / k
    
    def recall_at_k(self, recommendations: List[str], ground_truth: List[str], k: int = 5) -> float:
        """Calculate Recall@K"""
        if not ground_truth:
            return 0.0
        
        relevant_count = len(set(recommendations[:k]) & set(ground_truth))
        return relevant_count / len(ground_truth)
    
    def ndcg_at_k(self, recommendations: List[str], ground_truth: List[str], k: int = 5) -> float:
        """Calculate NDCG@K"""
        if not ground_truth:
            return 0.0
        
        # Create relevance scores (1 for relevant, 0 for not)
        relevance_scores = [1 if rec in ground_truth else 0 for rec in recommendations[:k]]
        
        # Calculate DCG
        dcg = 0
        for i, rel in enumerate(relevance_scores):
            dcg += rel / np.log2(i + 2)  # i+2 because index starts at 0
        
        # Calculate IDCG (ideal ordering)
        ideal_relevance = [1] * min(len(ground_truth), k)
        ideal_relevance += [0] * (k - len(ideal_relevance))
        
        idcg = 0
        for i, rel in enumerate(ideal_relevance):
            idcg += rel / np.log2(i + 2)
        
        return dcg / idcg if idcg > 0 else 0
    
    def evaluate_all(self, recommendations: List[str], ground_truth: List[str], k: int = 5) -> Dict[str, float]:
        """Evaluate all metrics at K"""
        return {
            f'precision@{k}': self.precision_at_k(recommendations, ground_truth, k),
            f'recall@{k}': self.recall_at_k(recommendations, ground_truth, k),
            f'ndcg@{k}': self.ndcg_at_k(recommendations, ground_truth, k)
        }
    
    def compare_systems(self, baseline_recs: Dict, enhanced_recs: Dict, k: int = 5) -> Dict[str, Any]:
        """
        Compare baseline vs enhanced system performance
        """
        comparison_results = {}
        
        for user_id, ground_truth in self.test_data.items():
            if user_id in baseline_recs and user_id in enhanced_recs:
                baseline_metrics = self.evaluate_all(baseline_recs[user_id], ground_truth, k)
                enhanced_metrics = self.evaluate_all(enhanced_recs[user_id], ground_truth, k)
                
                comparison_results[user_id] = {
                    'baseline': baseline_metrics,
                    'enhanced': enhanced_metrics,
                    'improvement': {
                        metric: enhanced_metrics[metric] - baseline_metrics[metric]
                        for metric in baseline_metrics.keys()
                    }
                }
        
        # Calculate average improvements
        avg_improvement = {}
        for metric in ['precision@5', 'recall@5', 'ndcg@5']:
            improvements = [result['improvement'][metric] for result in comparison_results.values()]
            avg_improvement[metric] = np.mean(improvements) if improvements else 0
        
        return {
            'user_comparisons': comparison_results,
            'average_improvement': avg_improvement,
            'summary': f"LLM+RAG improved recommendations by {avg_improvement.get('precision@5', 0):.2%} on average"
        }

# Example test data generator
class TestDataGenerator:
    @staticmethod
    def generate_sample_test_data(movies_df, num_users=10):
        """Generate sample test data for evaluation"""
        test_data = {}
        all_movie_ids = movies_df['movieId'].tolist() if 'movieId' in movies_df.columns else list(range(len(movies_df)))
        
        for i in range(num_users):
            user_id = f"user_{i}"
            # Simulate user liking 5-15 random movies
            num_liked = np.random.randint(5, 15)
            liked_movies = np.random.choice(all_movie_ids, num_liked, replace=False)
            test_data[user_id] = liked_movies.tolist()
        
        return test_data
