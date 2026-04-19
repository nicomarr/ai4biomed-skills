# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nico Marr

"""OpenAlex API utilities for retrieving scholarly work metadata.

This module provides functions to query the OpenAlex API for works by DOI or
PMID, decode inverted-index abstracts, and validate DOI strings. It is designed
to complement ``pubmed_utils.py`` by adding citation metrics, related works, and
open-access metadata from OpenAlex.

Requirements:
    pip install "httpx[socks]" --break-system-packages

Egress:
    Requires ``*.openalex.org`` in the network allowlist.

Typical usage in a Jupyter notebook::

    from openalex_utils import search_works, decode_abstract

    works = search_works(["10.1016/S0140-6736(24)00004-7", "35486828"])
    for w in works:
        print(w["title"], "—", w["cited_by_count"], "citations")
        abstract = decode_abstract(w.get("abstract_inverted_index"))
        if abstract:
            print(abstract[:200], "...")
"""

from __future__ import annotations

import re
from typing import Optional, Union

import httpx

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OPENALEX_API = "https://api.openalex.org"
MAX_PER_PAGE = 200  # OpenAlex hard limit (per-page max; 201+ returns HTTP 400)
REQUEST_TIMEOUT = 20  # seconds


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------


def doi_is_valid(doi: str) -> bool:
    """Check whether a string looks like a valid DOI.

    Accepts both bare DOIs (``10.1234/abc``) and full URLs
    (``https://doi.org/10.1234/abc``).

    Args:
        doi: The string to validate.

    Returns:
        True if the string matches the DOI pattern ``10.<registrant>/<suffix>``.
    """
    bare = _strip_doi_url(doi)
    return bool(re.match(r"^10\.\d{4,9}/\S+$", bare))


def decode_abstract(inverted_index: Optional[dict]) -> Optional[str]:
    """Decode an OpenAlex inverted-index abstract into plain text.

    OpenAlex stores abstracts as ``{word: [positions]}`` dictionaries. This
    function reassembles them into readable strings.

    Args:
        inverted_index: The ``abstract_inverted_index`` dict from an OpenAlex
            work record, or ``None``.

    Returns:
        The decoded abstract string, or ``None`` if the input is empty/None.
    """
    if not inverted_index:
        return None
    word_positions: list[tuple[int, str]] = [
        (pos, word)
        for word, positions in inverted_index.items()
        for pos in positions
    ]
    return " ".join(word for _, word in sorted(word_positions))


def search_works(
    identifiers: Union[str, list[str]],
    mailto: Optional[str] = None,
) -> list[dict]:
    """Retrieve OpenAlex work records for one or more identifiers.

    Each identifier can be any of:

    - A **bare DOI**: ``"10.1016/S0140-6736(24)00004-7"``
    - A **DOI URL**: ``"https://doi.org/10.1016/S0140-6736(24)00004-7"``
    - A **PMID** (numeric string): ``"35486828"``

    The function automatically classifies each identifier, groups DOIs and
    PMIDs into separate batched API calls (respecting the 200-per-page limit),
    and merges the results.

    Args:
        identifiers: A single identifier string, or a list of them.
        mailto: Optional email for OpenAlex's polite pool (faster rate limits).
            See https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication

    Returns:
        A list of OpenAlex work dicts. Works that were not found are silently
        omitted (check the length of the result). Returns an empty list on
        total failure.

    Raises:
        ValueError: If *identifiers* is empty or contains only blank strings.

    Example::

        works = search_works(["10.1016/S0140-6736(24)00004-7", "35486828"])
        for w in works:
            print(w["title"], w["cited_by_count"])
    """
    # --- Normalize input ------------------------------------------------
    if isinstance(identifiers, str):
        identifiers = [identifiers]
    identifiers = [s.strip() for s in identifiers if s.strip()]
    if not identifiers:
        raise ValueError("identifiers must be a non-empty list of DOIs or PMIDs")

    # --- Classify each identifier ---------------------------------------
    dois: list[str] = []
    pmids: list[str] = []
    for ident in identifiers:
        if _looks_like_pmid(ident):
            pmids.append(ident)
        else:
            # Normalize to full DOI URL for the filter
            dois.append(_normalize_doi_url(ident))

    # --- Fetch in batches -----------------------------------------------
    all_works: list[dict] = []

    for batch in _batches(dois, MAX_PER_PAGE):
        doi_filter = "|".join(batch)
        works = _api_get_works(f"doi:{doi_filter}", mailto=mailto)
        if works is not None:
            all_works.extend(works)

    for batch in _batches(pmids, MAX_PER_PAGE):
        pmid_urls = [f"https://pubmed.ncbi.nlm.nih.gov/{p}" for p in batch]
        pmid_filter = "|".join(pmid_urls)
        works = _api_get_works(f"ids.pmid:{pmid_filter}", mailto=mailto)
        if works is not None:
            all_works.extend(works)

    return all_works


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _api_get_works(
    filter_expr: str,
    mailto: Optional[str] = None,
) -> Optional[list[dict]]:
    """Execute a single ``/works?filter=…`` request.

    Args:
        filter_expr: The complete filter string, e.g. ``"doi:https://doi.org/10.1234/abc"``.
        mailto: Optional email for the polite pool.

    Returns:
        A list of work dicts, or ``None`` on HTTP error.
    """
    params: dict[str, Union[str, int]] = {
        "filter": filter_expr,
        "per-page": MAX_PER_PAGE,
    }
    if mailto:
        params["mailto"] = mailto

    try:
        resp = httpx.get(
            f"{OPENALEX_API}/works",
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json().get("results", [])
    except httpx.HTTPError as exc:
        print(f"OpenAlex API error: {exc}")
        return None


def _strip_doi_url(doi: str) -> str:
    """Remove the ``https://doi.org/`` prefix if present."""
    for prefix in ("https://doi.org/", "http://doi.org/"):
        if doi.startswith(prefix):
            return doi[len(prefix):]
    return doi


def _normalize_doi_url(doi: str) -> str:
    """Ensure a DOI is a full ``https://doi.org/…`` URL."""
    bare = _strip_doi_url(doi)
    return f"https://doi.org/{bare}"


def _looks_like_pmid(identifier: str) -> bool:
    """Return True if *identifier* is a purely numeric string (i.e. a PMID)."""
    return bool(re.fullmatch(r"\d+", identifier))


def _batches(items: list, size: int):
    """Yield successive chunks of *items* with at most *size* elements."""
    for i in range(0, len(items), size):
        yield items[i : i + size]
