import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


def fetch_interest_rates(url: str, timeout: int = 10) -> Dict[str, str]:
    """
    Scrapes a page containing bank interest rates and returns a dict of rates.
    This is a simple example: real pages will require tailored parsers.
    """
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
    except requests.RequestException as exc:
        logger.exception("Failed to fetch rates")
        raise

    soup = BeautifulSoup(resp.text, "html.parser")
    # Example heuristic: find table rows with 'rate' or 'interest'
    data = {}
    for tr in soup.select("table tr"):
        cols = [td.get_text(strip=True) for td in tr.select("td")]
        if len(cols) >= 2:
            key = cols[0]
            val = cols[1]
            if "rate" in key.lower() or "%" in val:
                data[key] = val
    # fallback: look for any strong tags
    if not data:
        for tag in soup.select("p,li"):
            text = tag.get_text(" ", strip=True)
            if "%" in text:
                data[text[:40]] = text
    return data


def fetch_with_selenium(url: str, driver_path: Optional[str] = None) -> str:
    """
    Optional selenium fallback when JS rendering is required.
    This function is a stub — a real implementation requires selenium & driver.
    """
    raise NotImplementedError("Selenium fallback not implemented in this example.")
