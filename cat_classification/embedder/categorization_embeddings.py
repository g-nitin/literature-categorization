import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json


# Load existing papers data
def load_existing_papers(file_path):
    """
    Load existing papers data from a JSON file
    :param file_path: Path to the JSON file. Should contain the abstract field.
    Sample value:
    {
        {
            "title": "Plansformer: Generating symbolic plans using transformers",
            "category": "plan-generation",
            "link": "https://arxiv.org/abs/2212.08681",
            "authors": "Pallagani, Vishal and Muppasani, Bharath and Murugesan, Keerthiram and Rossi, Francesca and Horesh, Lior and Srivastava, Biplav and Fabiano, Francesco and Loreggia, Andrea",
            "year": "2022",
            "abstract": "Large Language Models (LLMs) have been the subject of active research,\nsignificantly advancing the field of Natural Language Processing (NLP). From\nBERT to BLOOM, LLMs have surpassed state-of-the-art results in various natural\nlanguage tasks such as question answering, summarization, and text generation.\nMany ongoing efforts focus on understanding LLMs' capabilities, including their\nknowledge of the world, syntax, and semantics. However, extending the textual\nprowess of LLMs to symbolic reasoning has been slow and predominantly focused\non tackling problems related to the mathematical field. In this paper, we\nexplore the use of LLMs for automated planning - a branch of AI concerned with\nthe realization of action sequences (plans) to achieve a goal, typically\nexecuted by intelligent agents, autonomous robots, and unmanned vehicles. We\nintroduce Plansformer; an LLM fine-tuned on planning problems and capable of\ngenerating plans with favorable behavior in terms of correctness and length\nwith reduced knowledge-engineering efforts. We also demonstrate the\nadaptability of Plansformer in solving different planning domains with varying\ncomplexities, owing to the transfer learning abilities of LLMs. For one\nconfiguration of Plansformer, we achieve ~97% valid plans, out of which ~95%\nare optimal for Towers of Hanoi - a puzzle-solving domain."
        },
    }
    :return: List of dictionaries containing paper data
    """
    print(f"Loading existing papers data at {file_path}")
    with open(file_path, 'r') as f:
        papers_data = json.load(f)
    return papers_data


# Load new papers from CSV
def load_new_papers(file_path):
    """
    Load new papers from a CSV file
    :param file_path: Path to the CSV file.
    :return: DataFrame containing new papers data
    """
    print(f"Loading new papers from {file_path}")
    return pd.read_csv(file_path)


# Generate embeddings
def generate_embeddings(texts):
    """
    Generate embeddings for a list of texts
    :param texts: List of texts
    :return: Numpy array of embeddings
    """
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model.encode(texts)


# Calculate similarity and assign categories
def categorize_papers(new_embeddings, existing_embeddings, existing_categories, threshold):
    """
    Calculate cosine similarity between new and existing embeddings and assign categories to new papers.
    Note that multiple categories can be assigned to a paper.
    :param new_embeddings: Numpy array of embeddings for new papers
    :param existing_embeddings: Numpy array of embeddings for existing papers
    :param existing_categories: List of categories for existing papers
    :param threshold: Threshold for similarity
    :return: List of categories for new papers. Contains 'Unclassified' if no category is assigned
    """
    similarities = cosine_similarity(new_embeddings, existing_embeddings)
    categories = []
    for sim in similarities:
        paper_categories = set()
        for i, s in enumerate(sim):
            if s > threshold:
                paper_categories.update(existing_categories[i])
        categories.append(list(paper_categories) if paper_categories else ['Unclassified'])
    return categories


# Main function
def main():
    # Load existing papers
    existing_papers = load_existing_papers('../../abstract_adding/updated_papers_data.json')
    print(f"Found {len(existing_papers)} existing papers")

    # Extract abstracts and categories from existing papers
    existing_abstracts = [paper['abstract'] for paper in existing_papers
                          if paper['abstract'] != "Abstract not found"]
    print(f"Found {len(existing_abstracts)} existing abstracts")

    existing_categories = [paper['category'] if isinstance(paper['category'], list) else [paper['category']] for paper
                           in existing_papers]
    print(f"Found {len(existing_categories)} existing categories")

    # Generate embeddings for existing papers
    existing_embeddings = generate_embeddings(existing_abstracts)

    # Load new papers
    new_papers = load_new_papers('../data/copy_new_arxiv_papers_20240903_170512.csv')
    print(f"Found {len(new_papers)} new papers")

    # Generate embeddings for new papers
    new_embeddings = generate_embeddings(new_papers['Abstract'].tolist())

    # Categorize new papers
    threshold = 0.7
    new_categories = categorize_papers(new_embeddings, existing_embeddings, existing_categories, threshold)

    # Add categories to new papers dataframe
    new_papers['Categories'] = new_categories
    print(f"Number of unclassified papers: {new_categories.count(['Unclassified'])}")

    # Save results
    out_file_name = f"categorized_papers_{threshold}.csv"
    new_papers.to_csv(out_file_name, index=False)
    print(f"Categorization complete. Results saved to '{out_file_name}'")


if __name__ == "__main__":
    main()
