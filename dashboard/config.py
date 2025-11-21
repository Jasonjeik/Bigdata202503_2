"""
Application configuration and settings
"""
import os
from pathlib import Path
import qrcode
from io import BytesIO
import base64

class AppConfig:
    # Application settings
    APP_NAME = "MovieLover - AI Sentiment Analysis"
    APP_VERSION = "1.0.0"
    APP_URL = "https://your-streamlit-app.streamlit.app"  # Update with your deployed URL
    
    # MongoDB configuration
    MONGODB_URI = os.getenv(
        "MONGODB_URI",
        "mongodb+srv://jasonebm16_db_user:JK0jknwzzkJdRaDt@bdproyecto2.u5gbblq.mongodb.net/?appName=BDProyecto2"
    )
    DATABASE_NAME = "sample_mflix"
    
    # Collections
    MOVIES_COLLECTION = "movies"
    COMMENTS_COLLECTION = "comments"
    USERS_COLLECTION = "users"
    REVIEWS_COLLECTION = "audience_reviews"  # New collection for storing user reviews
    
    # Model paths
    BASE_DIR = Path(__file__).parent.parent
    MODEL_DIR = BASE_DIR / "api" / "models"
    
    # Model files
    DISTILBERT_MODEL_PATH = MODEL_DIR / "distilbert_final"
    LSTM_MODEL_PATH = MODEL_DIR / "lstm_final_cv_complete.pth"
    LOGISTIC_MODEL_PATH = MODEL_DIR / "logistic_regression_tfidf.pkl"
    RANDOM_FOREST_MODEL_PATH = MODEL_DIR / "random_forest.pkl"
    VOCAB_LSTM_PATH = MODEL_DIR / "vocab_lstm.pkl"
    
    # OMDB API for movie posters
    OMDB_API_KEY = os.getenv("OMDB_API_KEY", "bbe61596")  # Demo key - get your own from http://www.omdbapi.com/
    
    # Visualization settings
    CHART_THEME = "plotly"
    COLOR_SCHEME = {
        'primary': '#4f46e5',
        'secondary': '#7c3aed',
        'positive': '#10b981',
        'negative': '#ef4444',
        'neutral': '#f59e0b'
    }
    
    # Pagination
    MOVIES_PER_PAGE = 20
    REVIEWS_PER_PAGE = 10
    
    @staticmethod
    def generate_qr_code(url=None):
        """Generate QR code for the application URL"""
        if url is None:
            url = AppConfig.APP_URL
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to bytes for Streamlit
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return buffer
    
    @staticmethod
    def get_model_info():
        """Return information about available models"""
        return {
            'distilbert': {
                'name': 'DistilBERT',
                'accuracy': 0.9161,
                'description': 'Transformer-based model, highest accuracy',
                'type': 'Deep Learning - Transformer'
            },
            'lstm': {
                'name': 'LSTM Neural Network',
                'accuracy': 0.8738,
                'description': 'Recurrent neural network optimized with Optuna',
                'type': 'Deep Learning - RNN'
            },
            'logistic': {
                'name': 'Logistic Regression',
                'accuracy': 0.8840,
                'description': 'Traditional ML with TF-IDF features',
                'type': 'Classical ML'
            },
            'random_forest': {
                'name': 'Random Forest',
                'accuracy': 0.8512,
                'description': 'Ensemble method with multiple decision trees',
                'type': 'Classical ML'
            }
        }
