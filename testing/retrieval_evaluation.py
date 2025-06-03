# retrieval_evaluation.py

from typing import List
import numpy as np
# from sklearn.metrics import average_precision_score
from sklearn.metrics import average_precision_score


def precision_at_k(relevant: List[int], retrieved: List[int], k: int) -> float:
    retrieved_at_k = retrieved[:k]
    relevant_set = set(relevant)
    return sum(1 for item in retrieved_at_k if item in relevant_set) / k

def recall_at_k(relevant: List[int], retrieved: List[int], k: int) -> float:
    retrieved_at_k = retrieved[:k]
    relevant_set = set(relevant)
    return sum(1 for item in retrieved_at_k if item in relevant_set) / len(relevant_set)

def mean_reciprocal_rank(relevant_lists: List[List[int]], retrieved_lists: List[List[int]]) -> float:
    mrr = 0.0
    for rel, ret in zip(relevant_lists, retrieved_lists):
        for i, r in enumerate(ret):
            if r in rel:
                mrr += 1.0 / (i + 1)
                break
    return mrr / len(relevant_lists)

def evaluate_retrieval(relevant_lists: List[List[int]], retrieved_lists: List[List[int]], k: int = 5):
    precisions = [precision_at_k(rel, ret, k) for rel, ret in zip(relevant_lists, retrieved_lists)]
    recalls = [recall_at_k(rel, ret, k) for rel, ret in zip(relevant_lists, retrieved_lists)]
    mrr = mean_reciprocal_rank(relevant_lists, retrieved_lists)

    print(f"Precision@{k}: {np.mean(precisions):.4f}")
    print(f"Recall@{k}: {np.mean(recalls):.4f}")
    print(f"MRR: {mrr:.4f}")

# Example usage
if __name__ == "__main__":
    # # Example: each query has a list of relevant doc IDs and a list of retrieved doc IDs
    # ground_truth = [[1, 2], [3], [4, 5]]
    # predictions = [[2, 3, 4], [3, 1, 2], [5, 4, 1]]
    if __name__ == "__main__":
        # Simulated test case for evaluating retrieval using a Vector DB

        # Each list in ground_truth corresponds to a query and contains relevant doc IDs (ground truth)
        ground_truth = [
            ["doc_12", "doc_27"],      # relevant docs for query 1
            ["doc_5"],                 # relevant doc for query 2
            ["doc_101", "doc_103"]     # relevant docs for query 3
        ]

        # Each list in predictions is the ranked result returned from the Vector DB for that query
        predictions = [
            ["doc_27", "doc_3", "doc_99", "doc_12"],   # retrieved docs for query 1
            ["doc_5", "doc_1", "doc_9"],               # retrieved docs for query 2
            ["doc_103", "doc_55", "doc_101"]           # retrieved docs for query 3
        ]

    # Run evaluation with K = 3
    evaluate_retrieval(ground_truth, predictions, k=3)


    evaluate_retrieval(ground_truth, predictions)
