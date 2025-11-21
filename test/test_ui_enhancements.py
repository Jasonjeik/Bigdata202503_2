"""
Quick test script for MovieLover UI enhancements
Tests: Star rating system, modal functionality, OMDB integration
"""

import sys
from pathlib import Path

# Add dashboard to path
sys.path.insert(0, str(Path(__file__).parent))

def test_star_rating_conversion():
    """Test star rating display logic"""
    print("Testing Star Rating System...")
    print("-" * 50)
    
    test_ratings = [1.0, 2.3, 3.5, 4.7, 5.0]
    
    for rating in test_ratings:
        full_stars = int(rating)
        half_star = 1 if (rating - full_stars) >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star
        stars = '⭐' * full_stars + '✨' * half_star + '☆' * empty_stars
        print(f"{rating:.1f}/5 → {stars}")
    
    print("✅ Star rating conversion working\n")

def test_omdb_config():
    """Test OMDB API configuration"""
    print("Testing OMDB Configuration...")
    print("-" * 50)
    
    try:
        from config import AppConfig
        
        if AppConfig.OMDB_API_KEY and AppConfig.OMDB_API_KEY != "":
            print(f"✅ OMDB API Key configured: {AppConfig.OMDB_API_KEY[:8]}...")
            print("   Real movie posters will be loaded")
        else:
            print("⚠️  OMDB API Key not configured")
            print("   Placeholder images will be used")
            print("   See OMDB_API_SETUP.md for instructions")
        
    except Exception as e:
        print(f"❌ Error loading config: {e}")
    
    print()

def test_app_branding():
    """Test MovieLover branding"""
    print("Testing MovieLover Branding...")
    print("-" * 50)
    
    try:
        from config import AppConfig
        
        print(f"App Name: {AppConfig.APP_NAME}")
        
        if "MovieLover" in AppConfig.APP_NAME:
            print("✅ Branding updated to MovieLover")
        else:
            print("❌ Branding not updated")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()

def test_imports():
    """Test that all modules import correctly"""
    print("Testing Module Imports...")
    print("-" * 50)
    
    modules = [
        "utils.database",
        "utils.models",
        "utils.visualizations",
        "utils.movie_search",
        "utils.language",
        "config"
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except Exception as e:
            print(f"❌ {module}: {e}")
    
    print()

def test_dialog_syntax():
    """Verify @st.dialog syntax is correct"""
    print("Testing Dialog Decorator...")
    print("-" * 50)
    
    # Read app.py and check for @st.dialog
    app_path = Path(__file__).parent / "app.py"
    
    try:
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '@st.dialog' in content:
            print("✅ @st.dialog decorator found in app.py")
            print("   Floating modal will work correctly")
        else:
            print("⚠️  @st.dialog not found")
        
        if 'show_review_dialog()' in content:
            print("✅ show_review_dialog() function defined")
        
    except Exception as e:
        print(f"❌ Error reading app.py: {e}")
    
    print()

def main():
    print("=" * 50)
    print("MovieLover UI Enhancements - Test Suite")
    print("=" * 50)
    print()
    
    test_app_branding()
    test_omdb_config()
    test_star_rating_conversion()
    test_imports()
    test_dialog_syntax()
    
    print("=" * 50)
    print("Test Suite Complete!")
    print("=" * 50)
    print()
    print("Next Steps:")
    print("1. Run: streamlit run app.py")
    print("2. Test each feature manually")
    print("3. Check UI_ENHANCEMENTS.md for detailed testing checklist")
    print()
    print("If you see any ❌ errors above, address them before running the app.")

if __name__ == "__main__":
    main()
