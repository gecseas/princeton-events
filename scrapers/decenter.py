"""
scrapers/decenter.py  —  DeCenter (Blockchain & Decentralization)
Uses: WordPress + Tribe Events REST API
API: https://decenter.princeton.edu/wp-json/tribe/events/v1/events
"""

from .wp_tribe import scrape_tribe

BASE = "https://decenter.princeton.edu"
DEPARTMENT = "DeCenter (Center for Decentralization of Power Through Blockchain)"
TAGS = ["Blockchain", "Tech Policy", "Computer Science", "Financial Engineering"]


def scrape() -> list[dict]:
    return scrape_tribe(BASE, DEPARTMENT, TAGS)
