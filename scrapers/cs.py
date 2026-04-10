"""
scrapers/cs.py  —  Department of Computer Science
Uses: Drupal JSON:API
"""

from .drupal_api import scrape_drupal

BASE = "https://www.cs.princeton.edu"
DEPARTMENT = "Department of Computer Science"
TAGS = ["Computer Science", "AI / ML", "Theory", "Systems"]


def scrape() -> list[dict]:
    return scrape_drupal(BASE, DEPARTMENT, TAGS)
