"""
Test edge cases for poster extraction: missing/unknown movies
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "dashboard"))
from utils.database import DatabaseManager
from utils.movie_search import MovieCatalog

def test_edge_cases():
    db_manager = DatabaseManager()
    catalog = MovieCatalog(db_manager)
    cases = [
        ("Krot na more", 2012),
        ("Convenience", 2015)
    ]
    for title, year in cases:
        print(f"Testing: {title} ({year})")
        url = catalog.get_poster_url(title, year)
        print(f"  Poster URL: {url}")
        if url == "https://freesvg.org/img/Movie-Projector-Icon.png":
            print("  ✓ Returned MovieLover logo as expected.")
        elif url:
            print("  ⚠ Returned unexpected poster: ", url)
        else:
            print("  ✗ No poster returned!")
        print()
if __name__ == "__main__":
    test_edge_cases()
