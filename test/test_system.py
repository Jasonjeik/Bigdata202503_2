"""
Test script to verify all components are working correctly
Run this before deploying or presenting
"""

import sys
from pathlib import Path

# Color output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.END}")

def test_imports():
    """Test if all required packages are installed"""
    print_info("Testing package imports...")
    
    packages = [
        ('streamlit', 'streamlit'),
        ('pymongo', 'pymongo'),
        ('torch', 'torch'),
        ('transformers', 'transformers'),
        ('sklearn', 'scikit-learn'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('plotly', 'plotly'),
        ('PIL', 'Pillow'),
        ('qrcode', 'qrcode'),
        ('requests', 'requests'),
    ]
    
    all_ok = True
    for module, package in packages:
        try:
            __import__(module)
            print_success(f"{package} installed")
        except ImportError:
            print_error(f"{package} NOT installed - run: pip install {package}")
            all_ok = False
    
    return all_ok

def test_model_files():
    """Test if all model files exist"""
    print_info("\nTesting model files...")
    
    base_dir = Path(__file__).parent.parent
    model_dir = base_dir / "api" / "models"
    
    required_files = [
        'distilbert_final',
        'lstm_final_cv_complete.pth',
        'logistic_regression_tfidf.pkl',
        'random_forest.pkl',
        'vocab_lstm.pkl'
    ]
    
    all_ok = True
    for file in required_files:
        file_path = model_dir / file
        if file_path.exists():
            if file_path.is_dir():
                # Check if directory has files
                if list(file_path.iterdir()):
                    print_success(f"{file}/ directory exists and contains files")
                else:
                    print_error(f"{file}/ directory is empty")
                    all_ok = False
            else:
                size_mb = file_path.stat().st_size / (1024 * 1024)
                print_success(f"{file} exists ({size_mb:.1f} MB)")
        else:
            print_error(f"{file} NOT FOUND at {file_path}")
            all_ok = False
    
    return all_ok

def test_database_connection():
    """Test MongoDB connection"""
    print_info("\nTesting database connection...")
    
    try:
        from pymongo import MongoClient
        from pymongo.server_api import ServerApi
        import os
        from dotenv import load_dotenv
        
        # Load environment variables
        load_dotenv()
        
        uri = os.getenv("MONGODB_URI", 
                       "mongodb+srv://jasonebm16_db_user:JK0jknwzzkJdRaDt@bdproyecto2.u5gbblq.mongodb.net/?appName=BDProyecto2")
        
        client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        
        # Test database and collections
        db = client['sample_mflix']
        movie_count = db.movies.count_documents({})
        
        print_success(f"Connected to MongoDB")
        print_success(f"Database 'sample_mflix' accessible")
        print_success(f"Found {movie_count:,} movies in database")
        
        client.close()
        return True
        
    except Exception as e:
        print_error(f"Database connection failed: {e}")
        print_warning("Make sure MongoDB URI is correct in .env file")
        return False

def test_model_loading():
    """Test if models can be loaded"""
    print_info("\nTesting model loading...")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "dashboard"))
        from utils.models import ModelManager
        
        manager = ModelManager()
        available = manager.get_available_models()
        
        if available:
            print_success(f"Loaded {len(available)} models: {', '.join(available)}")
        else:
            print_error("No models were loaded successfully")
            return False
        
        # Test a prediction
        test_text = "This movie was absolutely amazing! I loved every minute of it."
        result = manager.predict_sentiment(test_text, available[0])
        
        print_success(f"Test prediction: {result['label']} (confidence: {result['score']:.2%})")
        
        return True
        
    except Exception as e:
        print_error(f"Model loading failed: {e}")
        return False

def test_app_structure():
    """Test if all required files exist"""
    print_info("\nTesting application structure...")
    
    base_dir = Path(__file__).parent.parent / "dashboard"
    
    required_files = [
        'app.py',
        'config.py',
        'requirements.txt',
        'README.md',
        'utils/__init__.py',
        'utils/database.py',
        'utils/models.py',
        'utils/movie_search.py',
        'utils/visualizations.py',
    ]
    
    all_ok = True
    for file in required_files:
        file_path = base_dir / file
        if file_path.exists():
            print_success(f"{file} exists")
        else:
            print_error(f"{file} NOT FOUND")
            all_ok = False
    
    return all_ok

def test_environment():
    """Test environment configuration"""
    print_info("\nTesting environment configuration...")
    
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    required_vars = ['MONGODB_URI']
    optional_vars = ['OMDB_API_KEY', 'APP_URL']
    
    all_ok = True
    for var in required_vars:
        if os.getenv(var):
            print_success(f"{var} is set")
        else:
            print_error(f"{var} is NOT set")
            all_ok = False
    
    for var in optional_vars:
        if os.getenv(var):
            print_success(f"{var} is set (optional)")
        else:
            print_warning(f"{var} is not set (optional)")
    
    return all_ok

def main():
    """Run all tests"""
    print("=" * 60)
    print("Movie Sentiment Analytics Platform - System Check")
    print("=" * 60)
    
    results = {
        "Imports": test_imports(),
        "File Structure": test_app_structure(),
        "Environment": test_environment(),
        "Model Files": test_model_files(),
        "Database": test_database_connection(),
        "Model Loading": test_model_loading(),
    }
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results.items():
        if passed:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print_success("ALL TESTS PASSED! System is ready for deployment.")
        print_info("\nNext steps:")
        print("  1. Run: streamlit run app.py")
        print("  2. Test the UI manually")
        print("  3. Deploy to Streamlit Cloud")
        return 0
    else:
        print_error("SOME TESTS FAILED! Please fix issues before deploying.")
        print_info("\nCommon fixes:")
        print("  • Install missing packages: pip install -r requirements.txt")
        print("  • Copy .env.example to .env and configure")
        print("  • Ensure model files are in api/models/")
        print("  • Check MongoDB connection string")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
