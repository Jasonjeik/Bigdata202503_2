#!/usr/bin/env python3
"""
Quick inference test for sentiment analysis
"""
import sys
from pathlib import Path

# Add dashboard to path
sys.path.insert(0, str(Path(__file__).parent / 'dashboard'))

from utils.models import ModelManager
from utils.language import detect_language, translate_to_english

def test_inference(text):
    print(f"\n{'='*60}")
    print(f"TEST: Sentiment Analysis")
    print(f"{'='*60}")
    print(f"Input text: {text}")
    
    # Initialize model manager
    mm = ModelManager()
    
    # Detect language and translate
    detected_lang = detect_language(text)
    translated_text, was_translated, translation_model = translate_to_english(text, detected_lang)
    
    print(f"\nLanguage detected: {detected_lang}")
    if was_translated:
        print(f"Translated to English: {translated_text}")
        print(f"Translation model: {translation_model}")
    else:
        print("No translation needed (already English)")
    
    # Test all models
    models = ['distilbert', 'lstm', 'logistic', 'random_forest']
    
    print(f"\n{'='*60}")
    print("MODEL PREDICTIONS:")
    print(f"{'='*60}")
    
    for model_name in models:
        print(f"\n--- {model_name.upper().replace('_', ' ')} ---")
        result = mm.predict_sentiment(translated_text, model_name)
        
        print(f"Prediction: {result['label']}")
        print(f"Confidence: {result['score']:.4f} ({result['score']*100:.2f}%)")
        
        if 'prob_positive' in result and 'prob_negative' in result:
            print(f"Prob Positive: {result['prob_positive']:.4f} ({result['prob_positive']*100:.2f}%)")
            print(f"Prob Negative: {result['prob_negative']:.4f} ({result['prob_negative']*100:.2f}%)")
        
        if 'entropy' in result:
            print(f"Entropy: {result['entropy']:.4f}")
        
        if 'time' in result:
            print(f"Processing time: {result['time']:.3f}s")
        
        # Show model_type for DistilBERT
        if model_name == 'distilbert' and 'model_type' in result:
            print(f"Model type: {result['model_type']}")
        
        # Show debug info if available
        if 'debug' in result and result['debug']:
            print(f"Debug info: {result['debug']}")
    
    print(f"\n{'='*60}")

if __name__ == "__main__":
    test_text = "Excelente película me gustó mucho"
    test_inference(test_text)
