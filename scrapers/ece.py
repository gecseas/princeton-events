"""
scrapers/ece.py  —  Electrical and Computer Engineering
Uses: Drupal JSON:API
"""

from .drupal_api import scrape_drupal

BASE = "https://ece.princeton.edu"
DEPARTMENT = "Electrical and Computer Engineering (ECE)"
TAGS = ["Electrical Engineering", "Computer Engineering", "Engineering", "AI / ML"]


def scrape() -> list[dict]:
    return scrape_drupal(BASE, DEPARTMENT, TAGS)
