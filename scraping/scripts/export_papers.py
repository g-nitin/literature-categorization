import csv
import os
import sqlite3
from datetime import datetime


def export_all_papers():
    """Export all papers from the database to a CSV file"""
    conn = sqlite3.connect("../db/arxiv_papers.db")
    c = conn.cursor()

    # Get all papers from the database
    c.execute("SELECT * FROM papers ORDER BY published_date DESC")
    papers = c.fetchall()

    if papers:
        csv_filename = os.path.join("../out", f"all_arxiv_papers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

        try:
            with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Title', 'Authors', 'Published Date', 'Abstract', 'URL', 'Categories'])

                for paper in papers:
                    writer.writerow(paper)

            print(f"Exported {len(papers)} papers to {csv_filename}")
        except Exception as e:
            print(f"Error exporting papers: {str(e)}")
    else:
        print("No papers found in the database.")

    conn.close()


if __name__ == "__main__":
    export_all_papers()
