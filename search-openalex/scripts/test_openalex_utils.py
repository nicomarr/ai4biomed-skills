# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nico Marr

"""Tests for openalex_utils module.

Run with:
    python -m pytest test_openalex_utils.py -v -p no:cacheprovider

Requires:
    pip install "httpx[socks]" pytest --break-system-packages
    *.openalex.org in egress allowlist
"""

import pytest
from openalex_utils import doi_is_valid, decode_abstract, search_works


# ======================================================================
# doi_is_valid
# ======================================================================


class TestDoiIsValid:
    """Tests for DOI validation."""

    def test_full_url(self):
        assert doi_is_valid("https://doi.org/10.1016/S0140-6736(24)00004-7") is True

    def test_bare_doi(self):
        assert doi_is_valid("10.1111/tmi.14062") is True

    def test_http_url(self):
        assert doi_is_valid("http://doi.org/10.1234/test") is True

    def test_invalid_string(self):
        assert doi_is_valid("not-a-doi") is False

    def test_empty_string(self):
        assert doi_is_valid("") is False

    def test_pmid_not_a_doi(self):
        """A bare numeric PMID is not a valid DOI."""
        assert doi_is_valid("35486828") is False

    def test_short_registrant_rejected(self):
        """DOI registrants must have at least 4 digits."""
        assert doi_is_valid("10.12/x") is False


# ======================================================================
# decode_abstract
# ======================================================================


class TestDecodeAbstract:
    """Tests for inverted-index abstract decoding."""

    def test_basic(self):
        inv = {"The": [0], "quick": [1], "brown": [2], "fox": [3]}
        assert decode_abstract(inv) == "The quick brown fox"

    def test_repeated_word(self):
        inv = {"the": [0, 4], "cat": [1], "sat": [2], "on": [3], "mat": [5]}
        assert decode_abstract(inv) == "the cat sat on the mat"

    def test_none_input(self):
        assert decode_abstract(None) is None

    def test_empty_dict(self):
        assert decode_abstract({}) is None


# ======================================================================
# search_works — input handling
# ======================================================================


class TestSearchWorksInput:
    """Tests for input normalization and validation."""

    def test_rejects_empty_list(self):
        with pytest.raises(ValueError, match="non-empty"):
            search_works([])

    def test_rejects_blank_strings(self):
        with pytest.raises(ValueError, match="non-empty"):
            search_works(["", "  "])

    def test_accepts_single_string(self):
        """A single string (not a list) should work."""
        works = search_works("10.1016/S0140-6736(24)00004-7")
        assert works is not None
        assert len(works) == 1

    def test_accepts_mixed_whitespace(self):
        """Leading/trailing whitespace on identifiers should be stripped."""
        works = search_works(["  10.1016/S0140-6736(24)00004-7  "])
        assert len(works) == 1


# ======================================================================
# search_works — DOI lookups (network required)
# ======================================================================

KNOWN_DOIS = [
    "https://doi.org/10.1016/S0140-6736(24)00004-7",
    "https://doi.org/10.1111/tmi.14062",
    "https://doi.org/10.1007/s00281-024-01022-9",
]


class TestSearchWorksByDoi:
    """DOI-based lookups against the live API."""

    def test_returns_all(self):
        works = search_works(KNOWN_DOIS)
        assert len(works) == 3

    def test_has_expected_fields(self):
        works = search_works(KNOWN_DOIS[:1])
        work = works[0]
        for key in ("id", "title", "doi", "cited_by_count", "counts_by_year",
                     "related_works"):
            assert key in work, f"Missing field: {key}"

    def test_has_abstract_inverted_index(self):
        works = search_works(KNOWN_DOIS)
        with_abstract = [w for w in works if w.get("abstract_inverted_index")]
        assert len(with_abstract) >= 1

    def test_abstract_decodes(self):
        works = search_works(KNOWN_DOIS)
        for w in works:
            inv = w.get("abstract_inverted_index")
            if inv:
                text = decode_abstract(inv)
                assert isinstance(text, str)
                assert len(text) > 50
                break
        else:
            pytest.skip("No works had abstract_inverted_index")

    def test_bare_doi(self):
        """Bare DOIs (no https://doi.org/ prefix) should work."""
        works = search_works(["10.1007/s00281-024-01022-9"])
        assert len(works) == 1

    def test_single_doi_url(self):
        works = search_works(["https://doi.org/10.1007/s00281-024-01022-9"])
        assert len(works) == 1


# ======================================================================
# search_works — PMID lookups (network required)
# ======================================================================


class TestSearchWorksByPmid:
    """PMID-based lookups against the live API."""

    def test_single_pmid(self):
        """PMID 35486828 should resolve to a work in OpenAlex."""
        works = search_works(["35486828"])
        assert len(works) == 1
        assert "title" in works[0]

    def test_multiple_pmids(self):
        works = search_works(["35486828", "33264437"])
        assert len(works) == 2

    def test_mixed_doi_and_pmid(self):
        """A mix of DOIs and PMIDs in one call should return all works."""
        works = search_works([
            "10.1016/S0140-6736(24)00004-7",  # bare DOI
            "35486828",                         # PMID
        ])
        assert len(works) == 2


# ======================================================================
# search_works — edge cases
# ======================================================================


class TestSearchWorksEdgeCases:
    """Edge-case handling."""

    def test_nonexistent_doi_returns_empty(self):
        """A fabricated DOI should return no results (not crash)."""
        works = search_works(["10.9999/this-doi-does-not-exist-xyz"])
        assert works == []

    def test_nonexistent_pmid_returns_empty(self):
        """A fabricated PMID should return no results (not crash)."""
        works = search_works(["9999999999"])
        assert works == []
