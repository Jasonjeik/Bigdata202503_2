#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis de Sentimiento de Comentarios de Películas
Aplicación de demostración estudiantil - Big Data 2025-03
Sin propósito comercial - Solo para fines educativos

Este script analiza el sentimiento de comentarios sobre películas
utilizando técnicas de procesamiento de lenguaje natural (NLP).
"""

import sys
import argparse
from textblob import TextBlob
from colorama import init, Fore, Style
import warnings

# Suprimir advertencias para una salida más limpia
warnings.filterwarnings('ignore')

# Inicializar colorama para colores en terminal
init(autoreset=True)


class SentimentAnalyzer:
    """
    Clase para análisis de sentimiento de comentarios de películas.
    Implementa métodos educativos simplificados para demostración.
    """
    
    def __init__(self):
        """Inicializa el analizador de sentimientos"""
        self.polarity_threshold_positive = 0.1
        self.polarity_threshold_negative = -0.1
    
    def analyze_sentiment(self, text):
        """
        Analiza el sentimiento de un texto dado.
        
        Args:
            text (str): Comentario a analizar
            
        Returns:
            dict: Diccionario con polaridad, subjetividad y clasificación
        """
        # Analizar con TextBlob (optimizado para inglés)
        # Para simplificación educativa, usamos análisis directo
        blob = TextBlob(text)
        
        # Obtener polaridad (-1 a 1) y subjetividad (0 a 1)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Clasificar sentimiento
        if polarity > self.polarity_threshold_positive:
            sentiment = "POSITIVO"
            color = Fore.GREEN
        elif polarity < self.polarity_threshold_negative:
            sentiment = "NEGATIVO"
            color = Fore.RED
        else:
            sentiment = "NEUTRAL"
            color = Fore.YELLOW
        
        return {
            'text': text,
            'polarity': polarity,
            'subjectivity': subjectivity,
            'sentiment': sentiment,
            'color': color
        }
    
    def print_result(self, result):
        """
        Imprime el resultado del análisis de forma formateada.
        
        Args:
            result (dict): Resultado del análisis
        """
        print("\n" + "="*60)
        print(f"{Fore.CYAN}📝 Comentario analizado:{Style.RESET_ALL}")
        print(f"   {result['text']}")
        print("-"*60)
        print(f"{Fore.CYAN}📊 Resultado del análisis:{Style.RESET_ALL}")
        print(f"   Sentimiento: {result['color']}{result['sentiment']}{Style.RESET_ALL}")
        print(f"   Polaridad: {result['polarity']:.3f} (rango: -1 a +1)")
        print(f"   Subjetividad: {result['subjectivity']:.3f} (rango: 0 a 1)")
        print("="*60 + "\n")
    
    def analyze_batch(self, comments):
        """
        Analiza múltiples comentarios.
        
        Args:
            comments (list): Lista de comentarios a analizar
            
        Returns:
            list: Lista de resultados
        """
        results = []
        for comment in comments:
            result = self.analyze_sentiment(comment)
            results.append(result)
        return results


def get_demo_comments():
    """
    Retorna comentarios de ejemplo para demostración.
    
    Returns:
        list: Lista de comentarios de ejemplo (en inglés para mejor precisión)
    """
    return [
        "This movie is absolutely amazing, the best I've seen this year",
        "I loved every minute, spectacular performances and engaging plot",
        "Excellent movie, highly recommended for the whole family",
        "I didn't like it at all, very boring and completely predictable",
        "Terrible movie, a total waste of time and money",
        "Awful acting, the plot makes no sense whatsoever",
        "The movie is acceptable, nothing extraordinary but entertaining",
        "It has its good and bad moments, overall it's decent",
    ]


def print_welcome():
    """Imprime mensaje de bienvenida"""
    print("\n" + "="*60)
    print(f"{Fore.CYAN}🎬 Analizador de Sentimiento de Comentarios de Películas{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}📚 Aplicación de Demostración Estudiantil{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}⚠️  Sin propósito comercial - Solo fines educativos{Style.RESET_ALL}")
    print("="*60)


def main():
    """Función principal del programa"""
    parser = argparse.ArgumentParser(
        description='Análisis de sentimiento de comentarios de películas (Demo Educativa)',
        epilog='Nota: Esta es una aplicación de demostración para fines educativos únicamente.'
    )
    parser.add_argument(
        'comment',
        nargs='?',
        help='Comentario a analizar'
    )
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Ejecutar demostración con comentarios de ejemplo'
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Modo de análisis por lotes (lee comentarios desde stdin)'
    )
    
    args = parser.parse_args()
    
    # Crear analizador
    analyzer = SentimentAnalyzer()
    
    # Imprimir bienvenida
    print_welcome()
    
    # Modo demostración
    if args.demo:
        print(f"\n{Fore.CYAN}🎯 Ejecutando modo demostración...{Style.RESET_ALL}\n")
        demo_comments = get_demo_comments()
        
        results = analyzer.analyze_batch(demo_comments)
        
        for result in results:
            analyzer.print_result(result)
        
        # Estadísticas
        positive = sum(1 for r in results if r['sentiment'] == 'POSITIVO')
        negative = sum(1 for r in results if r['sentiment'] == 'NEGATIVO')
        neutral = sum(1 for r in results if r['sentiment'] == 'NEUTRAL')
        
        print(f"{Fore.CYAN}📈 Estadísticas:{Style.RESET_ALL}")
        print(f"   Total de comentarios: {len(results)}")
        print(f"   {Fore.GREEN}Positivos: {positive}{Style.RESET_ALL}")
        print(f"   {Fore.RED}Negativos: {negative}{Style.RESET_ALL}")
        print(f"   {Fore.YELLOW}Neutrales: {neutral}{Style.RESET_ALL}\n")
    
    # Modo análisis individual
    elif args.comment:
        result = analyzer.analyze_sentiment(args.comment)
        analyzer.print_result(result)
    
    # Modo por lotes desde stdin
    elif args.batch:
        print(f"{Fore.CYAN}📝 Modo por lotes: Ingrese comentarios (Ctrl+D para terminar):{Style.RESET_ALL}\n")
        comments = []
        try:
            for line in sys.stdin:
                line = line.strip()
                if line:
                    comments.append(line)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⚠️  Análisis interrumpido{Style.RESET_ALL}")
            return
        
        if comments:
            results = analyzer.analyze_batch(comments)
            for result in results:
                analyzer.print_result(result)
    
    # Sin argumentos: mostrar ayuda
    else:
        parser.print_help()
        print(f"\n{Fore.YELLOW}💡 Ejemplos de uso:{Style.RESET_ALL}")
        print('   python sentiment_analyzer.py "I loved this movie"')
        print('   python sentiment_analyzer.py --demo')
        print('   echo "Great movie" | python sentiment_analyzer.py --batch\n')


if __name__ == "__main__":
    main()
