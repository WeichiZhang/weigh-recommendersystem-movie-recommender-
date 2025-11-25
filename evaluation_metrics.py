# evaluation_metrics.py
import numpy as np

class RecSysEvaluator:
    def __init__(self, test_interactions):
        self.test_data = test_interactions
    
    def precision_at_k(self, recommendations, ground_truth, k=5):
        """Calculate Precision@K"""
        relevant_count = len(set(recommendations[:k]) & set(ground_truth))
        return relevant_count / k
    
    def recall_at_k(self, recommendations, ground_truth, k=5):
        """Calculate Recall@K"""
        relevant_count = len(set(recommendations[:k]) & set(ground_truth))
        return relevant_count / len(ground_truth) if ground_truth else 0
    
    def ndcg_at_k(self, recommendations, ground_truth, k=5):
        """Calculate NDCG@K"""
        dcg = 0
        for i, rec in enumerate(recommendations[:k]):
            if rec in ground_truth:
                dcg += 1 / np.log2(i + 2)
        
        idcg = sum(1 / np.log2(i + 2) for i in range(min(len(ground_truth), k)))
        return dcg / idcg if idcg > 0 else 0
    
    def evaluate_all(self, recommendations, ground_truth, k=5):
        return {
            'precision@5': self.precision_at_k(recommendations, ground_truth, k),
            'recall@5': self.recall_at_k(recommendations, ground_truth, k),
            'ndcg@5': self.ndcg_at_k(recommendations, ground_truth, k)
        }
