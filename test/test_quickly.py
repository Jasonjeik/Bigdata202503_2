"""
Quick test to verify imports and model paths
"""
import sys
from pathlib import Path

# Add dashboard to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("Testing Dashboard Application Setup")
print("=" * 60)

# Test 1: Import config
print("\n1. Testing config import...")
try:
    from config import AppConfig
    print(f"   ✓ Config imported successfully")
    print(f"   - Base DIR: {AppConfig.BASE_DIR}")
    print(f"   - Model DIR: {AppConfig.MODEL_DIR}")
    print(f"   - Model DIR exists: {AppConfig.MODEL_DIR.exists()}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: Check model files
print("\n2. Checking model files...")
try:
    from config import AppConfig
    
    models = {
        'DistilBERT': AppConfig.DISTILBERT_MODEL_PATH,
        'LSTM': AppConfig.LSTM_MODEL_PATH,
        'Logistic Regression': AppConfig.LOGISTIC_MODEL_PATH,
        'Random Forest': AppConfig.RANDOM_FOREST_MODEL_PATH,
        'LSTM Vocab': AppConfig.VOCAB_LSTM_PATH
    }
    
    for name, path in models.items():
        exists = path.exists()
        symbol = "✓" if exists else "✗"
        print(f"   {symbol} {name}: {path} ({'EXISTS' if exists else 'NOT FOUND'})")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Import utilities
print("\n3. Testing utility imports...")
try:
    from utils.database import DatabaseManager
    print("   ✓ DatabaseManager imported")
except Exception as e:
    print(f"   ✗ DatabaseManager error: {e}")

try:
    from utils.models import ModelManager
    print("   ✓ ModelManager imported")
except Exception as e:
    print(f"   ✗ ModelManager error: {e}")

try:
    from utils.movie_search import MovieCatalog
    print("   ✓ MovieCatalog imported")
except Exception as e:
    print(f"   ✗ MovieCatalog error: {e}")

try:
    from utils.visualizations import create_sentiment_gauge
    print("   ✓ Visualizations imported")
except Exception as e:
    print(f"   ✗ Visualizations error: {e}")

# Test 4: Database connection
print("\n4. Testing database connection...")
try:
    from utils.database import DatabaseManager
    db = DatabaseManager()
    if db.is_connected():
        print(f"   ✓ Connected to MongoDB")
        count = db.get_movie_count()
        print(f"   ✓ Found {count:,} movies in database")
    else:
        print("   ✗ Failed to connect to MongoDB")
except Exception as e:
    print(f"   ✗ Database error: {e}")

# Test 5: Model loading (basic test, not full loading)
print("\n5. Testing model loading capability...")
try:
    import torch
    print(f"   ✓ PyTorch available (device: {'cuda' if torch.cuda.is_available() else 'cpu'})")
    
    try:
        from transformers import DistilBertTokenizer
        print("   ✓ Transformers library available")
    except:
        print("   ⚠ Transformers not available")
    
    import pickle
    print("   ✓ Pickle available for sklearn models")
    
except Exception as e:
    print(f"   ✗ Model loading error: {e}")

print("\n" + "=" * 60)
print("Setup verification complete!")
print("=" * 60)
print("\nTo run the application:")
print("  streamlit run app.py")
