# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nico Marr

from typing import Optional, List, Dict, Any
import httpx
import xml.etree.ElementTree as ET
from time import sleep


def search_pubmed(query: str, retmax: int = 1000) -> Optional[Dict[str, Any]]:
    """Perform a PubMed search using E-utilities.
    
    Args:
        query: PubMed search query with field tags (MeSH [mh], title/abstract [tiab], title [ti], 
            date published [dp], language [la]), filters (humans[mh], English[la]), 
            and boolean operators (AND, OR, NOT). For recent articles use: ("2020"[dp] : "3000"[dp]) 
            or ("last 5 years"[dp]).
        retmax: Maximum number of results to return.
        
    Returns:
        dict with:
            - 'count': total number of matching articles in PubMed
            - 'retmax': maximum number of IDs requested
            - 'retstart': starting index for retrieval (pagination)
            - 'idlist': list of returned PubMed IDs (length may be less than retmax)
            - 'translationset': PubMed's translation of search terms
            - 'querytranslation': final translated query string
        None if HTTP request fails.

    Examples:
    >>> pubmed_response = search_pubmed('(ABO[ti] AND blood[tiab]) OR "ABO blood group"[tiab] OR "ABO system"[tiab] OR "ABO antigen"[ti]')
    >>> pubmed_ids = pubmed_response.get('idlist', [])
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {'db': 'pubmed', 'term': query, 'retmode': 'json', 'retmax': retmax}
    try:
        response = httpx.get(base_url, params=params, timeout=30.0)
        response.raise_for_status()
        return response.json().get('esearchresult', {})
    except httpx.HTTPError as e:
        print(f"Error occurred: {e}")
        return None


def search_gene(query: str, retmax: int = 100) -> Optional[Dict[str, Any]]:
    """Search NCBI Gene database using E-utilities ESearch.
    
    Args:
        query: Gene search query with field tags and boolean operators. Examples:
            - Simple: 'JUN[sym] AND "Homo sapiens"[Organism]'
            - Complex: '(BRCA1[sym] OR BRCA2[sym]) AND human[Organism]'
            Field tags: [sym] (gene symbol), [Organism] (organism/species name),
            [gene] (gene name), [chr] (chromosome), [map] (map location).
        retmax: Maximum number of Gene IDs to return (default: 100, max: 10000).
            
    Returns:
        dict with:
            - 'count': total number of matching genes
            - 'idlist': list of NCBI Gene database IDs (integers as strings)
            - 'retmax': maximum number requested
            - 'retstart': starting index for pagination
            - 'translationset': contains information about how PubMed/NCBI translated search terms
            - 'translationstack': shows step-by-step processing of the query, including how boolean operators were applied and how terms were combined
            - 'querytranslation': PubMed's interpretation of the query
        Returns None if HTTP request fails.
        
    Note:
        NCBI Gene database contains records for genes from all organisms. Use [Organism]
        field tag to restrict to specific species. Rate limit: 3 requests/second 
        without API key, 10 requests/second with API key.
        
    Examples:
        >>> response = search_gene('JUN[sym] AND "Homo sapiens"[Organism]')
        >>> gene_ids = response['idlist']  # Returns ['3725']
        >>> response['count']  # Total matches found
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {'db': 'gene', 'term': query, 'retmode': 'json', 'retmax': retmax}
    try:
        response = httpx.get(base_url, params=params, timeout=30.0)
        response.raise_for_status()
        return response.json().get('esearchresult', {})
    except httpx.HTTPError as e:
        print(f"Error occurred: {e}")
        return None


