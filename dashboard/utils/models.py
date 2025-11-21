"""
Model loading and inference utilities
"""
import torch
import torch.nn as nn
import numpy as np
import pickle
import time
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from config import AppConfig
except ImportError:
    import importlib.util
    config_path = Path(__file__).parent.parent / 'config.py'
    spec = importlib.util.spec_from_file_location("config", config_path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    AppConfig = config_module.AppConfig

class LSTMSentimentModel(nn.Module):
    """LSTM model architecture for sentiment analysis"""
    def __init__(self, vocab_size, embedding_dim=128, hidden_dim=256, num_layers=2, dropout=0.3):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.lstm = nn.LSTM(
            embedding_dim,
            hidden_dim,
            num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0,
            bidirectional=True
        )
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * 2, 1)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, (hidden, cell) = self.lstm(embedded)
        # Use last hidden state from both directions
        hidden_concat = torch.cat((hidden[-2], hidden[-1]), dim=1)
        dropped = self.dropout(hidden_concat)
        output = self.fc(dropped)
        return self.sigmoid(output)

class ModelManager:
    """Manage loading and inference for all sentiment analysis models"""
    
    def __init__(self):
        self.models = {}
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self._load_models()
    
    def _load_models(self):
        """Load all pre-trained models"""
        print("Loading models...")
        
        # Load DistilBERT
        try:
            from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
            
            model_path = AppConfig.DISTILBERT_MODEL_PATH
            if model_path.exists():
                self.models['distilbert'] = {
                    'model': DistilBertForSequenceClassification.from_pretrained(str(model_path)).to(self.device),
                    'tokenizer': DistilBertTokenizer.from_pretrained(str(model_path))
                }
                self.models['distilbert']['model'].eval()
                print("✓ DistilBERT loaded")
            else:
                print(f"⚠ DistilBERT model not found at {model_path}")
        except Exception as e:
            print(f"Error loading DistilBERT: {e}")
        
        # Load LSTM
        try:
            lstm_path = AppConfig.LSTM_MODEL_PATH
            vocab_path = AppConfig.VOCAB_LSTM_PATH
            
            if lstm_path.exists() and vocab_path.exists():
                # Load vocabulary
                with open(vocab_path, 'rb') as f:
                    vocab = pickle.load(f)
                
                # Load model with weights_only=False for PyTorch 2.6 compatibility
                checkpoint = torch.load(lstm_path, map_location=self.device, weights_only=False)
                
                # Initialize model with correct parameters from checkpoint
                vocab_size = len(vocab) if hasattr(vocab, '__len__') else checkpoint.get('vocab_size', 10000)
                
                # Check if checkpoint has the actual dimensions stored
                state_dict = checkpoint.get('model_state_dict', checkpoint)
                
                # Infer dimensions from state_dict if available
                if 'embedding.weight' in state_dict:
                    vocab_size, embedding_dim = state_dict['embedding.weight'].shape
                else:
                    embedding_dim = checkpoint.get('embedding_dim', 128)
                
                if 'lstm.weight_ih_l0' in state_dict:
                    # For bidirectional LSTM: weight_ih_l0 shape is (4*hidden_dim, embedding_dim)
                    hidden_dim = state_dict['lstm.weight_ih_l0'].shape[0] // 4
                else:
                    hidden_dim = checkpoint.get('hidden_dim', 256)
                
                num_layers = checkpoint.get('num_layers', 2)
                dropout = checkpoint.get('dropout', 0.3)
                
                model = LSTMSentimentModel(
                    vocab_size=vocab_size,
                    embedding_dim=embedding_dim,
                    hidden_dim=hidden_dim,
                    num_layers=num_layers,
                    dropout=dropout
                )
                
                # Load state dict, handling architecture mismatches
                try:
                    model.load_state_dict(state_dict, strict=False)
                except Exception as load_err:
                    print(f"Warning loading LSTM state dict: {load_err}")
                    # Try loading only matching keys
                    model_dict = model.state_dict()
                    pretrained_dict = {k: v for k, v in state_dict.items() if k in model_dict and model_dict[k].shape == v.shape}
                    model_dict.update(pretrained_dict)
                    model.load_state_dict(model_dict)
                
                model.to(self.device)
                model.eval()
                
                self.models['lstm'] = {
                    'model': model,
                    'vocab': vocab
                }
                print("✓ LSTM loaded")
            else:
                print(f"⚠ LSTM model files not found")
        except Exception as e:
            print(f"Error loading LSTM: {e}")
        
        # Load Logistic Regression
        try:
            lr_path = AppConfig.LOGISTIC_MODEL_PATH
            if lr_path.exists():
                import joblib
                # Try joblib first (often used for sklearn models)
                try:
                    self.models['logistic'] = joblib.load(lr_path)
                    print("✓ Logistic Regression loaded (joblib)")
                except Exception as joblib_err:
                    print(f"⚠ Joblib failed: {joblib_err}")
                    # Try pickle as fallback
                    try:
                        with open(lr_path, 'rb') as f:
                            self.models['logistic'] = pickle.load(f)
                        print("✓ Logistic Regression loaded (pickle)")
                    except Exception as pickle_err:
                        print(f"⚠ Pickle also failed: {pickle_err}")
            else:
                print(f"⚠ Logistic Regression model not found at {lr_path}")
        except Exception as e:
            print(f"Error loading Logistic Regression: {e}")
        
        # Load Random Forest
        try:
            rf_path = AppConfig.RANDOM_FOREST_MODEL_PATH
            if rf_path.exists():
                import joblib
                # Try joblib first (often used for sklearn models)
                try:
                    self.models['random_forest'] = joblib.load(rf_path)
                    print("✓ Random Forest loaded (joblib)")
                except Exception as joblib_err:
                    print(f"⚠ Joblib failed: {joblib_err}")
                    # Try pickle as fallback
                    try:
                        with open(rf_path, 'rb') as f:
                            self.models['random_forest'] = pickle.load(f)
                        print("✓ Random Forest loaded (pickle)")
                    except Exception as pickle_err:
                        print(f"⚠ Pickle also failed: {pickle_err}")
            else:
                print(f"⚠ Random Forest model not found at {rf_path}")
        except Exception as e:
            print(f"Error loading Random Forest: {e}")
    
    def _preprocess_text_lstm(self, text, vocab, max_length=200):
        """Preprocess text for LSTM model"""
        # Simple tokenization
        tokens = text.lower().split()
        
        # Convert to indices
        if hasattr(vocab, 'get_stoi'):
            # torchtext vocab
            indices = [vocab.get_stoi().get(token, vocab.get_stoi().get('<unk>', 1)) for token in tokens]
        elif isinstance(vocab, dict):
            # dictionary vocab
            indices = [vocab.get(token, vocab.get('<unk>', 1)) for token in tokens]
        else:
            # Assume it's a simple word to index mapping
            indices = [vocab.get(token, 1) for token in tokens]
        
        # Pad or truncate
        if len(indices) < max_length:
            indices = indices + [0] * (max_length - len(indices))
        else:
            indices = indices[:max_length]
        
        return torch.tensor([indices], dtype=torch.long).to(self.device)
    
    def predict_sentiment(self, text, model_name='distilbert'):
        """
        Predict sentiment for given text using specified model
        
        Args:
            text: Input text to analyze
            model_name: Model to use ('distilbert', 'lstm', 'logistic', 'random_forest')
        
        Returns:
            Dictionary with prediction results
        """
        start_time = time.time()
        
        # Validate text quality - filter garbage/irrelevant text
        if self._is_garbage_text(text):
            return {
                'label': 'Neutral',
                'score': 0.5,
                'time': time.time() - start_time,
                'model': model_name,
                'warning': 'Text appears to be irrelevant or garbage'
            }
        
        try:
            if model_name == 'distilbert' and 'distilbert' in self.models:
                return self._predict_distilbert(text, start_time)
            
            elif model_name == 'lstm' and 'lstm' in self.models:
                return self._predict_lstm(text, start_time)
            
            elif model_name == 'logistic' and 'logistic' in self.models:
                return self._predict_sklearn(text, 'logistic', start_time)
            
            elif model_name == 'random_forest' and 'random_forest' in self.models:
                return self._predict_sklearn(text, 'random_forest', start_time)
            
            else:
                # Fallback: try any available model
                for available_model in ['distilbert', 'lstm', 'logistic', 'random_forest']:
                    if available_model in self.models:
                        print(f"Model {model_name} not available, using {available_model}")
                        return self.predict_sentiment(text, available_model)
                
                return {
                    'label': 'Neutral',
                    'score': 0.5,
                    'time': time.time() - start_time,
                    'error': f'Model {model_name} not loaded'
                }
        
        except Exception as e:
            print(f"Error in prediction: {e}")
            return {
                'label': 'Error',
                'score': 0.5,
                'time': time.time() - start_time,
                'error': str(e)
            }
    
    def _predict_distilbert(self, text, start_time):
        """Predict using DistilBERT"""
        model_dict = self.models['distilbert']
        tokenizer = model_dict['tokenizer']
        model = model_dict['model']
        
        # Tokenize
        inputs = tokenizer(
            text,
            return_tensors='pt',
            truncation=True,
            padding=True,
            max_length=512
        ).to(self.device)
        
        # Predict
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)
            prediction = torch.argmax(probs, dim=1).item()
            confidence = probs[0][prediction].item()
            
            # Calculate entropy: -sum(p * log(p)) - measures uncertainty
            entropy = -(probs[0][0] * torch.log2(probs[0][0] + 1e-10) + 
                       probs[0][1] * torch.log2(probs[0][1] + 1e-10)).item()
        
        return {
            'label': 'Positive' if prediction == 1 else 'Negative',
            'score': confidence,
            'entropy': entropy,
            'prob_negative': probs[0][0].item(),
            'prob_positive': probs[0][1].item(),
            'time': time.time() - start_time,
            'model': 'DistilBERT'
        }
    
    def _predict_lstm(self, text, start_time):
        """Predict using LSTM"""
        model_dict = self.models['lstm']
        model = model_dict['model']
        vocab = model_dict['vocab']
        
        # Preprocess
        input_tensor = self._preprocess_text_lstm(text, vocab)
        
        # Predict
        with torch.no_grad():
            output = model(input_tensor)
            score = output.item()
        
        # LSTM outputs a sigmoid score between 0 and 1
        # score > 0.5 = Positive, score <= 0.5 = Negative
        # Convert to probabilities for both classes
        prob_positive = score
        prob_negative = 1 - score
        
        # Calculate entropy
        entropy = -(prob_negative * np.log2(prob_negative + 1e-10) + 
                   prob_positive * np.log2(prob_positive + 1e-10))
        
        return {
            'label': 'Positive' if score > 0.5 else 'Negative',
            'score': score,
            'entropy': entropy,
            'prob_negative': prob_negative,
            'prob_positive': prob_positive,
            'time': time.time() - start_time,
            'model': 'LSTM'
        }
    
    def _predict_sklearn(self, text, model_name, start_time):
        """Predict using sklearn models (Logistic Regression or Random Forest)"""
        pipeline = self.models[model_name]
        
        # Predict
        prediction = pipeline.predict([text])[0]
        
        # Get probability if available
        if hasattr(pipeline, 'predict_proba'):
            proba = pipeline.predict_proba([text])[0]
            # Get confidence for the predicted class
            # proba[0] = probability of class 0 (Negative)
            # proba[1] = probability of class 1 (Positive)
            confidence = proba[1] if prediction == 1 else proba[0]
            
            # Calculate entropy
            entropy = -(proba[0] * np.log2(proba[0] + 1e-10) + 
                       proba[1] * np.log2(proba[1] + 1e-10))
            
            prob_negative = proba[0]
            prob_positive = proba[1]
        else:
            confidence = 0.85  # Default confidence for models without probability
            entropy = 0.5  # Default entropy
            prob_negative = 0.15 if prediction == 1 else 0.85
            prob_positive = 0.85 if prediction == 1 else 0.15
        
        return {
            'label': 'Positive' if prediction == 1 else 'Negative',
            'score': confidence,
            'entropy': entropy,
            'prob_negative': prob_negative,
            'prob_positive': prob_positive,
            'time': time.time() - start_time,
            'model': model_name.replace('_', ' ').title()
        }
    
    def _is_garbage_text(self, text):
        """Detect if text is garbage/irrelevant (random characters, keyboard mashing, etc.)"""
        import re
        
        # Remove whitespace for analysis
        cleaned = text.strip()
        
        # Too short to be meaningful
        if len(cleaned) < 5:
            return True
        
        # Check for excessive repeated characters (e.g., "aaaaaa", "111111")
        if re.search(r'(.)\1{4,}', cleaned):
            return True
        
        # Check ratio of consonants without vowels (random keyboard mashing)
        # Remove spaces and count vowels
        no_space = cleaned.replace(' ', '')
        if len(no_space) > 5:
            vowel_count = sum(1 for c in no_space.lower() if c in 'aeiouáéíóúàèìòùäëïöü')
            vowel_ratio = vowel_count / len(no_space)
            # Most languages have at least 25% vowels; less suggests garbage
            if vowel_ratio < 0.15:
                return True
        
        # Check for excessive single-character "words" (e.g., "a s d f g h")
        words = cleaned.split()
        if len(words) >= 4:
            single_char_words = sum(1 for w in words if len(w) == 1)
            if single_char_words / len(words) > 0.5:
                return True
        
        # Check for patterns like "sdf st gf dge" - many short fragments
        if len(words) >= 4:
            short_words = sum(1 for w in words if len(w) <= 3)
            if short_words / len(words) > 0.7:
                # Most short words could be garbage
                # Double-check: do they form recognizable patterns?
                recognizable = sum(1 for w in words if w.lower() in ['the', 'and', 'but', 'for', 'not', 'are', 'was', 'you', 'all', 'can', 'had', 'her', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'one', 'our', 'out', 'say', 'she', 'too', 'two', 'use', 'way', 'who', 'yes', 'yet'])
                if recognizable < 2:
                    return True
        
        return False
    
    def get_available_models(self):
        """Return list of loaded models"""
        return list(self.models.keys())
    
    def get_model_info(self):
        """Return information about all models"""
        return AppConfig.get_model_info()
