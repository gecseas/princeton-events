"""
scrapers/pmi.py  —  Princeton Materials Institute
Uses: Drupal JSON:API
Note: Correct URL is materials.princeton.edu, not pmi.princeton.edu
"""

from .drupal_api import scrape_drupal

BASE = "https://materials.princeton.edu"
DEPARTMENT = "Princeton Materials Institute (PMI)"
TAGS = ["Materials Science", "Engineering", "Applied Science"]


def scrape() -> list[dict]:
    return scrape_drupal(BASE, DEPARTMENT, TAGS)
