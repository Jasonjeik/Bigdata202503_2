"""
Movie catalog and search utilities
"""
import requests
from typing import List, Dict
import sys
from pathlib import Path

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

class MovieCatalog:
    """Handle movie search and poster retrieval"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.omdb_api_key = AppConfig.OMDB_API_KEY
        self.poster_cache = {}
    
    def search_movies(self, query="", genre_filter="All Genres", sort_by="title", sort_order="asc", limit=20, page=1, use_pagination=False):
        """Unified search interface.

        Behavior:
        - If a query is provided: perform precise title matching (top 20 ranked results).
        - If no query and pagination requested: return page of movies (20 per page) using sorting.
        - Else: fallback to basic search limited to `limit`.
        """
        genre = None if genre_filter == "All Genres" else genre_filter

        if query:
            # Precise title-based search (always limit=20)
            return self.db_manager.search_movies_precise_title(query=query, genre=genre, limit=20)

        if use_pagination:
            skip = (max(page, 1) - 1) * limit
            return self.db_manager.search_movies(query="", genre=genre, sort_by=sort_by, sort_order=sort_order, limit=limit, skip=skip)

        return self.db_manager.search_movies(query="", genre=genre, sort_by=sort_by, sort_order=sort_order, limit=limit)

    def count_movies(self, query="", genre_filter="All Genres"):
        """Count total movies for pagination (ignores fuzzy ranking scenario)."""
        genre = None if genre_filter == "All Genres" else genre_filter
        return self.db_manager.count_movies(query=query, genre=genre)
    
    def get_poster_url(self, movie_title, year=None):
        """
        Get movie poster URL from OMDB API with validation or use placeholder
        
        Args:
            movie_title: Title of the movie
            year: Release year (optional, helps with accuracy)
        
        Returns:
            URL string for validated poster image or placeholder
        """
        # Check cache first
        cache_key = f"{movie_title}_{year}"
        if cache_key in self.poster_cache:
            return self.poster_cache[cache_key]
        
        # Try OMDB API if key is available
        if not self.omdb_api_key:
            # Use demo API key if not configured
            self.omdb_api_key = 'bbe61596'
        
        if self.omdb_api_key:
            try:
                # First try with year if provided
                if year:
                    params = {
                        'apikey': self.omdb_api_key,
                        't': movie_title,
                        'y': str(year)
                    }
                    response = requests.get('http://www.omdbapi.com/', params=params, timeout=5)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        if data.get('Response') == 'True' and data.get('Poster'):
                            poster_url = data['Poster']
                            
                            # Validate poster URL (not 'N/A' and is a valid URL)
                            if poster_url != 'N/A' and self._validate_poster_url(poster_url):
                                self.poster_cache[cache_key] = poster_url
                                return poster_url
                
                # Try without year as fallback
                params = {
                    'apikey': self.omdb_api_key,
                    't': movie_title
                }
                response = requests.get('http://www.omdbapi.com/', params=params, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get('Response') == 'True' and data.get('Poster'):
                        poster_url = data['Poster']
                        
                        # Validate poster URL
                        if poster_url != 'N/A' and self._validate_poster_url(poster_url):
                            self.poster_cache[cache_key] = poster_url
                            return poster_url
                    
            except Exception as e:
                print(f"Error fetching poster for '{movie_title}': {e}")
        
        # Fallback to placeholder
        placeholder_url = self._generate_placeholder_poster(movie_title)
        self.poster_cache[cache_key] = placeholder_url
        return placeholder_url
    
    def _validate_poster_url(self, url):
        """
        Validate that poster URL is accessible and returns valid image.
        If the image is not found (status != 200), fallback to MovieLover logo.
        """
        try:
            if not url or not url.startswith(('http://', 'https://')):
                return False
            # Only validate for OMDB/Amazon URLs
            if 'm.media-amazon.com' in url or 'ia.media-imdb.com' in url:
                head_response = requests.head(url, timeout=3, allow_redirects=True)
                if head_response.status_code == 200:
                    content_type = head_response.headers.get('Content-Type', '')
                    return 'image' in content_type.lower()
                else:
                    # If image not found, fallback
                    print(f"Poster not found (status {head_response.status_code}): {url}")
                    return False
            # For other URLs, assume valid if format is correct
            return True
        except Exception as e:
            print(f"Poster validation failed for {url}: {e}")
            return False
    
    def _generate_placeholder_poster(self, title):
        """
        Generate a placeholder poster URL using MovieLover logo
        
        Args:
            title: Movie title
        
        Returns:
            URL for placeholder image (MovieLover logo)
        """
        # Use MovieLover logo as fallback for missing/failed posters
        return "https://freesvg.org/img/Movie-Projector-Icon.png"
    
    def get_movie_details(self, movie_id):
        """Get detailed information for a specific movie"""
        return self.db_manager.get_movie_by_id(movie_id)
    
    def get_popular_movies(self, limit=20):
        """Get most popular movies"""
        return self.db_manager.get_popular_movies(limit=limit)
    
    def get_genres(self):
        """Get list of all available genres"""
        # Standard movie genres
        return [
            "All Genres",
            "Action",
            "Adventure",
            "Animation",
            "Comedy",
            "Crime",
            "Documentary",
            "Drama",
            "Fantasy",
            "Horror",
            "Mystery",
            "Romance",
            "Sci-Fi",
            "Thriller",
            "Western"
        ]
