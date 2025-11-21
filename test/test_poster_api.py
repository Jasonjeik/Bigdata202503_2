"""
Test script for poster URL extraction from OMDB API
"""
import sys
from pathlib import Path

# Add dashboard to path
sys.path.insert(0, str(Path(__file__).parent / "dashboard"))

from utils.database import DatabaseManager
from utils.movie_search import MovieCatalog

def test_poster_extraction():
    """Test poster URL extraction with various movies"""
    
    print("=" * 80)
    print("POSTER API EXTRACTION TEST")
    print("=" * 80)
    
    # Initialize
    db_manager = DatabaseManager()
    catalog = MovieCatalog(db_manager)
    
    # Test cases: movies with different characteristics
    test_movies = [
        ("Harry Potter and the Deathly Hallows: Part 2", 2011),
        ("The Shawshank Redemption", 1994),
        ("The Godfather", 1972),
        ("Inception", 2010),
        ("Pulp Fiction", 1994),
        ("The Dark Knight", 2008),
        ("Forrest Gump", 1994),
        ("The Matrix", 1999),
        ("Invalid Movie That Does Not Exist XYZ123", 2025),  # Should fallback
        ("Titanic", 1997)
    ]
    
    print(f"\nTesting {len(test_movies)} movies...\n")
    
    results = []
    for title, year in test_movies:
        print(f"Testing: {title} ({year})")
        print("-" * 80)
        
        try:
            poster_url = catalog.get_poster_url(title, year)
            
            # Check if it's a real poster or placeholder
            is_placeholder = "via.placeholder.com" in poster_url or "placehold.co" in poster_url
            is_amazon = "media-amazon.com" in poster_url or "media-imdb.com" in poster_url
            
            result = {
                'title': title,
                'year': year,
                'url': poster_url,
                'type': 'PLACEHOLDER' if is_placeholder else ('OMDB/Amazon' if is_amazon else 'OTHER'),
                'valid': bool(poster_url and poster_url.startswith('http'))
            }
            results.append(result)
            
            print(f"  ✓ URL Type: {result['type']}")
            print(f"  ✓ URL: {poster_url[:100]}{'...' if len(poster_url) > 100 else ''}")
            print(f"  ✓ Valid: {result['valid']}")
            
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            results.append({
                'title': title,
                'year': year,
                'url': None,
                'type': 'ERROR',
                'valid': False
            })
        
        print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    total = len(results)
    valid_count = sum(1 for r in results if r['valid'])
    omdb_count = sum(1 for r in results if 'OMDB' in r['type'])
    placeholder_count = sum(1 for r in results if r['type'] == 'PLACEHOLDER')
    error_count = sum(1 for r in results if r['type'] == 'ERROR')
    
    print(f"Total Movies Tested: {total}")
    print(f"Valid URLs: {valid_count}/{total} ({valid_count/total*100:.1f}%)")
    print(f"OMDB/Amazon Posters: {omdb_count} ({omdb_count/total*100:.1f}%)")
    print(f"Placeholder Images: {placeholder_count} ({placeholder_count/total*100:.1f}%)")
    print(f"Errors: {error_count}")
    
    print("\n" + "=" * 80)
    print("DETAILED RESULTS")
    print("=" * 80)
    
    for r in results:
        status = "✓" if r['valid'] else "✗"
        print(f"{status} [{r['type']:15s}] {r['title'][:40]:40s} ({r['year']})")
        if r['url']:
            print(f"    {r['url'][:90]}...")
    
    print("\n" + "=" * 80)
    
    # Test cache effectiveness
    print("\nTesting cache effectiveness...")
    print("-" * 80)
    
    import time
    
    # First call (should fetch from API)
    start = time.time()
    url1 = catalog.get_poster_url("The Godfather", 1972)
    time1 = time.time() - start
    
    # Second call (should use cache)
    start = time.time()
    url2 = catalog.get_poster_url("The Godfather", 1972)
    time2 = time.time() - start
    
    print(f"First call (API): {time1:.4f}s")
    print(f"Second call (Cache): {time2:.4f}s")
    print(f"Speed improvement: {(time1/time2):.1f}x faster")
    print(f"URLs match: {url1 == url2}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    try:
        results = test_poster_extraction()
        
        # Exit with appropriate code
        if all(r['valid'] for r in results if r['type'] != 'ERROR'):
            print("\n✓ All valid URLs successfully retrieved!")
            sys.exit(0)
        else:
            print("\n⚠ Some URLs failed validation")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n✗ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
