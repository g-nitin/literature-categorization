import arxiv
import csv
from datetime import datetime
import re
import logging
import os
import sqlite3
import json


# Load configuration
def load_config():
    """Load configuration from config.json file"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)


def is_relevant(paper, must_include, optional_keywords):
    """Check if the paper is relevant based on its title and abstract"""
    text = (paper.title + " " + paper.summary).lower()
    return any(keyword.lower() in text for keyword in must_include) and \
        any(keyword.lower() in text for keyword in optional_keywords)


def init_db():
    """Initialize the SQLite database"""
    print(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS papers
                 (id TEXT PRIMARY KEY, title TEXT, authors TEXT, 
                  published_date TEXT, absEtract TEXT, url TEXT, categories TEXT)''')
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
        csv_filename = os.path.join(OUTPUT_DIR, f"new_arxiv_papers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

        try:
            with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Title', 'Authors', 'Published Date', 'Abstract', 'URL', 'Categories'])

                for paper in new_papers:
                    writer.writerow([
                        paper.title,
                        ', '.join([author.name for author in paper.authors]),
                        paper.published.strftime('%Y-%m-%d'),
                        re.sub(r'\s+', ' ', paper.summary).strip(),
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

    config = load_config()

    # Use environment variable if set, otherwise use config file
    BASE_DIR: str = os.environ.get('ARXIV_EXTRACTOR_BASE_DIR', os.path.dirname(os.path.abspath(__file__)))

    # Setup paths
    LOG_DIR = os.path.join(BASE_DIR, config['log_dir'])
    OUTPUT_DIR = os.path.join(BASE_DIR, config['output_dir'])
    DB_DIR = os.path.join(BASE_DIR, config['db_dir'])
    DB_FILE = os.path.join(DB_DIR, config['db_file'])

    # Create necessary directories
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(DB_DIR, exist_ok=True)

    # Setup logging
    logging.basicConfig(
        filename=os.path.join(LOG_DIR, f"arxiv_extractor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Write the paths to the log file
    logging.info(f"BASE_DIR: {BASE_DIR}")
    logging.info(f"LOG_DIR: {LOG_DIR}")
    logging.info(f"OUTPUT_DIR: {OUTPUT_DIR}")
    logging.info(f"DB_DIR: {DB_DIR}")
    logging.info(f"DB_FILE: {DB_FILE}")

    main()
