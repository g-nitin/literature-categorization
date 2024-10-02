## Paper Categorization Using BERT and SciBERT 

Both the BERT and SciBERT scripts follow a similar process for categorizing papers. Here's a step-by-step breakdown of what they're doing:

1. **Data Loading and Preparation**:
   - The script loads existing papers from a JSON file and new papers to be categorized from a CSV file.
   - It combines the title and abstract of each paper into a single text.
   - _The categories of existing papers are transformed into a multi-label format using scikit-learn's MultiLabelBinarizer._

2. **Tokenization**:
   - _The combined text (title + abstract) is tokenized using the appropriate tokenizer (BERT or SciBERT)._
   - This process converts the text into numerical representations that the model can understand.

3. **Model Initialization**:
   - If a saved model doesn't exist, the script initializes a pre-trained BERT or SciBERT model.
   - The model's classification layer is adjusted to match the number of categories in the dataset.

4. **Fine-tuning**:
   - The script is fine-tuning the model on the existing papers. This process adapts the pre-trained model to the specific categorization task.
   - _Fine-tuning involves:_
     * Feeding the tokenized papers through the model.
     * Comparing the model's predictions to the actual categories.
     * Adjusting the model's parameters to minimize the difference between predictions and actual categories.
   - This process is repeated for several epochs (10 by default) to improve the model's performance on the specific dataset.

5. **Class Imbalance Handling**:
   - The script uses RandomOverSampler to address potential class imbalance in the dataset.
   - _This technique replicates examples from minority classes to ensure all categories are well-represented during training._

6. **Model Saving**:
   - After fine-tuning, the model is saved to disk along with the MultiLabelBinarizer.
   - This allows to reuse the fine-tuned model later without having to retrain it.

7. **Categorization of New Papers**:
   - For new papers, the script:
     * Tokenizes the combined title and abstract.
     * Feeds this through the fine-tuned model.
     * Applies a threshold to the model's output to determine which categories to assign.

8. **Result Saving**:
   - The categorized papers are saved to a new CSV file with their assigned categories.

### Key Differences between BERT and SciBERT

The main difference between the BERT and SciBERT scripts is the base model they use:

- The BERT script uses the 'bert-base-uncased' model, which is pre-trained on a large corpus of general text.
- The SciBERT script uses 'allenai/scibert_scivocab_uncased', which is pre-trained on a large corpus of scientific papers.

SciBERT may perform better on scientific papers because its pre-training data is more closely aligned with the task. However, the general BERT model might perform well too, especially after fine-tuning on the specific dataset.

Both scripts are performing transfer learning: they start with a pre-trained model and then fine-tune it on the specific dataset and task. This approach often leads to better performance than training a model from scratch, especially when we have a limited amount of labeled data.

## Base Model Outputs
We evaluated the two pre-trained models on the multi-label classification task for scientific paper categorization. Both models were tested without any fine-tuning on our dataset.

Key observations:

* Overall performance: SciBERT outperformed BERT across all metrics, suggesting its scientific pre-training gives it an edge for our domain-specific task.
* Micro-average F1 scores: BERT achieved 0.08, while SciBERT reached 0.18, indicating SciBERT's superior overall performance.
* Class imbalance: Both models struggled with less represented categories (e.g., 'brain-inspired-planning', 'interactive-planning'), often failing to predict these classes entirely.
* Recall vs Precision: SciBERT showed higher recall (0.57 micro-avg) compared to precision (0.11 micro-avg), suggesting it's more likely to assign categories but with lower confidence.
* Best performing category: 'plan-generation' had the highest F1-score (0.53) with SciBERT, likely due to having the most examples in the dataset.

These results highlight the potential of using SciBERT as a starting point, but also underscore the need for fine-tuning, addressing class imbalance, and potentially collecting more data for underrepresented categories to improve overall classification performance.

Console Output:
```shell
Classification Report for bert-base-uncased:
                         precision    recall  f1-score   support

brain-inspired-planning       0.00      0.00      0.00         1
heuristics-optimization       0.04      1.00      0.07         1
   interactive-planning       0.00      0.00      0.00         6
   language-translation       0.00      0.00      0.00         4
     model-construction       0.07      1.00      0.13         2
    multiagent-planning       0.08      1.00      0.15         1
        plan-generation       0.00      0.00      0.00        10
       tool-integration       0.00      0.00      0.00         3

              micro avg       0.06      0.14      0.08        28
              macro avg       0.02      0.38      0.05        28
           weighted avg       0.01      0.14      0.02        28
            samples avg       0.05      0.14      0.08        28

Classification Report for allenai/scibert_scivocab_uncased:
                         precision    recall  f1-score   support

brain-inspired-planning       0.00      0.00      0.00         1
heuristics-optimization       0.04      1.00      0.07         1
   interactive-planning       0.00      0.00      0.00         6
   language-translation       0.14      0.75      0.23         4
     model-construction       0.04      0.50      0.07         2
    multiagent-planning       0.04      1.00      0.07         1
        plan-generation       0.36      1.00      0.53        10
       tool-integration       0.00      0.00      0.00         3

              micro avg       0.11      0.57      0.18        28
              macro avg       0.08      0.53      0.12        28
           weighted avg       0.15      0.57      0.23        28
            samples avg       0.11      0.57      0.18        28
```