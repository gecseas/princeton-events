"""
scrapers/orfe.py  —  Operations Research and Financial Engineering
Uses: Drupal JSON:API
"""

from .drupal_api import scrape_drupal

BASE = "https://orfe.princeton.edu"
DEPARTMENT = "Operations Research and Financial Engineering (ORFE)"
TAGS = ["Operations Research", "Financial Engineering", "Statistics", "AI / ML"]


def scrape() -> list[dict]:
    return scrape_drupal(BASE, DEPARTMENT, TAGS)
