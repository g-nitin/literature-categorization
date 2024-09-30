# Formal Report: arXiv Paper Extraction Script Functionality

## 1. Introduction

This report outlines the functionality of the arXiv paper extraction script, designed to automate the process of retrieving, filtering, and storing relevant academic papers from the arXiv database. The script is implemented in Python and utilizes various components to ensure efficient and consistent operation.

## 2. Components and Functionality

### 2.1 CRON Job Scheduling

The script is designed to be run as a CRON job, allowing for automated, periodic execution. This ensures regular updates to the paper database without manual intervention. The CRON job can be configured to run at specified intervals (e.g., daily or weekly) using the following format in the crontab:

```
ARXIV_EXTRACTOR_BASE_DIR=/path/to/base/directory
0 2 * * * /usr/bin/python3 /path/to/arxiv_extractor.py
```

This example sets the script to run every day at 2:00 AM.

### 2.2 Configuration Management

The script utilizes a JSON configuration file (`config.json`) and environment variables for flexible setup across different environments. This approach allows for easy customization and portability. The configuration includes:

- Log directory
- Output directory
- Database file location

An environment variable (`ARXIV_EXTRACTOR_BASE_DIR`) can be used to specify the base directory, enhancing flexibility for different deployment scenarios.

### 2.3 arXiv API Interaction and Paper Scraping

The script interacts with the arXiv API using the `arxiv` Python package. It performs the following steps:

1. Executes predefined search queries targeting relevant categories and keywords.
2. Retrieves metadata for papers matching these queries.
3. Applies additional relevance filtering based on specified keywords.

This process ensures that only papers pertinent to the areas of interest (e.g., large language models and automated planning) are collected.

### 2.4 Database Management

A SQLite database is employed for persistent storage of paper metadata. The database functionality includes:

1. Initializing the database and creating necessary tables if they don't exist.
2. Checking for the existence of papers to avoid duplication.
3. Inserting new papers into the database.

This approach allows for efficient storage and retrieval of paper information across multiple script executions.

### 2.5 Deduplication Process

To prevent redundant entries, the script implements a deduplication process:

1. For each retrieved paper, it checks if the paper already exists in the database.
2. Only papers not present in the database are added to the list of new papers and inserted into the database.

This ensures that each run of the script only processes and reports genuinely new papers.

### 2.6 Output Generation

The script generates two types of output:

1. A CSV file containing details of newly found papers, created only when new papers are discovered.
2. Log files recording the script's execution details, including any errors or warnings.

These outputs facilitate easy review of new papers and monitoring of the script's performance.

## 3. Conclusion

The arXiv paper extraction script provides an automated, efficient solution for regularly updating a database of relevant academic papers. Its modular design, incorporating CRON job scheduling, flexible configuration, API interaction, database management, and deduplication processes, ensures reliable and consistent operation across various environments. This tool significantly streamlines the process of staying updated with the latest research in specified fields of interest.


Over the course of [TIME_PERIOD], our system identified [NUMBER] unique, relevant papers. We observed that [PERCENTAGE]% of the papers focused primarily on large language models, while [PERCENTAGE]% specifically addressed the intersection of language models and automated planning.