def fetch_pubmed_data(
    pmids: List[str],
    retmax_per_request: int = 200,
    rate_limit_delay: float = 0.34
) -> List[Dict[str, Any]]:
    """Fetch titles, abstracts and other metadata from PubMed using EFetch.

    This function retrieves article metadata including titles, abstracts,
    authors, and publication details for a list of PubMed IDs. The function
    handles batching automatically and respects NCBI rate limits (3 requests
    per second without API key).

    Args:
        pmids: List of PubMed IDs (as strings) to retrieve, e.g., ["36003377", "38048195", "33497357"] or ['36003377', '38048195', '33497357'], not "['36003377', '38048195', '33497357']"
        retmax_per_request: Maximum number of PMIDs to fetch in a single
            request. NCBI recommends batching large requests. Defaults to 200.
        rate_limit_delay: Delay in seconds between requests to respect NCBI
            rate limits (0.34s ≈ 3 requests/second). Defaults to 0.34.

    Returns:
        A list of dictionaries, where each dictionary contains metadata for
        one PubMed article with the following keys:
        - 'pmid': PubMed ID
        - 'title': Article title
        - 'abstract': Article abstract text (or empty string if unavailable)
        - 'authors': List of author names
        - 'journal': Journal name
        - 'pub_date': Publication date (year)
        - 'doi': DOI (if available)

    Raises:
        httpx.HTTPError: If the HTTP request fails.

    Example:
        >>> pmids = ['19393038', '30242208', '29453458']
        >>> articles = fetch_pubmed_data(pmids)
        >>> print(f"Retrieved {len(articles)} articles")
        Retrieved 3 articles
        >>> print(articles[0]['title'][:50])
        Genome-wide association study identifies...
        
        >>> # Handle large batches automatically
        >>> large_pmid_list = [str(i) for i in range(1000, 1500)]
        >>> articles = fetch_pubmed_data(large_pmid_list, retmax_per_request=100)
        >>> print(f"Retrieved {len(articles)} articles in batches")
        Retrieved 500 articles in batches
    """
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    all_articles = []
    
    # Handle input format
    if isinstance(pmids, str):
        pmids = pmids.strip('"').strip("'")
        if pmids.startswith('[') and pmids.endswith(']'):
            import ast
            pmids = ast.literal_eval(pmids)
        elif ',' in pmids: pmids = [p.strip() for p in pmids.split(',')]
        else: pmids = [pmids]

    # "["36003377", "38048195", "33497357"]" → strips outer quotes, then parses list
    #  '["36003377", "38048195", "33497357"]' → same
    # "36003377, 38048195", 33497357" → splits on comma
    # "36003377" → single PMID as list
    
    # Validate PMID format
    assert isinstance(pmids, list), f"pmids must be a list, got {type(pmids)}"
    assert all(isinstance(p, str) for p in pmids), "All PMIDs must be strings"
    assert all(p.isdigit() for p in pmids), f"PMIDs must be numeric strings: {pmids[:3]}"
    assert all(len(p) >= 1 for p in pmids), f"Empty PMID found: {pmids[:3]}"

    # Process PMIDs in batches
    for i in range(0, len(pmids), retmax_per_request):
        batch = pmids[i:i + retmax_per_request]
        batch_ids = ','.join(batch)
        
        params = {
            'db': 'pubmed',
            'id': batch_ids,
            'retmode': 'xml'
        }
        
        try:
            response = httpx.get(BASE_URL, params=params, timeout=30.0)
            response.raise_for_status()
            
            # Parse XML response
            root = ET.fromstring(response.content)
            
            # Extract article information
            for article in root.findall('.//PubmedArticle'):
                article_data = {}
                
                # PMID
                pmid_elem = article.find('.//PMID')
                article_data['pmid'] = pmid_elem.text if pmid_elem is not None else ''
                
                # Title (use itertext to capture inline markup like <i>, <sub>, <sup>)
                title_elem = article.find('.//ArticleTitle')
                article_data['title'] = ''.join(title_elem.itertext()) if title_elem is not None else ''
                
                # Abstract (may have multiple parts)
                abstract_texts = article.findall('.//AbstractText')
                if abstract_texts:
                    abstract_parts = []
                    for abs_text in abstract_texts:
                        label = abs_text.get('Label', '')
                        text = ''.join(abs_text.itertext()) or ''
                        if label:
                            abstract_parts.append(f"{label}: {text}")
                        else:
                            abstract_parts.append(text)
                    article_data['abstract'] = ' '.join(abstract_parts)
                else:
                    article_data['abstract'] = ''
                
                # Authors
                authors = []
                for author in article.findall('.//Author'):
                    lastname = author.find('LastName')
                    forename = author.find('ForeName')
                    if lastname is not None and forename is not None:
                        authors.append(f"{forename.text} {lastname.text}")
                    elif lastname is not None:
                        authors.append(lastname.text)
                article_data['authors'] = authors
                
                # Journal
                journal_elem = article.find('.//Journal/Title')
                article_data['journal'] = journal_elem.text if journal_elem is not None else ''
                
                # Publication date
                pub_year = article.find('.//PubDate/Year')
                article_data['pub_date'] = pub_year.text if pub_year is not None else ''
                
                # DOI
                doi_elem = article.find('.//ArticleId[@IdType="doi"]')
                article_data['doi'] = doi_elem.text if doi_elem is not None else ''
                
                all_articles.append(article_data)
            
            # Rate limiting: sleep between requests
            if i + retmax_per_request < len(pmids):
                sleep(rate_limit_delay)
                
        except httpx.HTTPError as e:
            print(f"Error fetching batch starting at index {i}: {e}")
            continue
    
    return all_articles