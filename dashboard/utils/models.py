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
        # Initialize DistilBERT as None for lazy loading
        self.distilbert_model = None
        self.distilbert_tokenizer = None
        # Small registry to avoid repeated warnings
        self._lfs_warned = set()
        print("[ModelManager] Initialized - models will be loaded on demand")
    
    def _is_memory_limited_env(self):
        """Detect if we're in a memory-limited environment like Streamlit Cloud"""
        import os
        # Check for Streamlit Cloud indicators
        if os.getenv('STREAMLIT_SERVER_HEADLESS') == 'true':
            return True
        # Check hostname for common cloud patterns
        try:
            import socket
            hostname = socket.gethostname().lower()
            if any(pattern in hostname for pattern in ['streamlit', 'cloud', 'container', 'docker']):
                return True
        except:
            pass
        # Check available memory (rough estimate)
        try:
            import psutil
            available_gb = psutil.virtual_memory().available / (1024**3)
            if available_gb < 2.0:  # Less than 2GB available
                return True
        except:
            pass
        return False
        # Small registry to avoid repeated warnings
        self._lfs_warned = set()

    def _is_lfs_pointer(self, file_path):
        """Detect if a file is a Git LFS pointer instead of actual weights.

        Git LFS pointer files are tiny text files containing lines:
        version https://git-lfs.github.com/spec/v1
        oid sha256:<hash>
        size <bytes>
        """
        try:
            p = Path(file_path)
            if not p.exists():
                return False
            # Very small size strongly suggests pointer (< 1 KB)
            if p.stat().st_size > 2048:
                return False
            header = p.read_text(errors='ignore')
            return ('git-lfs.github.com/spec' in header and 'oid sha256:' in header and 'size ' in header)
        except Exception:
            return False
    
    def load_distilbert(self):
        """Lazy load DistilBERT only when needed"""
        if self.distilbert_model is None:
            try:
                from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
                from config import AppConfig
                model_path = AppConfig.DISTILBERT_MODEL_PATH
                if model_path.exists():
                    safetensors_file = model_path / 'model.safetensors'
                    if self._is_lfs_pointer(safetensors_file):
                        if safetensors_file not in self._lfs_warned:
                            print(f"[ModelManager] ⚠ Detected Git LFS pointer (no pesos reales) en {safetensors_file}. Ejecuta 'git lfs pull' antes de usar el modelo.")
                            self._lfs_warned.add(safetensors_file)
                        # Abort local load so fallback remoto pueda intentar
                        raise RuntimeError("DistilBERT local LFS pointer detected")
                    print("[ModelManager] Loading DistilBERT (local fine-tuned)...)")
                    try:
                        tokenizer = AutoTokenizer.from_pretrained(str(model_path))
                        model = AutoModelForSequenceClassification.from_pretrained(
                            str(model_path),
                            low_cpu_mem_usage=True
                        )
                        self.distilbert_model = TextClassificationPipeline(
                            task="sentiment-analysis",
                            model=model,
                            tokenizer=tokenizer,
                            device=-1,
                            top_k=None,
                            truncation=True,
                            max_length=512
                        )
                        print("[ModelManager] ✓ DistilBERT local cargado")
                    except Exception as inner:
                        print(f"[ModelManager] ⚠ Fallo carga local DistilBERT: {inner}")
                        raise inner
                else:
                    print(f"[ModelManager] ⚠ Ruta DistilBERT no existe: {model_path}")
                    return None
            except Exception as e:
                error_msg = str(e)
                if "header too large" in error_msg or "deserializing header" in error_msg:
                    print(f"[ModelManager] ⚠ Memoria insuficiente para modelo local DistilBERT: {error_msg}")
                    print("[ModelManager] Intentando modelo público ligero como respaldo...")
                    try:
                        from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
                        model_id = "distilbert-base-uncased-finetuned-sst-2-english"
                        tokenizer = AutoTokenizer.from_pretrained(model_id)
                        model = AutoModelForSequenceClassification.from_pretrained(model_id, low_cpu_mem_usage=True)
                        self.distilbert_model = TextClassificationPipeline(
                            task="sentiment-analysis",
                            model=model,
                            tokenizer=tokenizer,
                            device=-1,
                            top_k=None,
                            truncation=True,
                            max_length=512
                        )
                        print("[ModelManager] ✓ DistilBERT público cargado (respaldo)")
                    except Exception as bk:
                        print(f"[ModelManager] ⚠ Fallo también modelo público: {bk}")
                        self.distilbert_model = None
                else:
                    print(f"[ModelManager] Error loading DistilBERT: {error_msg}")
                self.distilbert_model = None
                return None
        return self.distilbert_model
    
    def _load_model(self, model_name):
        """Load a specific model on demand (except DistilBERT which uses lazy loading)"""
        if model_name in self.models:
            return  # Already loaded
        
        print(f"[ModelManager] Loading {model_name}...")
        
        try:
            from config import AppConfig
        except ImportError:
            import importlib.util
            config_path = Path(__file__).parent.parent / 'config.py'
            spec = importlib.util.spec_from_file_location("config", config_path)
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)
            AppConfig = config_module.AppConfig
        
        # Skip DistilBERT - it uses lazy loading now
        if model_name == 'distilbert':
            print("[ModelManager] DistilBERT uses lazy loading - will load when first used")
            return
        
        elif model_name == 'lstm':
            try:
                lstm_path = AppConfig.LSTM_MODEL_PATH
                vocab_path = AppConfig.VOCAB_LSTM_PATH
                if lstm_path.exists() and vocab_path.exists():
                    if self._is_lfs_pointer(lstm_path):
                        if lstm_path not in self._lfs_warned:
                            print(f"[ModelManager] ⚠ LSTM .pth es un puntero Git LFS en {lstm_path}. Ejecuta 'git lfs pull' para descargar pesos.")
                            self._lfs_warned.add(lstm_path)
                        raise RuntimeError("LSTM weights missing (LFS pointer)")
                    with open(vocab_path, 'rb') as f:
                        vocab = pickle.load(f)
                    checkpoint = None
                    try:
                        checkpoint = torch.load(lstm_path, map_location=self.device, weights_only=False)
                    except Exception as primary_err:
                        print(f"[ModelManager] ⚠ torch.load fallo LSTM: {primary_err}. Intentando pickle...")
                        try:
                            with open(lstm_path, 'rb') as fck:
                                checkpoint = pickle.load(fck)
                        except Exception as pk_err:
                            print(f"[ModelManager] ⚠ pickle fallo LSTM: {pk_err}. Intentando joblib...")
                            try:
                                import joblib
                                checkpoint = joblib.load(lstm_path)
                            except Exception as jb_err:
                                print(f"[ModelManager] ❌ joblib fallo LSTM: {jb_err}")
                    if isinstance(checkpoint, nn.Module):
                        model = checkpoint
                        model.to(self.device)
                        model.eval()
                        self.models['lstm'] = {'model': model, 'vocab': vocab}
                        print("✓ LSTM loaded (direct module)")
                        return
                    if isinstance(checkpoint, dict):
                        state_dict = checkpoint.get('model_state_dict', checkpoint)
                    else:
                        print("⚠ Formato LSTM inesperado, usando defaults")
                        state_dict = {}
                    if 'embedding.weight' in state_dict:
                        vocab_size, embedding_dim = state_dict['embedding.weight'].shape
                    else:
                        vocab_size = len(vocab) if hasattr(vocab, '__len__') else 10000
                        embedding_dim = 128
                    if 'lstm.weight_ih_l0' in state_dict:
                        hidden_dim = state_dict['lstm.weight_ih_l0'].shape[0] // 4
                    else:
                        hidden_dim = 256
                    num_layers = checkpoint.get('num_layers', 2) if isinstance(checkpoint, dict) else 2
                    dropout = checkpoint.get('dropout', 0.3) if isinstance(checkpoint, dict) else 0.3
                    model = LSTMSentimentModel(vocab_size=vocab_size, embedding_dim=embedding_dim, hidden_dim=hidden_dim, num_layers=num_layers, dropout=dropout)
                    try:
                        model.load_state_dict(state_dict, strict=False)
                    except Exception as load_err:
                        print(f"Warning parcial LSTM: {load_err}")
                        model_dict = model.state_dict()
                        pretrained_dict = {k: v for k, v in state_dict.items() if k in model_dict and model_dict[k].shape == v.shape}
                        model_dict.update(pretrained_dict)
                        model.load_state_dict(model_dict)
                    model.to(self.device)
                    model.eval()
                    self.models['lstm'] = {'model': model, 'vocab': vocab}
                    print("✓ LSTM loaded")
                else:
                    print("⚠ Archivos LSTM faltan")
            except Exception as e:
                print(f"Error loading LSTM: {e}")
                raise
        
        elif model_name == 'logistic':
            try:
                lr_path = AppConfig.LOGISTIC_MODEL_PATH
                if lr_path.exists():
                    import joblib
                    try:
                        self.models['logistic'] = joblib.load(lr_path)
                        print("✓ Logistic Regression loaded")
                    except Exception as joblib_err:
                        print(f"⚠ Joblib failed: {joblib_err}")
                        # Try pickle as fallback
                        try:
                            with open(lr_path, 'rb') as f:
                                self.models['logistic'] = pickle.load(f)
                            print("✓ Logistic Regression loaded (pickle)")
                        except Exception as pickle_err:
                            print(f"⚠ Pickle also failed: {pickle_err}")
                            raise
                else:
                    print(f"⚠ Logistic Regression model not found at {lr_path}")
            except Exception as e:
                print(f"Error loading Logistic Regression: {e}")
                raise
        
        elif model_name == 'random_forest':
            try:
                rf_path = AppConfig.RANDOM_FOREST_MODEL_PATH
                if rf_path.exists():
                    import joblib
                    try:
                        self.models['random_forest'] = joblib.load(rf_path)
                        print("✓ Random Forest loaded")
                    except Exception as joblib_err:
                        print(f"⚠ Joblib failed: {joblib_err}")
                        # Try pickle as fallback
                        try:
                            with open(rf_path, 'rb') as f:
                                self.models['random_forest'] = pickle.load(f)
                            print("✓ Random Forest loaded (pickle)")
                        except Exception as pickle_err:
                            print(f"⚠ Pickle also failed: {pickle_err}")
                            raise
                else:
                    print(f"⚠ Random Forest model not found at {rf_path}")
            except Exception as e:
                print(f"Error loading Random Forest: {e}")
                raise
    
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
        
        # In memory-limited environments, redirect heavy models to lighter alternatives
        if self._is_memory_limited_env():
            if model_name == 'distilbert':
                # Try logistic first, then random_forest, then fallback to remote DistilBERT
                light_models = ['logistic', 'random_forest']
                for light_model in light_models:
                    try:
                        result = self.predict_sentiment(text, light_model)
                        result['warning'] = f'Using {light_model} instead of DistilBERT (memory limited environment)'
                        return result
                    except:
                        continue
                # If sklearn models fail, try remote DistilBERT
                try:
                    result = self.predict_sentiment(text, 'distilbert_remote')
                    result['warning'] = 'Using remote DistilBERT (memory limited environment)'
                    return result
                except:
                    pass
            elif model_name == 'lstm':
                # Redirect LSTM to sklearn models in memory-limited env
                light_models = ['logistic', 'random_forest']
                for light_model in light_models:
                    try:
                        result = self.predict_sentiment(text, light_model)
                        result['warning'] = f'Using {light_model} instead of LSTM (memory limited environment)'
                        return result
                    except:
                        continue
        
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
            # Load model if not already loaded
            if model_name == 'distilbert':
                # Use lazy loading for DistilBERT
                if self.distilbert_model is None:
                    self.load_distilbert()
                    if self.distilbert_model is None:
                        # Fallback to another model if DistilBERT fails to load
                        fallback_models = ['logistic', 'random_forest', 'lstm']
                        for fallback in fallback_models:
                            try:
                                result = self.predict_sentiment(text, fallback)
                                result['warning'] = 'DistilBERT unavailable, using fallback model'
                                return result
                            except:
                                continue
                        # Heuristic fallback if no ML models load
                        lower = text.lower()
                        neg_words = ['terrible','horrible','awful','hate','mala','fea','boring','ugly','bad','waste']
                        pos_words = ['excellent','great','amazing','fantastic','love','buena','bonita','awesome']
                        if any(w in lower for w in neg_words):
                            return {
                                'label': 'Negative',
                                'score': 0.75,
                                'time': time.time() - start_time,
                                'model': 'heuristic',
                                'warning': 'Heuristic negative (models unavailable)'
                            }
                        if any(w in lower for w in pos_words):
                            return {
                                'label': 'Positive',
                                'score': 0.75,
                                'time': time.time() - start_time,
                                'model': 'heuristic',
                                'warning': 'Heuristic positive (models unavailable)'
                            }
                        return {
                            'label': 'Neutral',
                            'score': 0.5,
                            'time': time.time() - start_time,
                            'model': 'heuristic',
                            'warning': 'Heuristic neutral (models unavailable)'
                        }
            elif model_name not in self.models:
                try:
                    self._load_model(model_name)
                except Exception as load_error:
                    print(f"Failed to load model {model_name}: {load_error}")
                    # Try fallback models
                    for fallback_model in ['distilbert', 'logistic', 'random_forest', 'lstm']:
                        if fallback_model != model_name and fallback_model in self.models:
                            print(f"Using fallback model {fallback_model}")
                            return self.predict_sentiment(text, fallback_model)
                    return {
                        'label': 'Neutral',
                        'score': 0.5,
                        'time': time.time() - start_time,
                        'error': f'Failed to load model {model_name}: {load_error}'
                    }
            
            if model_name == 'distilbert':
                return self._predict_distilbert(text, start_time)
            
            elif model_name == 'lstm':
                return self._predict_lstm(text, start_time)
            
            elif model_name == 'logistic':
                return self._predict_sklearn(text, 'logistic', start_time)
            
            elif model_name == 'random_forest':
                return self._predict_sklearn(text, 'random_forest', start_time)
            
            else:
                return {
                    'label': 'Neutral',
                    'score': 0.5,
                    'time': time.time() - start_time,
                    'error': f'Unknown model {model_name}'
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
        """Predict using DistilBERT pipeline"""
        model = self.distilbert_model
        
        if model is None:
            return {
                'label': 'Error',
                'score': 0.5,
                'time': time.time() - start_time,
                'error': 'DistilBERT model not loaded'
            }
        
        try:
            # Use pipeline for prediction
            results = model(text)
            
            # Pipeline returns [[{label, score}, ...]] - nested list
            if results and len(results) > 0 and len(results[0]) > 0:
                predictions = results[0]  # Get the first (and only) prediction list
                
                # Find the prediction with highest score
                best_result = max(predictions, key=lambda x: x['score'])
                label = best_result['label']
                score = best_result['score']
                
                # Convert to our format
                # DistilBERT fine-tuned model: LABEL_1 or POSITIVE = Positive sentiment
                # LABEL_0 or NEGATIVE = Negative sentiment
                is_positive = ('POSITIVE' in label.upper() or 'LABEL_1' in label.upper() or 
                              label.upper() == '1' or 'POS' in label.upper())
                
                # Get probabilities for both classes
                pos_result = next((r for r in predictions if 'POSITIVE' in r['label'].upper() or 'LABEL_1' in r['label'].upper() or '1' == r['label'].upper()), None)
                neg_result = next((r for r in predictions if 'NEGATIVE' in r['label'].upper() or 'LABEL_0' in r['label'].upper() or '0' == r['label'].upper()), None)
                
                prob_positive = pos_result['score'] if pos_result else (score if is_positive else 1-score)
                prob_negative = neg_result['score'] if neg_result else (1-score if is_positive else score)
                
                # Calculate entropy
                entropy = -(prob_negative * np.log2(prob_negative + 1e-10) + 
                           prob_positive * np.log2(prob_positive + 1e-10))
                
                return {
                    'label': 'Positive' if is_positive else 'Negative',
                    'score': score,
                    'entropy': entropy,
                    'prob_negative': prob_negative,
                    'prob_positive': prob_positive,
                    'time': time.time() - start_time,
                    'model': 'DistilBERT'
                }
            else:
                return {
                    'label': 'Neutral',
                    'score': 0.5,
                    'time': time.time() - start_time,
                    'error': 'No prediction results from DistilBERT'
                }
                
        except Exception as e:
            return {
                'label': 'Error',
                'score': 0.5,
                'time': time.time() - start_time,
                'error': f'DistilBERT prediction error: {str(e)}'
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
        """Return list of models that can be loaded (files exist)"""
        available = []
        
        try:
            from config import AppConfig
            
            # Check DistilBERT (lazy loaded, but files must exist)
            if AppConfig.DISTILBERT_MODEL_PATH.exists():
                available.append('distilbert')
            
            # Check LSTM
            if AppConfig.LSTM_MODEL_PATH.exists() and AppConfig.VOCAB_LSTM_PATH.exists():
                available.append('lstm')
            
            # Check Logistic Regression
            if AppConfig.LOGISTIC_MODEL_PATH.exists():
                available.append('logistic')
            
            # Check Random Forest
            if AppConfig.RANDOM_FOREST_MODEL_PATH.exists():
                available.append('random_forest')
                
        except Exception as e:
            print(f"Error checking available models: {e}")
            # Fallback: return loaded models plus DistilBERT if it exists
            available = list(self.models.keys())
            if self.distilbert_model is not None:
                available.append('distilbert')
        
        return available
    
    def get_model_info(self):
        """Return information about all models"""
        return AppConfig.get_model_info()
