"""
scrapers/cbe.py  —  Chemical and Biological Engineering
Uses: Drupal JSON:API
"""

from .drupal_api import scrape_drupal

BASE = "https://cbe.princeton.edu"
DEPARTMENT = "Chemical and Biological Engineering (CBE)"
TAGS = ["Chemical Engineering", "Biological Engineering", "Engineering"]


def scrape() -> list[dict]:
    return scrape_drupal(BASE, DEPARTMENT, TAGS)
