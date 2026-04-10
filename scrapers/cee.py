"""
scrapers/cee.py  —  Civil and Environmental Engineering
Uses: Drupal JSON:API
"""

from .drupal_api import scrape_drupal

BASE = "https://cee.princeton.edu"
DEPARTMENT = "Civil and Environmental Engineering (CEE)"
TAGS = ["Civil Engineering", "Environmental Engineering", "Sustainability", "Engineering"]


def scrape() -> list[dict]:
    return scrape_drupal(BASE, DEPARTMENT, TAGS)
