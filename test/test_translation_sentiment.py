"""
Test script to verify translation and sentiment analysis pipeline
"""
import sys
from pathlib import Path

# Asegurar que el directorio 'dashboard' esté en PYTHONPATH para importar utils
BASE_DIR = Path(__file__).resolve().parent.parent / 'dashboard'
sys.path.insert(0, str(BASE_DIR))

from utils.language import detect_language, translate_to_english
from utils.models import ModelManager
import time

def test_sentiment_with_translation():
    """Test the full pipeline: detection -> translation -> sentiment"""
    
    print("="*60)
    print("SENTIMENT ANALYSIS WITH TRANSLATION TEST")
    print("="*60)
    
    # Initialize model manager
    print("\n1. Loading models...")
    model_manager = ModelManager()
    print("[OK] Models loaded")
    
    # Test cases: clear negative reviews in different languages
    test_cases = [
        ("es", "Muy mala no la recomiento para nada. Es horrible."),
        ("es", "No me gusto. Fea. Mala para niños"),
        ("it", "Non mi è piaciuto, era brutto"),
        ("de", "Es gefiel mir nicht, es war hässlich."),
        ("ar", "لم يعجبني، كان قبيحًا"),
        ("zh", "我不喜欢它，它很丑。"),
        ("haw", "ʻAʻole au i makemake, he ʻino"),
        ("en", "This movie is terrible and boring. I hate it."),
        ("en", "Awful film, waste of time, do not watch"),
    ]
    
    print("\n2. Testing sentiment predictions...\n")
    
    for expected_lang, text in test_cases:
        print("-" * 60)
        print(f"Original text: {text}")
        
        # Detect language
        detected_lang = detect_language(text)
        print(f"Detected language: {detected_lang} (expected: {expected_lang})")
        
        # Translate if needed
        translated_text, was_translated, model_name = translate_to_english(text, detected_lang)
        if was_translated:
            print(f"Translated to: {translated_text}")
            print(f"Translation model: {model_name}")
        else:
            print("No translation needed (already English)")
        
        # Get sentiment prediction
        text_for_model = translated_text if was_translated else text
        print(f"\nText sent to model: {text_for_model}")
        
        # Test with DistilBERT
        start = time.time()
        result = model_manager.predict_sentiment(text_for_model, 'distilbert')
        elapsed = time.time() - start
        
        print(f"\n[OK] PREDICTION:")
        print(f"  Label: {result['label']}")
        print(f"  Confidence: {result['score']:.4f} ({result['score']*100:.2f}%)")
        print(f"  Time: {elapsed:.3f}s")
        
        # Check if negative review was correctly identified
        if "hate" in text.lower() or "terrible" in text.lower() or "horrible" in text.lower() or "mala" in text.lower() or "fea" in text.lower():
            expected_sentiment = "Negative"
            if result['label'] != expected_sentiment:
                print(f"\n[WARNING] Expected {expected_sentiment} but got {result['label']}")
        
        print()
    
    print("="*60)
    print("TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    test_sentiment_with_translation()
