"""
Database management utilities for MongoDB Atlas
"""
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from config import AppConfig
except ImportError:
    # Fallback for different import scenarios
    import importlib.util
    config_path = Path(__file__).parent.parent / 'config.py'
    spec = importlib.util.spec_from_file_location("config", config_path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    AppConfig = config_module.AppConfig

class DatabaseManager:
    def __init__(self):
        """Initialize MongoDB connection"""
        try:
            self.client = MongoClient(AppConfig.MONGODB_URI, server_api=ServerApi('1'))
            self.db = self.client[AppConfig.DATABASE_NAME]
            
            # Test connection
            self.client.admin.command('ping')
            self.connected = True
            
            # Initialize collections
            self.movies = self.db[AppConfig.MOVIES_COLLECTION]
            self.comments = self.db[AppConfig.COMMENTS_COLLECTION]
            self.reviews = self.db[AppConfig.REVIEWS_COLLECTION]
            
            # Create indexes for better performance
            self._create_indexes()
            
        except Exception as e:
            print(f"Database connection error: {e}")
            self.connected = False
    
    def _create_indexes(self):
        """Create indexes for optimized queries"""
        try:
            # Index on movie title for search
            self.movies.create_index("title")
            
            # Index on genres for filtering
            self.movies.create_index("genres")
            
            # Index on year for sorting
            self.movies.create_index("year")
            
            # Index on reviews timestamp
            self.reviews.create_index("timestamp")
            
        except Exception as e:
            print(f"Index creation warning: {e}")
    
    def is_connected(self):
        """Check if database connection is active"""
        return self.connected
    
    def get_movie_count(self):
        """Get total number of movies in database"""
        try:
            return self.movies.count_documents({})
        except:
            return 0
    
    def search_movies(self, query="", genre=None, sort_by="title", sort_order="asc", limit=50, skip=0):
        """
        Search movies with filters and sorting
        
        Args:
            query: Text search query (searches in title, plot, cast, directors)
            genre: Genre filter
            sort_by: Field to sort by (title, year, rating)
            sort_order: Sort order (asc or desc)
            limit: Maximum results to return
            skip: Number of results to skip (pagination)
        
        Returns:
            List of movie documents
        """
        try:
            filter_query = {}
            
            # Text search - search in multiple fields for better results
            if query:
                # Split query into words for better matching
                words = query.strip().split()
                if len(words) == 1:
                    # Single word - search in title, plot, cast, directors
                    filter_query['$or'] = [
                        {'title': {'$regex': query, '$options': 'i'}},
                        {'plot': {'$regex': query, '$options': 'i'}},
                        {'cast': {'$regex': query, '$options': 'i'}},
                        {'directors': {'$regex': query, '$options': 'i'}}
                    ]
                else:
                    # Multiple words - search each word
                    word_patterns = [{'title': {'$regex': word, '$options': 'i'}} for word in words]
                    filter_query['$or'] = word_patterns
            
            # Genre filter
            if genre and genre != "All Genres":
                filter_query['genres'] = {'$regex': genre, '$options': 'i'}
            
            # Determine sort order
            sort_direction = 1 if sort_order == "asc" else -1
            
            # Map sort_by to actual field
            sort_field_map = {
                'title': 'title',
                'year': 'year',
                'rating': 'imdb.rating',
                'popularity': 'imdb.rating'  # Use rating as popularity proxy
            }
            sort_field = sort_field_map.get(sort_by.lower(), 'title')
            
            # Execute query with sorting
            # Apply sort then skip then limit (safer pagination order)
            movies = list(
                self.movies.find(
                    filter_query,
                    {
                        'title': 1,
                        'year': 1,
                        'genres': 1,
                        'plot': 1,
                        'poster': 1,
                        'imdb.rating': 1,
                        'runtime': 1,
                        'directors': 1,
                        'cast': 1
                    }
                ).sort(sort_field, sort_direction).skip(skip).limit(limit)
            )

            # Fallback: if requesting rating/popularity sort and result unexpectedly empty on first page, retry without sort to avoid blank UI
            if not movies and skip == 0 and sort_field == 'imdb.rating':
                unsorted = list(
                    self.movies.find(
                        filter_query,
                        {
                            'title': 1,
                            'year': 1,
                            'genres': 1,
                            'plot': 1,
                            'poster': 1,
                            'imdb.rating': 1,
                            'runtime': 1,
                            'directors': 1,
                            'cast': 1
                        }
                    ).skip(0).limit(limit)
                )
                movies = unsorted
            
            # Process results
            for movie in movies:
                if 'imdb' in movie and 'rating' in movie['imdb']:
                    movie['rating'] = movie['imdb']['rating']
                else:
                    movie['rating'] = None

            # Custom post-sort to ensure unrated movies always appear at the end
            # MongoDB may place nulls first in descending order; we normalize here.
            if sort_field in ['imdb.rating'] and movies:
                if sort_order == 'desc':
                    # High rating first, None at end
                    movies.sort(key=lambda m: (m['rating'] is None, -(m['rating'] if m['rating'] is not None else 0)))
                else:
                    # Low rating first, None at end
                    movies.sort(key=lambda m: (m['rating'] is None, m['rating'] if m['rating'] is not None else 10**9))
            
            return movies
            
        except Exception as e:
            print(f"Error searching movies: {e}")
            return []

    def count_movies(self, query="", genre=None):
        """Count movies matching filters (used for pagination)."""
        try:
            filter_query = {}
            if query:
                filter_query['title'] = {'$regex': query, '$options': 'i'}
            if genre and genre != "All Genres":
                filter_query['genres'] = {'$regex': genre, '$options': 'i'}
            return self.movies.count_documents(filter_query)
        except Exception as e:
            print(f"Error counting movies: {e}")
            return 0

    def search_movies_precise_title(self, query, genre=None, limit=20):
        """Return top-N movies best matching the title query using fuzzy ranking.

        Steps:
        1. Collect candidate set via regex on title (up to 1000 docs)
        2. If insufficient, broaden using word components
        3. Score each candidate using rapidfuzz similarity (WRatio)
        4. Sort by similarity desc then IMDb rating desc
        5. Return top `limit`
        """
        try:
            from rapidfuzz import fuzz
        except Exception as e:
            print(f"rapidfuzz not available ({e}), falling back to basic search")
            return self.search_movies(query=query, genre=genre, sort_by='title', sort_order='asc', limit=limit)

        try:
            filter_query = {}
            if genre and genre != "All Genres":
                filter_query['genres'] = {'$regex': genre, '$options': 'i'}

            # Primary candidate set: title contains full query
            primary_regex = {'title': {'$regex': query, '$options': 'i'}}
            candidate_filter = {**filter_query, **primary_regex}
            projection = {
                'title': 1,
                'year': 1,
                'genres': 1,
                'imdb.rating': 1
            }
            candidates = list(self.movies.find(candidate_filter, projection).limit(1000))

            # Broaden if very few results
            if len(candidates) < 10:
                words = [w for w in query.split() if len(w) > 2]
                word_or = [{ 'title': {'$regex': w, '$options': 'i'}} for w in words]
                if word_or:
                    broaden_filter = {**filter_query, '$or': word_or}
                    more_candidates = list(self.movies.find(broaden_filter, projection).limit(1000))
                    # Merge by _id
                    existing_ids = {c['_id'] for c in candidates}
                    for m in more_candidates:
                        if m['_id'] not in existing_ids:
                            candidates.append(m)

            # Score and sort
            scored = []
            q_lower = query.lower().strip()
            for m in candidates:
                title = m.get('title', '')
                sim = fuzz.WRatio(q_lower, title.lower())  # 0-100
                rating = None
                if 'imdb' in m and isinstance(m['imdb'], dict) and 'rating' in m['imdb']:
                    rating = m['imdb']['rating']
                scored.append((sim, rating if rating is not None else -1, m))

            scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
            top = [s[2] for s in scored[:limit]]

            # Normalize rating field
            for movie in top:
                if 'imdb' in movie and 'rating' in movie['imdb']:
                    movie['rating'] = movie['imdb']['rating']
                else:
                    movie['rating'] = None
            return top
        except Exception as e:
            print(f"Precise title search error: {e}")
            return []
    
    def get_movie_by_id(self, movie_id):
        """Get a single movie by ID"""
        try:
            from bson import ObjectId
            return self.movies.find_one({'_id': ObjectId(movie_id)})
        except Exception as e:
            print(f"Error getting movie: {e}")
            return None
    
    def get_popular_movies(self, limit=20):
        """Get popular movies based on IMDb rating and number of comments"""
        try:
            # Use aggregation to join with comments and sort
            pipeline = [
                {
                    '$match': {
                        'imdb.rating': {'$exists': True, '$ne': None}
                    }
                },
                {
                    '$lookup': {
                        'from': 'comments',
                        'localField': '_id',
                        'foreignField': 'movie_id',
                        'as': 'comments'
                    }
                },
                {
                    '$addFields': {
                        'comment_count': {'$size': '$comments'},
                        'rating': '$imdb.rating'
                    }
                },
                {
                    '$sort': {
                        'rating': -1,
                        'comment_count': -1
                    }
                },
                {
                    '$limit': limit
                },
                {
                    '$project': {
                        'title': 1,
                        'year': 1,
                        'genres': 1,
                        'plot': 1,
                        'poster': 1,
                        'rating': 1,
                        'comment_count': 1,
                        'directors': 1,
                        'cast': 1
                    }
                }
            ]
            
            return list(self.movies.aggregate(pipeline))
            
        except Exception as e:
            print(f"Error getting popular movies: {e}")
            # Fallback to simple query
            return list(self.movies.find(
                {'imdb.rating': {'$exists': True}},
                {'title': 1, 'year': 1, 'genres': 1, 'poster': 1, 'imdb': 1}
            ).sort('imdb.rating', -1).limit(limit))
    
    def save_review(self, review_data):
        """
        Save a user review to database
        
        Args:
            review_data: Dictionary containing review information
        """
        try:
            review_data['timestamp'] = datetime.now()
            result = self.reviews.insert_one(review_data)
            print(f"✓ Review saved to MongoDB with ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            error_msg = str(e)
            print(f"⚠ Error saving review to MongoDB: {error_msg}")
            
            # Fallback storage if Atlas space quota exceeded OR any other error
            if 'space quota' in error_msg.lower() or 'quota' in error_msg.lower() or 'AtlasError' in error_msg:
                print(f"⚠ MongoDB Atlas space quota exceeded (using {review_data.get('movie_title', 'N/A')})")
                print("💾 Falling back to local file storage...")
                try:
                    from pathlib import Path
                    import json
                    backup_path = Path(__file__).parent.parent / 'local_reviews_backup.jsonl'
                    review_data['timestamp'] = str(datetime.now()) if isinstance(review_data.get('timestamp'), datetime) else review_data.get('timestamp', str(datetime.now()))
                    review_data['storage_fallback'] = 'local_file_quota_exceeded'
                    with open(backup_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps(review_data, default=str) + '\n')
                    print(f"✓ Review stored locally at {backup_path}")
                    return 'local-backup'
                except Exception as fe:
                    print(f"✗ Local backup also failed: {fe}")
                    return None
            return None
    
    def get_reviews(self, movie_id=None, limit=100):
        """Get reviews from MongoDB and local backup, optionally filtered by movie"""
        all_reviews = []
        
        # Try to get from MongoDB first
        try:
            query = {}
            if movie_id:
                query['movie_id'] = movie_id
            
            mongo_reviews = list(self.reviews.find(query).sort('timestamp', -1).limit(limit))
            all_reviews.extend(mongo_reviews)
            print(f"✓ Loaded {len(mongo_reviews)} reviews from MongoDB")
        except Exception as e:
            print(f"⚠ Error getting reviews from MongoDB: {e}")
        
        # Also load from local backup if it exists (for demo when MongoDB is full)
        try:
            from pathlib import Path
            import json
            backup_path = Path(__file__).parent.parent / 'local_reviews_backup.jsonl'
            if backup_path.exists():
                with open(backup_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            try:
                                review = json.loads(line)
                                # Convert timestamp string back to datetime if needed
                                if isinstance(review.get('timestamp'), str):
                                    from dateutil.parser import parse
                                    try:
                                        review['timestamp'] = parse(review['timestamp'])
                                    except:
                                        pass
                                # Filter by movie_id if specified
                                if movie_id is None or str(review.get('movie_id')) == str(movie_id):
                                    all_reviews.append(review)
                            except json.JSONDecodeError:
                                continue
                print(f"✓ Loaded {len(all_reviews) - len(mongo_reviews)} additional reviews from local backup")
        except Exception as e:
            print(f"⚠ Could not load from local backup: {e}")
        
        # Sort by timestamp descending and limit
        try:
            all_reviews.sort(key=lambda x: x.get('timestamp', datetime.min), reverse=True)
        except:
            pass
        
        return all_reviews[:limit]
    
    def get_review_statistics(self):
        """Get aggregated statistics about reviews from MongoDB and local backup"""
        stats = {
            'total_reviews': 0,
            'avg_rating': 0,
            'avg_sentiment': 0,
            'positive_count': 0,
            'negative_count': 0,
            'active_participants': 0
        }
        
        try:
            # Try MongoDB first
            pipeline = [
                {
                    '$group': {
                        '_id': None,
                        'total_reviews': {'$sum': 1},
                        'avg_rating': {'$avg': '$rating'},
                        'avg_sentiment': {'$avg': '$sentiment_score'},
                        'positive_count': {
                            '$sum': {
                                '$cond': [{'$gt': ['$sentiment_score', 0.5]}, 1, 0]
                            }
                        },
                        'negative_count': {
                            '$sum': {
                                '$cond': [{'$lt': ['$sentiment_score', 0.5]}, 1, 0]
                            }
                        }
                    }
                }
            ]
            
            result = list(self.reviews.aggregate(pipeline))
            mongo_stats = result[0] if result else {}
            
            if mongo_stats:
                stats.update(mongo_stats)
                try:
                    # Distinct session identifiers for active participant count
                    active_ids = self.reviews.distinct('session_id')
                    stats['active_participants'] = len([i for i in active_ids if i])
                except Exception as e:
                    print(f"Warning computing active participants: {e}")
                    
        except Exception as e:
            print(f"⚠ Error getting MongoDB statistics: {e}")
        
        # Also count reviews from local backup
        try:
            from pathlib import Path
            import json
            backup_path = Path(__file__).parent.parent / 'local_reviews_backup.jsonl'
            if backup_path.exists():
                local_reviews = []
                with open(backup_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            try:
                                review = json.loads(line)
                                local_reviews.append(review)
                            except:
                                continue
                
                if local_reviews:
                    # Add to totals
                    stats['total_reviews'] += len(local_reviews)
                    
                    # Recalculate averages
                    all_ratings = [r.get('rating', 0) for r in local_reviews if r.get('rating')]
                    all_sentiments = [r.get('sentiment_score', 0.5) for r in local_reviews if r.get('sentiment_score')]
                    
                    if all_ratings:
                        stats['avg_rating'] = (stats.get('avg_rating', 0) * (stats['total_reviews'] - len(local_reviews)) + sum(all_ratings)) / stats['total_reviews']
                    if all_sentiments:
                        stats['avg_sentiment'] = (stats.get('avg_sentiment', 0) * (stats['total_reviews'] - len(local_reviews)) + sum(all_sentiments)) / stats['total_reviews']
                    
                    # Count positive/negative
                    stats['positive_count'] += sum(1 for r in local_reviews if r.get('sentiment_score', 0.5) > 0.5)
                    stats['negative_count'] += sum(1 for r in local_reviews if r.get('sentiment_score', 0.5) < 0.5)
                    
                    # Count unique sessions
                    local_sessions = set(r.get('session_id') for r in local_reviews if r.get('session_id'))
                    stats['active_participants'] += len(local_sessions)
                    
                    print(f"✓ Added {len(local_reviews)} local backup reviews to statistics")
        except Exception as e:
            print(f"⚠ Could not include local backup in statistics: {e}")
        
        return stats if stats['total_reviews'] > 0 else None
    
    def get_trending_movies(self, days=7):
        """Get movies with most recent reviews"""
        try:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=days)
            
            pipeline = [
                {
                    '$match': {
                        'timestamp': {'$gte': cutoff_date}
                    }
                },
                {
                    '$group': {
                        '_id': '$movie_id',
                        'movie_title': {'$first': '$movie_title'},
                        'review_count': {'$sum': 1},
                        'avg_rating': {'$avg': '$rating'},
                        'avg_sentiment': {'$avg': '$sentiment_score'}
                    }
                },
                {
                    '$sort': {'review_count': -1}
                },
                {
                    '$limit': 10
                }
            ]
            
            return list(self.reviews.aggregate(pipeline))
            
        except Exception as e:
            print(f"Error getting trending movies: {e}")
            return []
    
    def clear_all_reviews(self):
        """
        Delete all reviews from the database (admin function for demo reset)
        
        Returns:
            Number of reviews deleted
        """
        try:
            result = self.reviews.delete_many({})
            return result.deleted_count
        except Exception as e:
            print(f"Error clearing reviews: {e}")
            return 0
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
