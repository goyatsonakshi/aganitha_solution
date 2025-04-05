# get_papers.py

import argparse
import pandas as pd
import csv
import sys
from pubmed_fetcher.fetcher import fetch_papers, parse_papers

def save_to_csv(papers, filename):
    """Save the list of papers to a CSV file."""
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False, quoting=csv.QUOTE_NONNUMERIC)

def main():
    """Main function to handle command-line arguments and execute the fetching process."""
    parser = argparse.ArgumentParser(description='Fetch research papers from PubMed.')
    parser.add_argument('query', type=str, help='Search query for PubMed')
    parser.add_argument('-f', '--file', type=str, help='Output filename for CSV')
    parser.add_argument('-d', '--debug', action='store_true', help='Print debug information')
    
    args = parser.parse_args()

    if args.debug:
        print(f"Debug: Fetching papers for query: {args.query}")

    try:
        xml_data = fetch_papers(args.query)
        papers = parse_papers(xml_data)

        if args.debug:
            print(f"Debug: Found {len(papers)} papers")

        if args.file:
            save_to_csv(papers, args.file)
            print(f"Results saved to {args.file}")
        else:
            for paper in papers:
                print(paper)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()