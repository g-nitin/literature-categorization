# Category Classification

## Embedding
This script in this folder does the following:
1. Loads existing papers from a JSON file and loads new papers from a CSV file.
2. **Generates embeddings** for both existing and new papers using the **SentenceTransformer model**.
3. The script uses the 'all-MiniLM-L6-v2' model for generating embeddings.
4. **Categorizes new papers based on their similarity** to existing papers.
5. Saves the results to a new CSV file.

Potential Challenges:
1. Choosing the right similarity threshold to balance between over-classification and under-classification.
2. Handling papers that are on the borderline between categories.
3. Dealing with new emerging categories that don't exist in the current taxonomy.

## Supervised Learning: OneVsRestClassifier with LinearSVC
This script in this folder does the following:
1. Loads existing papers from a JSON file and loads new papers from a CSV file.
2. Text Preprocessing: removes stopwords and non-alphanumeric characters.
3. TF-IDF Vectorization: convert the text into numerical features.
4. The OneVsRestClassifier allows for **multi-label classification**, meaning a paper can be assigned to multiple categories if appropriate.
5. Includes an evaluation step, printing a **classification report** that shows **precision**, **recall**, and **F1-score** for each category.

## Supervised Learning: BERT
1. This script in this folder does the following:
2. Using a pre-trained BERT model, which is state-of-the-art for many NLP tasks.
3. Using both the **title and abstract for classification**, which provides more context for the model.
4. Using **RandomOverSampler** to address the class imbalance issue. This should help with categories that have very few examples.
5. Using a threshold (default 0.5) to determine whether to assign a category.
6. The script still supports multi-label classification, allowing papers to be assigned to multiple categories.

## Supervised Learning: SciBERT
1. Now using SciBERT (allenai/scibert_scivocab_uncased) instead of the standard BERT model. SciBERT is pre-trained on a large corpus of scientific text and should perform better on scientific papers.
2. 