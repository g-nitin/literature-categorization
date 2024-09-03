import arxiv
import csv
from datetime import datetime
import re


def is_relevant(paper, must_include, optional_keywords):
    """Check if the paper is relevant based on its title and abstract"""
    text = (paper.title + " " + paper.summary).lower()
    return any(keyword.lower() in text for keyword in must_include) and \
           any(keyword.lower() in text for keyword in optional_keywords)


def deduplicate(papers):
    """Remove duplicate papers based on their IDs"""
    seen = set()
    return [paper for paper in papers if not (paper.entry_id in seen or seen.add(paper.entry_id))]


# Define the main keywords we're interested in
must_include = ["large language models", "LLMs", "GPT", "BERT", "transformers"]
optional_keywords = ["automated planning", "symbolic planning", "neurosymbolic planning",
                     "task planning", "AI planning", "PDDL", "constraint-based planning",
                     "hierarchical task planning", "multi-agent planning", "robot planning"]


# Define more specific queries
queries = [
    'cat:cs.AI AND ("large language models" OR "LLMs" OR "GPT" OR "BERT" OR transformers)',
    'cat:cs.AI AND ("automated planning" OR "symbolic planning" OR "neurosymbolic planning" OR "task planning" OR "AI planning")',
    'cat:cs.AI AND ("neural-symbolic" OR "neurosymbolic") AND planning',
    'cat:cs.AI AND ("large language models" OR "LLMs" OR "GPT" OR "BERT" OR transformers) AND planning',
    'cat:cs.AI AND ("large language models" OR "LLMs" OR "GPT" OR "BERT" OR transformers) AND PDDL'
]

client = arxiv.Client()
all_papers = []

# Fetch papers for each query
for query in queries:
    print(f"Executing query: {query}")
    search = arxiv.Search(
        query=query,
        max_results=200,
        sort_by=arxiv.SortCriterion.Relevance
    )
    results = list(client.results(search))
    print(f"Found {len(results)} papers.\n")
    all_papers.extend(results)

print(f"Total number of papers found: {len(all_papers)}")

# Deduplicate papers
unique_papers = deduplicate(all_papers)
print(f"Number of unique papers: {len(unique_papers)}")

# Filter papers
relevant_papers = [paper for paper in unique_papers if is_relevant(paper, must_include, optional_keywords)]
print(f"Number of relevant papers: {len(relevant_papers)}")

# Sort papers by date (most recent first)
relevant_papers.sort(key=lambda x: x.published, reverse=True)

# Write to CSV
csv_filename = f"out/arxiv_papers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Authors', 'Published Date', 'Abstract', 'URL', 'Categories'])

    for paper in relevant_papers:
        writer.writerow([
            f"{paper.title}",
            ', '.join([author.name for author in paper.authors]),
            paper.published.strftime('%Y-%m-%d'),
            re.sub('\s+', ' ', paper.summary).strip(),
            paper.entry_id,
            ', '.join(paper.categories)
        ])

print(f"CSV file '{csv_filename}' has been created with {len(relevant_papers)} relevant papers.")
