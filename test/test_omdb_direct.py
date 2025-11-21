"""
Direct OMDB API test to verify poster URL extraction
"""
import requests
import os

def test_omdb_direct():
    """Test OMDB API directly with various configurations"""
    
    print("=" * 80)
    print("OMDB API DIRECT TEST")
    print("=" * 80)
    
    # Check for API key
    api_key = os.getenv("OMDB_API_KEY", "")
    
    print(f"\nAPI Key configured: {'Yes' if api_key else 'No (using free key)'}")
    
    # Use a free/public API key for testing (you should get your own from http://www.omdbapi.com/)
    # Note: Free keys have daily limits
    if not api_key:
        # This is a demo key - replace with your own
        api_key = "bbe61596"  # Demo key (may have rate limits)
        print(f"Using demo API key: {api_key}")
    
    print("\n" + "=" * 80)
    print("Testing with real movie: Harry Potter and the Deathly Hallows: Part 2")
    print("=" * 80)
    
    # Test case 1: With year
    print("\n[Test 1] Query with title and year:")
    print("-" * 80)
    
    params = {
        'apikey': api_key,
        't': 'Harry Potter and the Deathly Hallows: Part 2',
        'y': '2011'
    }
    
    try:
        response = requests.get('http://www.omdbapi.com/', params=params, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response URL: {response.url}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nJSON Response (formatted):")
            print(f"  Response: {data.get('Response')}")
            print(f"  Title: {data.get('Title')}")
            print(f"  Year: {data.get('Year')}")
            print(f"  Poster: {data.get('Poster')}")
            
            if data.get('Error'):
                print(f"  ❌ Error: {data.get('Error')}")
            
            if data.get('Response') == 'True' and data.get('Poster'):
                poster_url = data['Poster']
                if poster_url != 'N/A':
                    print(f"\n✓ SUCCESS: Poster URL retrieved")
                    print(f"  URL: {poster_url}")
                    
                    # Verify poster is accessible
                    print(f"\n  Verifying poster accessibility...")
                    try:
                        head = requests.head(poster_url, timeout=3)
                        print(f"  Poster Status: {head.status_code}")
                        print(f"  Content-Type: {head.headers.get('Content-Type')}")
                        
                        if head.status_code == 200:
                            print(f"  ✓ Poster is accessible!")
                        else:
                            print(f"  ✗ Poster returned non-200 status")
                    except Exception as e:
                        print(f"  ✗ Poster verification failed: {e}")
                else:
                    print(f"\n✗ FAIL: Poster is 'N/A'")
            else:
                print(f"\n✗ FAIL: Invalid response or no poster")
        else:
            print(f"✗ FAIL: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"✗ EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
    
    # Test case 2: Without year
    print("\n" + "=" * 80)
    print("[Test 2] Query with title only (no year):")
    print("=" * 80)
    
    params = {
        'apikey': api_key,
        't': 'The Godfather'
    }
    
    try:
        response = requests.get('http://www.omdbapi.com/', params=params, timeout=5)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data.get('Response')}")
            print(f"Title: {data.get('Title')}")
            print(f"Year: {data.get('Year')}")
            print(f"Poster: {data.get('Poster')}")
            
            if data.get('Poster') and data['Poster'] != 'N/A':
                print(f"✓ SUCCESS: Poster URL retrieved")
            else:
                print(f"✗ FAIL: No poster available")
    except Exception as e:
        print(f"✗ EXCEPTION: {e}")
    
    # Test case 3: Invalid movie
    print("\n" + "=" * 80)
    print("[Test 3] Query with invalid movie name:")
    print("=" * 80)
    
    params = {
        'apikey': api_key,
        't': 'This Movie Does Not Exist XYZ123'
    }
    
    try:
        response = requests.get('http://www.omdbapi.com/', params=params, timeout=5)
        data = response.json()
        print(f"Response: {data.get('Response')}")
        print(f"Error: {data.get('Error')}")
        
        if data.get('Response') == 'False':
            print(f"✓ SUCCESS: Correctly returned error for invalid movie")
        else:
            print(f"✗ Unexpected response")
    except Exception as e:
        print(f"✗ EXCEPTION: {e}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)
    
    print("\n📝 NOTES:")
    print("  1. If all tests failed with 401 or rate limit errors, you need a valid API key")
    print("  2. Get a free API key at: http://www.omdbapi.com/apikey.aspx")
    print("  3. Set it as environment variable: OMDB_API_KEY=your_key_here")
    print("  4. Or update config.py with your key")

if __name__ == "__main__":
    test_omdb_direct()
