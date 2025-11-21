#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo de Uso del Analizador de Sentimientos
Aplicación de demostración estudiantil - Big Data 2025-03
Sin propósito comercial - Solo para fines educativos

Este script muestra cómo usar el analizador de sentimientos
de forma programática en tus propios proyectos educativos.
"""

from sentiment_analyzer import SentimentAnalyzer


def main():
    """Ejemplos de uso del analizador de sentimientos"""
    
    print("="*60)
    print("📚 Ejemplos de Uso del Analizador de Sentimientos")
    print("="*60 + "\n")
    
    # Crear instancia del analizador
    analyzer = SentimentAnalyzer()
    
    # Ejemplo 1: Análisis de un solo comentario
    print("📝 Ejemplo 1: Análisis individual")
    print("-"*60)
    
    comment1 = "This is an amazing and wonderful movie"
    result1 = analyzer.analyze_sentiment(comment1)
    
    print(f"Comentario: {result1['text']}")
    print(f"Sentimiento: {result1['sentiment']}")
    print(f"Polaridad: {result1['polarity']:.3f}")
    print(f"Subjetividad: {result1['subjectivity']:.3f}\n")
    
    # Ejemplo 2: Análisis de múltiples comentarios
    print("📝 Ejemplo 2: Análisis por lotes")
    print("-"*60)
    
    comments = [
        "Great movie, loved it!",
        "Terrible film, waste of time",
        "It was okay, nothing special"
    ]
    
    results = analyzer.analyze_batch(comments)
    
    for i, result in enumerate(results, 1):
        print(f"\nComentario {i}: {result['text']}")
        print(f"  → {result['sentiment']} (polaridad: {result['polarity']:.3f})")
    
    # Ejemplo 3: Clasificación y conteo
    print("\n\n📝 Ejemplo 3: Estadísticas de sentimientos")
    print("-"*60)
    
    movie_reviews = [
        "Absolutely brilliant masterpiece",
        "Best movie of the year",
        "Horrible, don't watch it",
        "Disappointing and boring",
        "It's fine, not great not terrible",
        "Amazing cinematography and acting",
        "Waste of money",
        "Pretty good overall"
    ]
    
    results = analyzer.analyze_batch(movie_reviews)
    
    # Contar sentimientos
    positive = sum(1 for r in results if r['sentiment'] == 'POSITIVO')
    negative = sum(1 for r in results if r['sentiment'] == 'NEGATIVO')
    neutral = sum(1 for r in results if r['sentiment'] == 'NEUTRAL')
    
    print(f"\nTotal de reseñas analizadas: {len(results)}")
    print(f"  ✓ Positivas: {positive} ({positive/len(results)*100:.1f}%)")
    print(f"  ✗ Negativas: {negative} ({negative/len(results)*100:.1f}%)")
    print(f"  ○ Neutrales: {neutral} ({neutral/len(results)*100:.1f}%)")
    
    # Calcular polaridad promedio
    avg_polarity = sum(r['polarity'] for r in results) / len(results)
    print(f"\nPolaridad promedio: {avg_polarity:.3f}")
    
    if avg_polarity > 0.1:
        print("→ En general, los comentarios son POSITIVOS")
    elif avg_polarity < -0.1:
        print("→ En general, los comentarios son NEGATIVOS")
    else:
        print("→ En general, los comentarios son NEUTRALES")
    
    print("\n" + "="*60)
    print("✓ Ejemplos completados exitosamente")
    print("="*60)


if __name__ == "__main__":
    main()
