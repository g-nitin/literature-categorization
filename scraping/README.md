# Scraping Papers

## arxiv_extractor_db
- Two-tier Keyword System: Script has `must_include` keywords (related to language models) and `optional_keywords` (related to planning).
  - A paper must contain at least one keyword from each list to be considered relevant.
  - The `is_relevant()` function now checks for the presence of keywords from both lists.
- Increased Results per Query: Script sets `max_results` to 200 for each query to capture more papers.
- SQLite Database: The script adds a SQLite database to keep track of papers already processed.
  - The `init_db()` function creates the database and table if they don't exist.
  - The paper_exists() function checks if a paper is already in the database.
  - The insert_paper() function adds new papers to the database.
  - In the main loop, the script checks each paper against the database before adding it to the list of new papers (deduplication process).
- CSV Output: The script only creates a CSV file if there are new papers to report.
- Logging: The script logs the number of new papers found and the number of papers added to the database.
- Configuration File Extension:
  - Using absolute paths can make the script less portable and harder to share. A good workaround is to use relative paths with environment variables or a configuration file. This approach allows for flexibility when running the script manually or as a CRON job, while also making it easy to share and deploy on different systems.
  - The script now uses a configuration file to set the output directory and the database file path.
  - When sharing:
    - Share both the arxiv_extractor.py and config.json files.
    - The recipient can place these files in any directory and run the script from there.
    - If they want to use a different base directory, they can set the ARXIV_EXTRACTOR_BASE_DIR environment variable.
- Requirements:
  - Need to have the `config.json` file in the same directory as the script.
  - Also, need to have an empty `db` folder.


## Scraping Test
This directory contains a copy of the scraping directory and was made to test the original scraping.
One issue was that the original code did not access some pages (check logs) and wanted to check whether rerunning would result in improvements.
However, testing was abandoned.