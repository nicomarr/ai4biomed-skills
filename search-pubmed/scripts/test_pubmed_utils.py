# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nico Marr

"""Tests for pubmed_utils module."""

import pytest
from pubmed_utils import search_pubmed, search_gene, fetch_pubmed_data


# --- search_pubmed ---

def test_search_pubmed_returns_expected_keys():
    result = search_pubmed("CRISPR[ti]", retmax=3)
    assert result is not None
    assert set(result.keys()) >= {"count", "retmax", "retstart", "idlist", "querytranslation"}


def test_search_pubmed_respects_retmax():
    result = search_pubmed("cancer", retmax=5)
    assert len(result["idlist"]) <= 5


def test_search_pubmed_returns_numeric_pmids():
    result = search_pubmed("asthma[mh]", retmax=3)
    assert all(pmid.isdigit() for pmid in result["idlist"])


# --- search_gene ---

def test_search_gene_known_symbols():
    """JUN, ABO, and CLOCK should map to Gene IDs 3725, 28, 9575."""
    result = search_gene('(JUN[sym] OR CLOCK[sym] OR ABO[sym]) AND "Homo sapiens"[Organism]')
    assert result is not None
    assert set(result["idlist"]) == {"3725", "28", "9575"}


def test_search_gene_returns_expected_keys():
    result = search_gene('TP53[sym] AND "Homo sapiens"[Organism]')
    assert set(result.keys()) >= {"count", "retmax", "retstart", "idlist", "querytranslation"}


# --- fetch_pubmed_data ---

KNOWN_PMIDS = ["36003377", "38048195", "33497357"]
EXPECTED_TITLES = {
    "36003377": "Human leukocyte antigen class II gene diversity tunes antibody repertoires to common pathogens.",
    "38048195": "Pre-Covid-19, SARS-CoV-2-Negative Multisystem Inflammatory Syndrome in Children.",
    "33497357": "Distinct antibody repertoires against endemic human coronaviruses in children and adults.",
}


def test_fetch_pubmed_data_returns_all_articles():
    articles = fetch_pubmed_data(KNOWN_PMIDS)
    assert len(articles) == len(KNOWN_PMIDS)


def test_fetch_pubmed_data_article_keys():
    articles = fetch_pubmed_data(KNOWN_PMIDS[:1])
    expected_keys = {"pmid", "title", "abstract", "authors", "journal", "pub_date", "doi"}
    assert set(articles[0].keys()) == expected_keys


def test_fetch_pubmed_data_correct_titles():
    articles = fetch_pubmed_data(KNOWN_PMIDS)
    for article in articles:
        assert article["title"] == EXPECTED_TITLES[article["pmid"]]


def test_fetch_pubmed_data_has_abstracts():
    """Most articles have abstracts; some (e.g., letters) may not."""
    articles = fetch_pubmed_data(KNOWN_PMIDS)
    with_abstract = [a for a in articles if a["abstract"]]
    assert len(with_abstract) >= 2  # at least 2 of 3 known PMIDs have abstracts
    assert all(len(a["abstract"]) > 50 for a in with_abstract)


def test_fetch_pubmed_data_single_pmid_string():
    """Accepts a single-element list without error."""
    articles = fetch_pubmed_data(["36003377"])
    assert len(articles) == 1
    assert articles[0]["pmid"] == "36003377"


def test_fetch_pubmed_data_rejects_bad_input():
    with pytest.raises(AssertionError):
        fetch_pubmed_data(["not_a_number"])
    with pytest.raises(AssertionError):
        fetch_pubmed_data([""])  # empty string


# --- Edge cases ---

def test_search_pubmed_no_results():
    """Nonsense exact-match query should return empty idlist, not error."""
    result = search_pubmed('"xyzzyqqq999zzznotarealterm"[ti]', retmax=5)
    assert result is not None
    assert result["idlist"] == []
    assert result["count"] == "0"


def test_fetch_pubmed_data_batching():
    """Batching logic is exercised when retmax_per_request < len(pmids)."""
    pmids = ["36003377", "38048195", "33497357"]
    articles = fetch_pubmed_data(pmids, retmax_per_request=2)
    assert len(articles) == 3
    assert {a["pmid"] for a in articles} == set(pmids)


def test_fetch_pubmed_data_string_input_comma_separated():
    """The function accepts a comma-separated string of PMIDs."""
    articles = fetch_pubmed_data("36003377, 33497357")
    assert len(articles) == 2
    assert {a["pmid"] for a in articles} == {"36003377", "33497357"}


def test_fetch_pubmed_data_string_input_list_literal():
    """The function accepts a stringified list of PMIDs."""
    articles = fetch_pubmed_data('["36003377", "33497357"]')
    assert len(articles) == 2
    assert {a["pmid"] for a in articles} == {"36003377", "33497357"}
