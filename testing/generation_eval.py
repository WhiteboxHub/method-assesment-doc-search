# generation_eval.py

import evaluate

def evaluate_generation(preds, refs):
    # Load metrics
    bleu = evaluate.load("bleu")
    rouge = evaluate.load("rouge")
    meteor = evaluate.load("meteor")

    # Compute metrics
    bleu_score = bleu.compute(predictions=preds, references=[[ref] for ref in refs])
    rouge_score = rouge.compute(predictions=preds, references=refs)
    meteor_score = meteor.compute(predictions=preds, references=refs)

    print(f"BLEU: {bleu_score['bleu']:.4f}")
    print(f"ROUGE-L: {rouge_score['rougeL']:.4f}")
    print(f"METEOR: {meteor_score['meteor']:.4f}")

# Example usage
if __name__ == "__main__":
    references = ["The cat sat on the mat.", "A man is walking a dog."]
    predictions = ["The cat is sitting on the mat.", "A person walks the dog."]

    evaluate_generation(predictions, references)
