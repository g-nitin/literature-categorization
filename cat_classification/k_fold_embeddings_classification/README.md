## K-Fold Cross-Validation
The `k-fold_cross-val.py` performs multi-label classification of scientific papers using a k-fold cross-validation approach. It uses sentence embeddings and cosine similarity to categorize papers based on their abstracts. 

Key Components:

1. Data Loading: Loads existing paper data from a JSON file.
2. Embedding Generation: Uses SentenceTransformer to create embeddings for paper abstracts.
3. Categorization: Assigns categories to papers based on similarity to known papers.
4. Cross-Validation: Implements 5-fold cross-validation to assess model performance.
5. Evaluation: Calculates precision, recall, and F1-score for overall and per-category performance.

Assumptions:

1. Input data is in a specific JSON format with 'abstract' and 'category' fields.
2. Categories are treated as multi-label (papers can belong to multiple categories).
3. The similarity threshold (0.7) is appropriate for category assignment.
4. The chosen embedding model (all-MiniLM-L6-v2) is suitable for scientific text.

Outputs:

1. Console output: Overall and per-fold performance metrics, per-category metrics.
2. CSV file: Original paper data with added columns for predicted categories and cross-validation fold.

Limitations:

1. Relies on the quality and comprehensiveness of the existing labeled dataset.
2. Performance may vary with different similarity thresholds or embedding models.
3. Does not handle potential class imbalance issues.

Sample Console Output:
```shell
Found 140 existing papers
Performing 5-fold cross-validation...
Fold 1 - Precision: 0.2178, Recall: 0.7857, F1-score: 0.3411
Fold 2 - Precision: 0.1927, Recall: 0.7500, F1-score: 0.3066
Fold 3 - Precision: 0.1895, Recall: 0.6429, F1-score: 0.2927
Fold 4 - Precision: 0.2165, Recall: 0.7500, F1-score: 0.3360
Fold 5 - Precision: 0.2079, Recall: 0.7500, F1-score: 0.3256

Overall Results:
Precision: 0.2049 (±0.0118)
Recall: 0.7357 (±0.0484)
F1-score: 0.3204 (±0.0182)

Updated data with predictions saved to output/original_papers_with_cross_val_predictions.csv

Per-category Performance:
Unclassified: Precision=0.0000, Recall=0.0000, F1-score=0.0000
brain-inspired-planning: Precision=0.1000, Recall=0.6000, F1-score=0.1714
heuristics-optimization: Precision=0.0847, Recall=0.6250, F1-score=0.1493
interactive-planning: Precision=0.1625, Recall=0.6190, F1-score=0.2574
language-translation: Precision=0.1724, Recall=0.6522, F1-score=0.2727
model-construction: Precision=0.1429, Recall=0.7059, F1-score=0.2376
multiagent-planning: Precision=0.2222, Recall=0.4000, F1-score=0.2857
plan-generation: Precision=0.4182, Recall=0.8679, F1-score=0.5644
tool-integration: Precision=0.2593, Recall=0.8750, F1-score=0.4000
```