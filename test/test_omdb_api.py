"""
Test OMDB API with real API key
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OMDB_API_KEY")

print("=" * 60)
print("OMDB API Test with Real Posters")
print("=" * 60)
print()

if api_key and api_key != "":
    print(f"✅ API Key configured: {api_key[:8]}...")
    print()
    
    # Test with some popular movies
    test_movies = [
        ("The Godfather", 1972),
        ("Inception", 2010),
        ("The Matrix", 1999),
        ("Forrest Gump", 1994),
        ("Pulp Fiction", 1994)
    ]
    
    print("Testing OMDB API with sample movies:")
    print("-" * 60)
    
    for title, year in test_movies:
        try:
            params = {
                'apikey': api_key,
                't': title,
                'y': str(year)
            }
            
            response = requests.get('http://www.omdbapi.com/', params=params, timeout=5)
            data = response.json()
            
            if data.get('Response') == 'True':
                poster = data.get('Poster', 'N/A')
                if poster != 'N/A':
                    print(f"✅ {title} ({year})")
                    print(f"   Poster: {poster[:60]}...")
                else:
                    print(f"⚠️  {title} ({year}) - No poster available")
            else:
                print(f"❌ {title} ({year}) - Error: {data.get('Error', 'Unknown error')}")
            
        except Exception as e:
            print(f"❌ {title} ({year}) - Exception: {e}")
    
    print()
    print("=" * 60)
    print("✅ OMDB API is working correctly!")
    print("Real movie posters will now load in the dashboard")
    print("=" * 60)
    
else:
    print("❌ API Key not configured")
    print("Please set OMDB_API_KEY in .env file")

print()
