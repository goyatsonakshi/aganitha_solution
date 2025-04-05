# pubmed_fetcher/fetcher.py

import requests
import xml.etree.ElementTree as ET

def fetch_papers(query):
    """Fetch papers from PubMed based on the query."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        'db': 'pubmed',
        'term': query,
        'retmode': 'xml',
        'retmax': 100  # Adjust as needed
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raise an error for bad responses
    return response.text

def parse_papers(xml_data):
    """Parse the XML data returned from PubMed and extract relevant information."""
    root = ET.fromstring(xml_data)
    papers = []

    for article in root.findall('.//PubmedArticle'):
        pubmed_id = article.find('.//PMID').text
        title = article.find('.//ArticleTitle').text
        pub_date = article.find('.//PubDate')
        publication_date = (
            f"{pub_date.find('Year').text}-{pub_date.find('Month').text.zfill(2)}-{pub_date.find('Day').text.zfill(2)}"
            if pub_date is not None else "N/A"
        )

        authors = article.findall('.//Author')
        non_academic_authors = []
        company_affiliations = []
        corresponding_author_email = None

        for author in authors:
            last_name = author.find('LastName').text if author.find('LastName') is not None else ''
            fore_name = author.find('ForeName').text if author.find('ForeName') is not None else ''
            author_name = f"{fore_name} {last_name}".strip()

            affiliations = author.findall('.//Affiliation')
            for affiliation in affiliations:
                affiliation_text = affiliation.text
                if affiliation_text and ("pharmaceutical" in affiliation_text.lower() or "biotech" in affiliation_text.lower()):
                    non_academic_authors.append(author_name)
                    company_affiliations.append(affiliation_text)

            if author.find('.//Email') is not None:
                corresponding_author_email = author.find('.//Email').text

        papers.append({
            'PubmedID': pubmed_id,
            'Title': title,
            'Publication Date': publication_date,
            'Non-academicAuthor(s)': ', '.join(non_academic_authors) if non_academic_authors else 'N/A',
            'CompanyAffiliation(s)': ', '.join(company_affiliations) if company_affiliations else 'N/A',
            'Corresponding Author Email': corresponding_author_email if corresponding_author_email else 'N/A'
        })

    return papers