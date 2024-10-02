## Embedding-Based Categorization

The `categorization_embeddings.py` uses the existing dataset, process new papers from a CSV file, generate embeddings, and categorizes them based on similarity to existing papers.

To further elaborate, the script does the following:
1. Loads existing papers from a JSON file.
2. Loads new papers from a CSV file.
3. Generates embeddings for both existing and new papers using the SentenceTransformer model.
4. Categorizes new papers based on their similarity to existing papers.
5. Tries different thresholds for similarity to categorize papers.
5. Saves the results for all attempted thresholds to a new CSV file.

Two data files were used:
- `../abstract_adding/updated_papers_data.json`: The data file containing existing, categorized papers with their abstracts.
- `./copy_new_arxiv_papers_20240903_170512.csv`: The data file containing new papers to be categorized.

The output of the script is a csv file containing the same data and columns as the `./copy_new_arxiv_papers_20240903_170512.csv` file, with an additional columns `category_{threshold}` containing the category of the paper based on the threshold.
The output file is saved as `output/categorized_papers_multiple_thresholds.csv`.

Potential Challenges:
* Choosing the right similarity threshold to balance between over-classification and under-classification.
* Handling papers that are on the borderline between categories.
* Dealing with new emerging categories that don't exist in the current taxonomy.

Sample Console Output:
```shell
Loading existing papers data at ../../abstract_adding/updated_papers_data.json
Found 140 existing papers
Found 140 existing abstracts
Found 140 existing categories
Loading new papers from ../data/copy_new_arxiv_papers_20240903_170512.csv
Found 48 new papers
Number of unclassified papers (threshold 0.5): 0
Number of unclassified papers (threshold 0.6): 4
Number of unclassified papers (threshold 0.7): 8
Number of unclassified papers (threshold 0.8): 26
Number of unclassified papers (threshold 0.9): 34
Categorization complete. Results saved to 'categorized_papers_multiple_thresholds.csv'
```