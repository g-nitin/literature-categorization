# Categorization Based on Embeddings

The `categorization_embeddings.py` uses the existing dataset, process new papers from a CSV file, generate embeddings, and categorize them based on similarity to existing papers.

To further elaborate, the script does the following:
1. Loads existing papers from a JSON file.
2. Loads new papers from a CSV file.
3. Generates embeddings for both existing and new papers using the SentenceTransformer model.
4. Categorizes new papers based on their similarity to existing papers.
5. Saves the results to a new CSV file.

Two data files were used:
- `../abstract_adding/updated_papers_data.json`: The data file containing existing, categorized papers with their abstracts.
- `./copy_new_arxiv_papers_20240903_170512.csv`: The data file containing new papers to be categorized.

The output of the script is a csv file containing the same data and columns as the `./copy_new_arxiv_papers_20240903_170512.csv` file, with an additional column `category` containing the category of the paper based on the similarity to existing papers.
The output file is saved as `./categorized_papers_{threshold}.csv`, where `{threshold}` is the similarity threshold used for categorization.