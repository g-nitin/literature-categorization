import arxiv
import csv
from datetime import datetime
import re
import logging
import os
import sqlite3

# Setup logging
log_dir = "/path/to/your/log/directory"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=f"{log_dir}/arxiv_extractor_{datetime.now().strftime('%Y%m%d')}.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def is_relevant(paper, must_include, optional_keywords):
    """Check if the paper is relevant based on its title and abstract"""
    text = (paper.title + " " + paper.summary).lower()
    return any(keyword.lower() in text for keyword in must_include) and \
           any(keyword.lower() in text for keyword in optional_keywords)

def init_db():
    """Initialize the SQLite database"""
    conn = sqlite3.connect('/path/to/your/arxiv_papers.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS papers
                 (id TEXT PRIMARY KEY, title TEXT, authors TEXT, 
                  published_date TEXT, abstract TEXT, url TEXT, categories TEXT)''')
    conn.commit()
    return conn

def paper_exists(conn, paper_id):
    """Check if a paper already exists in the database"""
    c = conn.cursor()
    c.execute("SELECT 1 FROM papers WHERE id = ?", (paper_id,))
    return c.fetchone() is not None

def insert_paper(conn, paper):
    """Insert a new paper into the database"""
    c = conn.cursor()
    c.execute('''INSERT INTO papers (id, title, authors, published_date, abstract, url, categories)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (paper.entry_id, paper.title, ', '.join([author.name for author in paper.authors]),
               paper.published.strftime('%Y-%m-%d'), paper.summary, paper.entry_id, ', '.join(paper.categories)))
    conn.commit()

# Define the main keywords we're interested in
must_include = ["large language models", "LLMs", "GPT", "BERT", "transformers"]
optional_keywords = ["automated planning", "symbolic planning", "neurosymbolic planning", 
                     "task planning", "AI planning", "PDDL", "constraint-based planning",
                     "hierarchical task planning", "multi-agent planning", "robot planning"]

# Define queries
queries = [
    'cat:cs.AI AND ("large language models" OR "LLMs" OR "GPT" OR "BERT" OR transformers)',
    'cat:cs.AI AND ("automated planning" OR "symbolic planning" OR "neurosymbolic planning" OR "task planning" OR "AI planning")',
    'cat:cs.AI AND ("neural-symbolic" OR "neurosymbolic") AND planning',
    'cat:cs.AI AND ("large language models" OR "LLMs" OR "GPT" OR "BERT" OR transformers) AND planning',
    'cat:cs.AI AND ("large language models" OR "LLMs" OR "GPT" OR "BERT" OR transformers) AND PDDL'
]

def main():
    logging.info("Starting arXiv paper extraction")
    
    client = arxiv.Client()
    all_papers = []

    # Fetch papers for each query
    for query in queries:
        logging.info(f"Executing query: {query}")
        try:
            search = arxiv.Search(
                query=query,
                max_results=200,
                sort_by=arxiv.SortCriterion.Relevance
            )
            all_papers.extend(list(client.results(search)))
        except Exception as e:
            logging.error(f"Error executing query '{query}': {str(e)}")

    # Initialize database connection
    conn = init_db()

    # Filter papers and check for duplicates
    new_papers = []
    for paper in all_papers:
        if is_relevant(paper, must_include, optional_keywords) and not paper_exists(conn, paper.entry_id):
            new_papers.append(paper)
            insert_paper(conn, paper)

    # Sort new papers by date (most recent first)
    new_papers.sort(key=lambda x: x.published, reverse=True)

    # Write new papers to CSV
    if new_papers:
        output_dir = "/path/to/your/output/directory"
        os.makedirs(output_dir, exist_ok=True)
        csv_filename = f"{output_dir}/new_arxiv_papers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Title', 'Authors', 'Published Date', 'Abstract', 'URL', 'Categories'])

                for paper in new_papers:
                    writer.writerow([
                        paper.title,
                        ', '.join([author.name for author in paper.authors]),
                        paper.published.strftime('%Y-%m-%d'),
                        re.sub('\s+', ' ', paper.summary).strip(),
                        paper.entry_id,
                        ', '.join(paper.categories)
                    ])
            
            logging.info(f"CSV file '{csv_filename}' has been created with {len(new_papers)} new relevant papers.")
        except Exception as e:
            logging.error(f"Error writing to CSV file: {str(e)}")
    else:
        logging.info("No new papers found in this run.")

    # Close database connection
    conn.close()

if __name__ == "__main__":
    main()
