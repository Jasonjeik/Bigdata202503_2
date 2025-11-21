"""Language detection and translation utilities.

This module provides:
- detect_language(text): returns ISO 639-1 code (e.g., 'en', 'es').
- translate_to_english(text, source_lang): translates text to English if source_lang != 'en'.

Implementation details:
- Language detection with langdetect (fast, lightweight).
- Translation via Hugging Face transformers models (Helsinki-NLP opus-mt-* to English).
  Models are loaded lazily and cached in MEMORY.
- Fallback: if language unsupported or translation fails, returns original text.

Supported language models mapping kept deliberately small for demo performance.
Extend LANGUAGE_MODEL_MAP as needed.
"""
from functools import lru_cache
from typing import Tuple, Optional

def detect_language(text: str) -> str:
    """Detect language with multiple attempts for reliability.
    
    langdetect is non-deterministic, so we run it multiple times
    and take the most common result.
    """
    try:
        from langdetect import detect, detect_langs
        from collections import Counter
        
        # langdetect can fail on very short strings; guard minimal length
        cleaned = text.strip()
        if len(cleaned) < 5:
            return 'en'  # assume English for very short snippets
        
        # Try detect_langs first for confidence scores
        try:
            lang_probs = detect_langs(cleaned)
            # Get the language with highest probability
            if lang_probs:
                best_lang = str(lang_probs[0]).split(':')[0]
                confidence = float(str(lang_probs[0]).split(':')[1])
                # If confidence is high enough, use it
                if confidence > 0.7:
                    return best_lang
        except:
            pass
        
        # Fallback: Multiple detections for stability (langdetect is non-deterministic)
        detections = []
        for _ in range(3):
            try:
                detections.append(detect(cleaned))
            except:
                pass
        
        if detections:
            # Return most common detection
            most_common = Counter(detections).most_common(1)[0][0]
            return most_common
        
        return 'en'
    except Exception as e:
        print(f"Language detection error: {e}")
        return 'en'

# Map source language code -> HuggingFace model for translation to English
# Expanded to support more languages including Asian and Middle Eastern languages
LANGUAGE_MODEL_MAP = {
    # European Languages
    'es': 'Helsinki-NLP/opus-mt-es-en',
    'pt': 'Helsinki-NLP/opus-mt-pt-en',
    'fr': 'Helsinki-NLP/opus-mt-fr-en',
    'de': 'Helsinki-NLP/opus-mt-de-en',
    'it': 'Helsinki-NLP/opus-mt-it-en',
    'nl': 'Helsinki-NLP/opus-mt-nl-en',
    'ru': 'Helsinki-NLP/opus-mt-ru-en',
    'pl': 'Helsinki-NLP/opus-mt-pl-en',
    'uk': 'Helsinki-NLP/opus-mt-uk-en',
    'ro': 'Helsinki-NLP/opus-mt-ro-en',
    'sv': 'Helsinki-NLP/opus-mt-sv-en',
    'da': 'Helsinki-NLP/opus-mt-da-en',
    'no': 'Helsinki-NLP/opus-mt-no-en',
    'fi': 'Helsinki-NLP/opus-mt-fi-en',
    
    # Asian Languages
    'zh': 'Helsinki-NLP/opus-mt-zh-en',  # Chinese
    'zh-cn': 'Helsinki-NLP/opus-mt-zh-en',  # Simplified Chinese
    'zh-tw': 'Helsinki-NLP/opus-mt-zh-en',  # Traditional Chinese
    'ja': 'Helsinki-NLP/opus-mt-ja-en',  # Japanese
    'ko': 'Helsinki-NLP/opus-mt-ko-en',  # Korean
    'vi': 'Helsinki-NLP/opus-mt-vi-en',  # Vietnamese
    'th': 'Helsinki-NLP/opus-mt-th-en',  # Thai
    'id': 'Helsinki-NLP/opus-mt-id-en',  # Indonesian
    'ms': 'Helsinki-NLP/opus-mt-ms-en',  # Malay
    
    # Middle Eastern Languages
    'ar': 'Helsinki-NLP/opus-mt-ar-en',  # Arabic
    'he': 'Helsinki-NLP/opus-mt-he-en',  # Hebrew
    'fa': 'Helsinki-NLP/opus-mt-fa-en',  # Persian
    'tr': 'Helsinki-NLP/opus-mt-tr-en',  # Turkish
    
    # Other Languages
    'hi': 'Helsinki-NLP/opus-mt-hi-en',  # Hindi
    'bn': 'Helsinki-NLP/opus-mt-bn-en',  # Bengali
    'cs': 'Helsinki-NLP/opus-mt-cs-en',  # Czech
    'el': 'Helsinki-NLP/opus-mt-el-en',  # Greek
}

# Fallback: Use multilingual model for unsupported languages
MULTILINGUAL_MODEL = 'Helsinki-NLP/opus-mt-mul-en'

@lru_cache(maxsize=20)
def _get_pipeline(model_name: str):
    """Load and cache translation pipeline."""
    from transformers import pipeline
    return pipeline('translation', model=model_name, device=-1)  # CPU

def translate_to_english(text: str, source_lang: str) -> Tuple[str, bool, Optional[str]]:
    """Translate text to English with fallback to multilingual model.

    Returns (translated_text, translated_flag, used_model_name)
    """
    if source_lang == 'en':
        return text, False, None
    
    # Try language-specific model first
    model_name = LANGUAGE_MODEL_MAP.get(source_lang)
    
    # If no specific model, try multilingual model as fallback
    if not model_name:
        model_name = MULTILINGUAL_MODEL
        print(f"Using multilingual model for unsupported language: {source_lang}")
    
    try:
        pipe = _get_pipeline(model_name)
        result = pipe(text, max_length=512)
        translated = result[0]['translation_text']
        return translated, True, model_name
    except Exception as e:
        # If language-specific model failed, try multilingual as last resort
        if model_name != MULTILINGUAL_MODEL:
            try:
                print(f"Fallback to multilingual model for '{source_lang}'")
                pipe = _get_pipeline(MULTILINGUAL_MODEL)
                result = pipe(text, max_length=512)
                translated = result[0]['translation_text']
                return translated, True, MULTILINGUAL_MODEL
            except Exception as e2:
                print(f"Multilingual translation also failed: {str(e2)[:100]}")
        
        # All translation attempts failed; return original text
        print(f"Translation error for '{source_lang}': {str(e)[:100]}")
        return text, False, None

__all__ = ['detect_language', 'translate_to_english']
