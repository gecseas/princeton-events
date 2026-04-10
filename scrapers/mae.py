"""
scrapers/mae.py  —  Mechanical and Aerospace Engineering
Uses: Drupal JSON:API
"""

from .drupal_api import scrape_drupal

BASE = "https://mae.princeton.edu"
DEPARTMENT = "Mechanical and Aerospace Engineering (MAE)"
TAGS = ["Mechanical Engineering", "Aerospace", "Engineering", "Energy"]


def scrape() -> list[dict]:
    return scrape_drupal(BASE, DEPARTMENT, TAGS)
