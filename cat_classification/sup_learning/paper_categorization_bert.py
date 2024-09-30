import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import MultiLabelBinarizer
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from torch.utils.data import DataLoader, TensorDataset
import torch
import json
from collections import Counter
from imblearn.over_sampling import RandomOverSampler


"""
This script categorizes new papers based on their abstracts using BERT.
The model is trained on existing papers data and then used to predict categories for new papers.
The results are saved to a CSV file.
"""


# Load existing papers data
def load_existing_papers(file_path):
    print(f"Loading existing papers data from {file_path}...")
    with open(file_path, 'r') as f:
        papers_data = json.load(f)
    return papers_data


# Load new papers from CSV
def load_new_papers(file_path):
    print(f"Loading new papers data from {file_path}...")
    return pd.read_csv(file_path)


# Prepare data for BERT
def prepare_data(papers, tokenizer, max_length=512):
    # Extract texts and categories
    texts = [paper['title'] + " " + paper['abstract'] for paper in papers]  # Combine title and abstract

    # Handle single and multiple categories
    categories = [paper['category'] if isinstance(paper['category'], list) else [paper['category']] for paper in papers]

    # Tokenize texts
    encodings = tokenizer(texts, truncation=True, padding=True, max_length=max_length, return_tensors="pt")

    # Binarize labels
    mlb = MultiLabelBinarizer()
    labels = mlb.fit_transform(categories)

    return encodings, labels, mlb


def get_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device('cuda')
    # elif torch.backends.mps.is_available():
    #     return torch.device('mps')
    else:
        return torch.device('cpu')


# Train model
def train_model(encodings, labels, mlb, num_epochs=10, batch_size=8):
    # Convert to PyTorch tensors
    input_ids = encodings['input_ids']
    attention_mask = encodings['attention_mask']
    labels = torch.tensor(labels, dtype=torch.float)

    # Create dataset and dataloader
    dataset = TensorDataset(input_ids, attention_mask, labels)
    train_dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Initialize model
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased',
                                                          num_labels=len(mlb.classes_))

    # Set up optimizer
    optimizer = AdamW(model.parameters(), lr=2e-5)

    # Training loop
    device = get_device()
    print(f"Training on {device}...")
    model.to(device)
    model.train()

    for epoch in range(num_epochs):
        for batch in train_dataloader:
            batch = tuple(t.to(device) for t in batch)
            inputs = {'input_ids': batch[0], 'attention_mask': batch[1], 'labels': batch[2]}
            outputs = model(**inputs)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

        print(f"Epoch {epoch + 1}/{num_epochs} completed")

    return model, mlb


# Categorize new papers
def categorize_papers(model, tokenizer, mlb, new_papers, threshold=0.5):
    print("Categorizing new papers...")
    texts = new_papers['Title'] + " " + new_papers['Abstract']
    encodings = tokenizer(texts.tolist(), truncation=True, padding=True, max_length=512, return_tensors="pt")

    model.eval()
    with torch.no_grad():
        outputs = model(encodings['input_ids'], attention_mask=encodings['attention_mask'])

    predictions = torch.sigmoid(outputs.logits)
    predictions = (predictions > threshold).int().cpu().numpy()

    return mlb.inverse_transform(predictions)


# Main function
def main():
    # Load existing papers
    existing_papers = load_existing_papers('../../abstract_adding/updated_papers_data.json')

    # Initialize tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    # Prepare data
    encodings, labels, mlb = prepare_data(existing_papers, tokenizer)

    # Handle class imbalance
    ros = RandomOverSampler(random_state=13)  # Set random state for reproducibility

    # Resample data using RandomOverSampler
    flat_labels = [item for sublist in mlb.inverse_transform(labels) for item in sublist]

    # Convert labels to binary format
    resampled_encodings, resampled_labels = ros.fit_resample(
        pd.DataFrame({'input_ids': encodings['input_ids'].numpy().tolist(),
                      'attention_mask': encodings['attention_mask'].numpy().tolist()}),
        flat_labels
    )

    # Convert back to tensors
    resampled_input_ids = torch.tensor(resampled_encodings['input_ids'].tolist())
    resampled_attention_mask = torch.tensor(resampled_encodings['attention_mask'].tolist())
    resampled_labels = mlb.transform([[label] for label in resampled_labels])

    # Train model
    model, mlb = train_model({'input_ids': resampled_input_ids, 'attention_mask': resampled_attention_mask},
                             resampled_labels, mlb)

    # Load new papers
    new_papers = load_new_papers('../data/copy_new_arxiv_papers_20240903_170512.csv')

    # Categorize new papers
    new_categories = categorize_papers(model, tokenizer, mlb, new_papers)

    # Add categories to new papers dataframe
    new_papers['Categories'] = [', '.join(cats) if cats else 'Unclassified' for cats in new_categories]

    # Save results
    new_papers.to_csv('output/categorized_papers.csv', index=False)
    print("Categorization complete. Results saved to 'categorized_papers.csv'")


if __name__ == "__main__":
    main()
