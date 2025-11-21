"""
Professional Movie Sentiment Analysis Dashboard
Interactive application for real-time audience engagement and sentiment prediction
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.database import DatabaseManager
from utils.models import ModelManager
from utils.visualizations import create_sentiment_gauge, create_model_comparison_chart, create_timeline_chart, create_rating_distribution
from utils.movie_search import MovieCatalog
from utils.language import detect_language, translate_to_english
from config import AppConfig

# Page configuration
st.set_page_config(
    page_title="MovieLover - AI Sentiment Analysis",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 0.5rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .movie-card {
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: box-shadow 0.3s;
    }
    .movie-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .mini-movie-card {
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 0.5rem;
        margin: 0.3rem 0;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .mini-movie-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        background-color: #4f46e5;
        color: white;
        font-weight: 600;
        border-radius: 0.375rem;
        padding: 0.5rem 1rem;
        border: none;
        transition: background-color 0.2s;
    }
    .stButton>button:hover {
        background-color: #4338ca;
    }
    .star-rating {
        font-size: 2rem;
        color: #fbbf24;
        letter-spacing: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'db_manager' not in st.session_state:
    st.session_state.db_manager = DatabaseManager()
if 'model_manager' not in st.session_state:
    st.session_state.model_manager = ModelManager()
if 'movie_catalog' not in st.session_state:
    st.session_state.movie_catalog = MovieCatalog(st.session_state.db_manager)
if 'user_reviews' not in st.session_state:
    st.session_state.user_reviews = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'session_id' not in st.session_state:
    import uuid
    st.session_state.session_id = str(uuid.uuid4())

# Sidebar navigation
with st.sidebar:
    st.image("https://freesvg.org/img/Movie-Projector-Icon.png", width=80)
    st.title(" MovieLover")
    
    page = st.radio(
        "Select View",
        ["Home", "Movie Catalog", "Live Analytics", "Model Comparison", "Model Architecture"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Model selection
    st.subheader("Model Configuration")
    selected_model = st.selectbox(
        "Primary Model",
        ["DistilBERT (Recommended)", "LSTM Deep Learning", "Logistic Regression", "Random Forest"],
        help="Choose the sentiment analysis model"
    )
    
    st.divider()
    
    # Connection status
    if st.session_state.db_manager.is_connected():
        st.success("Database Connected")
        st.metric("Total Movies", st.session_state.db_manager.get_movie_count())
    else:
        st.error("Database Disconnected")

    try:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/MongoDB_Logo.svg/512px-MongoDB_Logo.svg.png",
            caption="MongoDB Atlas",
            use_container_width=True
        )
        st.image(
            "https://www.northware.mx/wp-content/uploads/2022/09/northware-microsoft-azure-logo.png",
            caption="Microsoft Azure",
            use_container_width=True
        )        
    except Exception as e:
        st.caption(f"Logos no disponibles ({e})")
    
    # Quick stats
    st.divider()
    st.subheader("Session Statistics")
    
    # Get total reviews from database
    total_reviews_db = 0
    if st.session_state.db_manager.is_connected():
        try:
            stats = st.session_state.db_manager.get_review_statistics()
            if stats:
                total_reviews_db = stats.get('total_reviews', 0)
        except:
            pass
    
    st.metric("Total Reviews (All Users)", total_reviews_db)
    st.metric("Your Reviews (This Session)", len(st.session_state.user_reviews))

# Main content area
if page == "Home":
    # Hero section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<p class="main-header"> MovieLover</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">AI-Powered Movie Sentiment Analysis & Reviews</p>', unsafe_allow_html=True)
        
        st.markdown("""
        ### Welcome to MovieLover!
        
        Your intelligent movie companion powered by advanced machine learning.
        Share your passion for cinema:
        
        - **Explore** thousands of movies with stunning posters
        - **Review** movies in any language with instant translation
        - **Discover** sentiment insights using 4 AI models
        - **Compare** model predictions side-by-side
        - **Visualize** trends and top recommendations
        """)
        
        if st.button("Start Exploring Movies", type="primary"):
            st.session_state.current_page = 'catalog'
            st.rerun()
    
    with col2:
        st.info("""
        **Quick Start Guide**
        
        1. Browse the Movie Catalog
        2. Select a movie that interests you
        3. Write your review
        4. See instant sentiment analysis
        5. Explore aggregated insights
        """)

        try:
            import qrcode
            from io import BytesIO
            st.markdown("### Acceso Rápido (QR)")
            app_url = st.session_state.get('app_base_url', 'http://localhost:8501')
            qr = qrcode.QRCode(box_size=4, border=2)
            qr.add_data(app_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buf = BytesIO()
            img.save(buf, format='PNG')
            st.image(buf.getvalue(), caption=f"Escanea para abrir: {app_url}")
        except Exception as e:
            st.caption(f"QR no disponible ({e})")
    
    # Key metrics dashboard
    st.divider()
    st.subheader("Platform Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Movies Available",
            value=st.session_state.db_manager.get_movie_count(),
            delta="Live Database"
        )
    
    with col2:
        # Get total reviews from database
        total_reviews = 0
        if st.session_state.db_manager.is_connected():
            try:
                stats = st.session_state.db_manager.get_review_statistics()
                if stats:
                    total_reviews = stats.get('total_reviews', 0)
            except:
                pass
        
        st.metric(
            label="Total Reviews",
            value=total_reviews,
            delta=f"+{len(st.session_state.user_reviews)} this session"
        )
    
    with col3:
        # Get positive sentiment from database
        positive_pct = 0
        if st.session_state.db_manager.is_connected():
            try:
                stats = st.session_state.db_manager.get_review_statistics()
                if stats and stats.get('total_reviews', 0) > 0:
                    positive_pct = (stats.get('positive_count', 0) / stats['total_reviews']) * 100
            except:
                pass
        
        st.metric(
            label="Positive Sentiment",
            value=f"{positive_pct:.0f}%"
        )
    
    with col4:
        st.metric(
            label="Active Models",
            value="4",
            delta="All Operational"
        )

    with col5:
        active_participants = 0
        if st.session_state.db_manager.is_connected():
            try:
                stats = st.session_state.db_manager.get_review_statistics()
                if stats:
                    active_participants = stats.get('active_participants', 0)
            except:
                pass
        # Fallback: count session IDs from local session reviews if DB empty
        if active_participants == 0 and st.session_state.user_reviews:
            active_participants = 1
        st.metric(
            label="Active Participants",
            value=active_participants
        )

elif page == "Movie Catalog":
    st.markdown('<p class="main-header">MovieLover Catalog</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Discover and review movies from our extensive collection</p>', unsafe_allow_html=True)
    
    # Search and filter section
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        search_query = st.text_input(
            "Search by title, plot, cast, or keywords",
            placeholder="Enter keywords (e.g., 'love', 'action', 'Tom Hanks')...",
            label_visibility="collapsed",
            help="Search for movies by keywords in title, plot, cast, or director"
        )
    
    with col2:
        sort_option = st.selectbox(
            "Sort by",
            ["Year", "Title", "Popularity","Rating"],
            label_visibility="collapsed"
        )
    
    with col3:
        sort_order = st.selectbox(
            "Order",
            ["⬆️ Ascending", "⬇️ Descending"],
            label_visibility="collapsed"
        )
        order = "asc" if sort_order.startswith("⬆️") else "desc"
    
    with col4:
        genre_filter = st.selectbox(
            "Genre",
            ["All Genres", "Action", "Comedy", "Drama", "Thriller", "Romance", "Sci-Fi"],
            label_visibility="collapsed"
        )
    
    # Initialize pagination state
    if 'catalog_page' not in st.session_state:
        st.session_state.catalog_page = 1

    # Reset page when search query changes
    if search_query and st.session_state.catalog_page != 1:
        st.session_state.catalog_page = 1

    use_pagination = not bool(search_query.strip())
    movies = st.session_state.movie_catalog.search_movies(
        query=search_query.strip(),
        genre_filter=genre_filter,
        sort_by=sort_option.lower(),
        sort_order=order,
        limit=20,
        page=st.session_state.catalog_page,
        use_pagination=use_pagination
    )

    # Count total for pagination when browsing
    total_movies = st.session_state.movie_catalog.count_movies(
        query="" if use_pagination else search_query.strip(),
        genre_filter=genre_filter
    ) if use_pagination else len(movies)

    if search_query.strip():
        st.markdown(f"**Top {len(movies)} matches for '{search_query}' (Title similarity)**")
    else:
        total_pages = max(1, (total_movies + 19) // 20)
        st.markdown(f"**Page {st.session_state.catalog_page}/{total_pages} — Showing {len(movies)} of {total_movies} movies**")
    
    # Display movies in grid layout
    cols_per_row = 4
    for idx in range(0, len(movies), cols_per_row):
        cols = st.columns(cols_per_row)
        for col_idx, col in enumerate(cols):
            if idx + col_idx < len(movies):
                movie = movies[idx + col_idx]
                with col:
                    # Movie poster
                    year = movie.get('year')
                    poster_url = st.session_state.movie_catalog.get_poster_url(movie['title'], year)
                    st.image(poster_url, use_container_width=True)
                    
                    # Movie details
                    st.markdown(f"**{movie['title'][:30]}{'...' if len(movie['title']) > 30 else ''}**")
                    st.caption(f"{movie.get('year', 'N/A')} | {movie.get('genres', 'N/A')[:20]}")
                    
                    # Rating display with stars
                    if movie.get('rating'):
                        rating_val = movie['rating']
                        full_stars = int(rating_val)
                        half_star = 1 if (rating_val - full_stars) >= 0.5 else 0
                        empty_stars = 5 - full_stars - half_star
                        stars = '⭐' * full_stars + '✨' * half_star + '☆' * empty_stars
                        st.markdown(f"{stars} {rating_val:.1f}/10")
                    
                    # Review button
                    if st.button(f"Review", key=f"review_btn_{movie['_id']}"):
                        st.session_state.selected_movie = movie
                        st.session_state.show_review_modal = True

    # Pagination controls (only when browsing without search)
    if use_pagination:
        st.divider()
        col_prev, col_page, col_next = st.columns([1,2,1])
        total_pages = max(1, (total_movies + 19) // 20)

        with col_prev:
            if st.button("⬅️ Previous", disabled=st.session_state.catalog_page <= 1):
                st.session_state.catalog_page = max(1, st.session_state.catalog_page - 1)
                st.rerun()
        with col_page:
            goto = st.number_input("Go to page", min_value=1, max_value=total_pages, value=st.session_state.catalog_page, step=1)
            if goto != st.session_state.catalog_page:
                st.session_state.catalog_page = int(goto)
                st.rerun()
            st.caption("Use the number box to jump directly to a page.")
        with col_next:
            if st.button("Next ➡️", disabled=st.session_state.catalog_page >= total_pages):
                st.session_state.catalog_page = min(total_pages, st.session_state.catalog_page + 1)
                st.rerun()
    
    # Review modal with @st.dialog decorator
    @st.dialog(f" Review: {st.session_state.get('selected_movie', {}).get('title', 'Movie')}")
    def show_review_dialog():
        movie = st.session_state.selected_movie
        
        col1, col2 = st.columns([2, 1])
        
        with col2:
            year = movie.get('year')
            st.image(st.session_state.movie_catalog.get_poster_url(movie['title'], year), use_container_width=True)
            st.caption(f"**Genres:** {movie.get('genres', 'N/A')}")
            st.caption(f"**Year:** {movie.get('year', 'N/A')}")
        
        with col1:
            st.subheader("Your Rating")
            
            # Star rating system
            rating_options = [
                "☆☆☆☆☆ (0/5)",
                "⭐☆☆☆☆ (1/5)",
                "⭐⭐☆☆☆ (2/5)",
                "⭐⭐⭐☆☆ (3/5)",
                "⭐⭐⭐⭐☆ (4/5)",
                "⭐⭐⭐⭐⭐ (5/5 - Perfect!)"
            ]
            selected_rating_str = st.radio(
                "Select your rating",
                rating_options,
                index=2,
                label_visibility="collapsed",
                key="star_rating_selector"
            )
            
            # Extract numeric rating
            if "0/5" in selected_rating_str:
                user_rating = 0
            elif "1/5" in selected_rating_str:
                user_rating = 1
            elif "2/5" in selected_rating_str:
                user_rating = 2
            elif "3/5" in selected_rating_str:
                user_rating = 3
            elif "4/5" in selected_rating_str:
                user_rating = 4
            else:
                user_rating = 5
            
            
            st.divider()
            
            user_review = st.text_area(
                "Your Review (any language)",
                placeholder="Share your thoughts about this movie in any language...",
                height=150,
                key="review_text_input"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("✅ Submit Review", type="primary", use_container_width=True):
                    if user_review.strip():
                        with st.spinner("Analyzing sentiment..."):
                            # Language detection & optional translation
                            detected_lang = detect_language(user_review)
                            translated_text, translated_flag, translation_model = translate_to_english(user_review, detected_lang)

                            # Get sentiment prediction (always on English text)
                            model_name = selected_model.split(" ")[0].lower()
                            sentiment_result = st.session_state.model_manager.predict_sentiment(
                                translated_text,
                                model_name
                            )

                            # Save review with multilingual metadata
                            review_data = {
                                'movie_id': movie['_id'],
                                'movie_title': movie['title'],
                                'rating': user_rating,
                                'original_text': user_review,
                                'original_language': detected_lang,
                                'translated_text': translated_text if translated_flag else None,
                                'translation_model': translation_model,
                                'was_translated': translated_flag,
                                'sentiment_score': sentiment_result['score'],
                                'sentiment_label': sentiment_result['label'],
                                'model_used': model_name,
                                'session_id': st.session_state.session_id,
                                'timestamp': datetime.now()
                            }

                            st.session_state.user_reviews.append(review_data)
                            st.session_state.db_manager.save_review(review_data)

                            lang_note = f" (translated from {detected_lang})" if translated_flag else ""
                            st.success(f"✅ Review submitted{lang_note}! Sentiment: {sentiment_result['label']} ({sentiment_result['score']:.2%})")
                            st.session_state.show_review_modal = False
                            st.rerun()
                    else:
                        st.error("⚠️ Please write a review before submitting")
            
            with col_btn2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.show_review_modal = False
                    st.rerun()
    
    # Show dialog if flag is set
    if st.session_state.get('show_review_modal', False):
        show_review_dialog()

elif page == "Live Analytics":
    col_title, col_refresh = st.columns([4, 1])
    
    with col_title:
        st.markdown('<p class="main-header">📊 Live Analytics Dashboard</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Real-time insights from audience feedback</p>', unsafe_allow_html=True)
    
    with col_refresh:
        st.write("")  # Spacing
        if st.button("🔄 Refresh Data", help="Load latest reviews from all sessions"):
            st.rerun()
    
    # Load reviews from database (shared across all sessions)
    db_reviews = []
    if st.session_state.db_manager.is_connected():
        try:
            db_reviews = st.session_state.db_manager.get_reviews(limit=1000)
            # Convert ObjectId to string for compatibility
            for review in db_reviews:
                if '_id' in review:
                    review['_id'] = str(review['_id'])
                if 'movie_id' in review and hasattr(review['movie_id'], '__str__'):
                    review['movie_id'] = str(review['movie_id'])
        except Exception as e:
            st.warning(f"Error loading reviews from database: {e}")
    
    # Combine database reviews with session reviews (avoid duplicates)
    all_reviews = db_reviews.copy()
    session_review_ids = set()
    
    # Add session reviews that aren't already in database
    for review in st.session_state.user_reviews:
        review_signature = f"{review.get('movie_id')}_{review.get('timestamp')}"
        if review_signature not in session_review_ids:
            session_review_ids.add(review_signature)
            # Only add if not already in db_reviews
            if not any(
                str(r.get('movie_id')) == str(review.get('movie_id')) and 
                r.get('timestamp') == review.get('timestamp') 
                for r in db_reviews
            ):
                all_reviews.append(review)
    
    if not all_reviews:
        st.info("No reviews collected yet. Visit the Movie Catalog to start collecting audience feedback.")
    else:
        # Optional: repair any legacy Neutral(0.50) predictions created while models were unavailable
        def _needs_recompute(row):
            try:
                return (row.get('sentiment_label') not in ['Positive', 'Negative']) or (abs(float(row.get('sentiment_score', 0.5)) - 0.5) < 1e-6)
            except Exception:
                return True

        if any(_needs_recompute(r) for r in all_reviews):
            if st.button("Recalcular sentimientos de reseñas neutrales (fix)", type="secondary"):
                fixed = 0
                for r in all_reviews:
                    if _needs_recompute(r):
                        # Prefer translated text if we have it; else original
                        raw_text = r.get('original_text') or r.get('text') or r.get('translated_text') or ''
                        if raw_text:
                            # Detect & translate
                            lang = detect_language(raw_text)
                            en_text, was_translated, t_model = translate_to_english(raw_text, lang)
                            # Predict with currently selected or default model
                            primary = 'distilbert' if 'distilbert' in st.session_state.model_manager.get_available_models() else next(iter(st.session_state.model_manager.get_available_models()), 'distilbert')
                            result = st.session_state.model_manager.predict_sentiment(en_text, primary)
                            r['sentiment_label'] = result['label']
                            r['sentiment_score'] = result['score']
                            r['original_language'] = lang
                            r['translated_text'] = en_text if was_translated else None
                            r['translation_model'] = t_model
                            r['was_translated'] = was_translated
                            fixed += 1
                st.success(f"Sentimientos recalculados para {fixed} reseñas.")
                st.rerun()

        # Prepare dataframe from all reviews (database + session)
        reviews_df = pd.DataFrame(all_reviews)
        # Ensure a canonical review_text column exists for downstream visuals
        if 'review_text' not in reviews_df.columns:
            for alt_col in ['text', 'original_text', 'translated_text']:
                if alt_col in reviews_df.columns:
                    reviews_df['review_text'] = reviews_df[alt_col]
                    break
        if 'review_text' not in reviews_df.columns:
            reviews_df['review_text'] = ''
        
        # KPI metrics in a single row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Reviews", len(reviews_df))
        
        with col2:
            avg_rating = reviews_df['rating'].mean()
            st.metric("⭐ Average Rating", f"{avg_rating:.2f}/5")
        
        with col3:
            positive_pct = (reviews_df['sentiment_label'] == 'Positive').mean() * 100
            st.metric("👍 Positive Sentiment", f"{positive_pct:.1f}%")
        
        with col4:
            avg_confidence = reviews_df['sentiment_score'].mean()
            st.metric("Model Confidence", f"{avg_confidence:.2%}")
        
        st.divider()
        
        # Calculate Top 5 Movies
        movie_sentiment = reviews_df.groupby('movie_title').agg({
            'sentiment_score': 'mean',
            'sentiment_label': lambda x: x.mode()[0] if len(x) > 0 else 'Neutral',
            'rating': 'mean',
            'movie_id': 'first'
        }).reset_index()
        
        movie_sentiment_sorted = movie_sentiment.sort_values('sentiment_score', ascending=False)
        
        # Top 2 recommended
        top_2_recommended = movie_sentiment_sorted.head(2)
        
        # Find most neutral
        movie_sentiment['distance_from_neutral'] = abs(movie_sentiment['sentiment_score'] - 0.5)
        neutral_movie = movie_sentiment.sort_values('distance_from_neutral').head(1)
        
        # Bottom 2 not recommended
        bottom_2_not_recommended = movie_sentiment_sorted.tail(2)
        
        # Combine into top_5
        top_5_movies = pd.concat([top_2_recommended, neutral_movie, bottom_2_not_recommended])
        
        # Store in session state for sidebar display
        st.session_state.top_5_movies = top_5_movies
        
        # Display Top 5 in a horizontal row
        st.subheader("🎬 Top 5 Movies by Sentiment Analysis")
        cols = st.columns(5)
        
        position = 1
        for (idx, row), col in zip(top_5_movies.iterrows(), cols):
            movie_title = row['movie_title']
            sentiment_score = row['sentiment_score']
            avg_rating = row['rating']
            
            # Determine emoji and color based on position
            if position <= 2:
                emoji = "👍"
                sentiment_color = "green"
                label = "Recommended"
            elif position == 3:
                emoji = "😐"
                sentiment_color = "orange"
                label = "Neutral"
            else:
                emoji = "👎"
                sentiment_color = "red"
                label = "Not Recommended"
            
            with col:
                st.markdown(f"**#{position} {emoji}**")
                st.markdown(f"**{movie_title[:20]}{'...' if len(movie_title) > 20 else ''}**")
                
                # Star rating
                full_stars = int(avg_rating)
                half_star = 1 if (avg_rating - full_stars) >= 0.5 else 0
                empty_stars = 5 - full_stars - half_star
                stars = '⭐' * full_stars + '✨' * half_star + '☆' * empty_stars
                st.caption(f"{stars}")
                st.caption(f"{avg_rating:.1f}/5")
                
                # Sentiment percentage with color
                sentiment_pct = sentiment_score * 100
                st.markdown(f":{sentiment_color}[{sentiment_pct:.0f}%]")
                st.caption(f"{label}")
            
            position += 1
        
        st.divider()
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Rating distribution
            st.plotly_chart(
                create_rating_distribution(reviews_df),
                use_container_width=True
            )
        
        with col2:
            # Timeline chart
            st.plotly_chart(
                create_timeline_chart(reviews_df),
                use_container_width=True
            )
            
            # Top reviewed movies
            top_movies = reviews_df.groupby('movie_title').agg({
                'rating': 'mean',
                'sentiment_score': 'mean',
                'review_text': 'count'
            }).sort_values('review_text', ascending=False).head(5)
            
            fig = px.bar(
                top_movies.reset_index(),
                x='review_text',
                y='movie_title',
                orientation='h',
                title="Most Reviewed Movies",
                labels={'review_text': 'Number of Reviews', 'movie_title': 'Movie'}
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Recent reviews table
        st.subheader("Recent Reviews")
        recent_reviews = reviews_df.sort_values('timestamp', ascending=False).head(10)
        
        display_df = recent_reviews[['movie_title', 'rating', 'sentiment_label', 'sentiment_score', 'review_text']].copy()
        display_df['sentiment_score'] = display_df['sentiment_score'].apply(lambda x: f"{x:.2%}")
        display_df.columns = ['Movie', 'Rating', 'Sentiment', 'Confidence', 'Review']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)

elif page == "Model Comparison":
    st.markdown('<p class="main-header"> MovieLover Model Comparison</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Compare multiple AI models side-by-side</p>', unsafe_allow_html=True)
    
    # Model comparison interface
    st.subheader("Test Your Review Across Models")
    
    test_review = st.text_area(
        "Enter a movie review to analyze (any language)",
        placeholder="Type or paste a movie review here...",
        height=150
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_button = st.button("Analyze with All Models", type="primary")
    
    if analyze_button and test_review.strip():
        # Check available models first
        available_models = st.session_state.model_manager.get_available_models()
        
        if len(available_models) < 4:
            st.warning(f"⚠️ Only {len(available_models)} model(s) loaded: {', '.join(available_models)}. Other models will use the available model as fallback.")
        
        with st.spinner("Running predictions across all models..."):
            # Get predictions from all models
            models = ['distilbert', 'lstm', 'logistic', 'random_forest']
            results = []
            
            # Detect & translate once for efficiency
            detected_lang = detect_language(test_review)
            translated_text, translated_flag, translation_model = translate_to_english(test_review, detected_lang)

            for model_name in models:
                result = st.session_state.model_manager.predict_sentiment(translated_text, model_name)
                
                # Mark if using fallback
                actual_model = result.get('model', model_name.upper().replace('_', ' '))
                is_fallback = model_name not in available_models
                display_name = model_name.upper().replace('_', ' ')
                if is_fallback:
                    display_name += f" (using {actual_model})"
                
                results.append({
                    'Model': display_name,
                    'Prediction': result['label'],
                    'Confidence': result['score'],
                    'Entropy': result.get('entropy', 0),
                    'Prob Positive': result.get('prob_positive', result['score']),
                    'Prob Negative': result.get('prob_negative', 1 - result['score']),
                    'Processing Time': result.get('time', 0),
                    'Original Language': detected_lang,
                    'Translated': translated_flag,
                    'Is Fallback': is_fallback
                })
            
            results_df = pd.DataFrame(results)
            
            # Display comparison
            st.divider()
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Prediction Results")
                
                for idx, row in results_df.iterrows():
                    with st.container():
                        st.markdown(f"### {row['Model']}")
                        
                        # Show fallback warning
                        if row['Is Fallback']:
                            st.caption("⚠️ Model not available - using fallback")
                        
                        col_a, col_b, col_c, col_d = st.columns(4)
                        with col_a:
                            st.metric("Prediction", row['Prediction'])
                        with col_b:
                            st.metric("Confidence", f"{row['Confidence']:.2%}")
                        with col_c:
                            st.metric("Entropy", f"{row['Entropy']:.3f}", 
                                     help="Lower = more certain (0=certain, 1=uncertain)")
                        with col_d:
                            st.metric("Time", f"{row['Processing Time']:.3f}s")
                        
                        # Show probability distribution
                        col_prob1, col_prob2 = st.columns(2)
                        with col_prob1:
                            st.caption(f"🟢 Positive: {row['Prob Positive']:.1%}")
                        with col_prob2:
                            st.caption(f"🔴 Negative: {row['Prob Negative']:.1%}")
                        
                        st.progress(row['Confidence'])
                        st.divider()
            
            with col2:
                # Comparison chart
                st.plotly_chart(
                    create_model_comparison_chart(results_df),
                    use_container_width=True
                )
                
                # Performance metrics
                st.subheader("Model Performance Summary")
                
                summary_data = {
                    'Metric': ['Average Confidence', 'Average Entropy', 'Most Certain Model', 'Fastest Model', 'Agreement Rate', 'Input Language', 'Translated'],
                    'Value': [
                        f"{results_df['Confidence'].mean():.2%}",
                        f"{results_df['Entropy'].mean():.3f}",
                        results_df.loc[results_df['Entropy'].idxmin(), 'Model'],
                        results_df.loc[results_df['Processing Time'].idxmin(), 'Model'],
                        f"{(results_df['Prediction'].value_counts().max() / len(results_df) * 100):.0f}%",
                        results[0]['Original Language'],
                        'Yes' if results[0]['Translated'] else 'No'
                    ]
                }
                st.table(pd.DataFrame(summary_data))
    
    elif analyze_button:
        st.warning("Please enter a review to analyze")
    
    # Model performance comparison from training
    st.divider()
    st.subheader("Pre-trained Model Benchmarks")
    
    benchmark_data = {
        'Model': ['DistilBERT', 'LSTM', 'Logistic Regression', 'Random Forest'],
        'Accuracy': [0.9161, 0.8738, 0.8840, 0.8512],
        'Training Time': [45, 20, 5, 8],
        'Parameters': ['66M', '2.5M', '10K', '500K']
    }
    benchmark_df = pd.DataFrame(benchmark_data)
    # Add numeric parameter counts for visualization sizing
    param_map = {
        'DistilBERT': 66_000_000,
        'LSTM': 2_500_000,
        'Logistic Regression': 10_000,
        'Random Forest': 500_000
    }
    benchmark_df['Parameter Count'] = benchmark_df['Model'].map(param_map)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            benchmark_df,
            x='Model',
            y='Accuracy',
            title="Model Accuracy Comparison",
            color='Accuracy',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        fig = px.scatter(
            benchmark_df,
            x='Training Time',
            y='Accuracy',
            size='Parameter Count',
            text='Model',
            hover_data=['Parameters'],
            title="Accuracy vs Training Time",
            labels={'Training Time': 'Training Time (min)', 'Parameter Count': 'Parameters (approx)'}
        )
        fig.update_traces(textposition='top center')
        st.plotly_chart(fig, width='stretch')

elif page == "Model Architecture":
    st.markdown('<p class="main-header"> Model Architecture & Design</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Deep Learning Pipeline - From Data to Predictions</p>', unsafe_allow_html=True)
    
    # Check if diagram files exist (robust path resolution)
    models_dir = Path(__file__).resolve().parent.parent / "api" / "models" / "diagrams"
    if not models_dir.exists():
        alt_dir = Path.cwd() / "api" / "models" / "diagrams"
        if alt_dir.exists():
            models_dir = alt_dir
        else:
            st.error(f"⚠️ Diagrams directory not found: {models_dir}")
            st.info("Run `python generate_model_diagrams.py` to create the architecture diagrams.")
            st.stop()
    else:
        # Model selection tabs
        model_tabs = st.tabs(["📊 Overview", "1️⃣ Logistic Regression", "2️⃣ Random Forest", "3️⃣ LSTM", "4️⃣ DistilBERT"])
        
        with model_tabs[0]:
            st.markdown("### 🏆 Model Comparison Summary")
            st.markdown("""
            **Training Dataset:** 50,000 IMDB Movie Reviews  
            **Hardware:** NVIDIA A100 GPU (Google Colab)  
            **Task:** Binary Sentiment Classification (Positive/Negative)
            """)
            
            comparison_img = models_dir / "model_comparison_summary.png"
            if comparison_img.exists():
                st.image(str(comparison_img), use_container_width=True)
            else:
                st.warning(f"Comparison image not found: {comparison_img}")
            
            st.markdown("---")
            
            # Key insights
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Best Model Performance")
                st.success("""
                **DistilBERT (Transformer)**
                - **Accuracy:** 91.61%
                - **Parameters:** 66M
                - **Architecture:** 6 Transformer layers with Multi-Head Attention
                - **Training:** Fine-tuned with Early Stopping
                """)
            
            with col2:
                st.markdown("#### ⚡ Fastest Model")
                st.info("""
                **Logistic Regression**
                - **Accuracy:** 88.40%
                - **Training Time:** ~2 minutes
                - **Features:** TF-IDF (10K-20K)
                - **Optimization:** GridSearchCV (3-fold CV)
                """)
        
        with model_tabs[1]:
            st.markdown("### Model 1: Logistic Regression + TF-IDF")
            st.markdown("""
            **Architecture Type:** Classical Machine Learning  
            **Feature Engineering:** TF-IDF Vectorization  
            **Optimization:** GridSearchCV with 3-Fold Cross-Validation
            """)
            
            lr_img = models_dir / "model1_logistic_regression.png"
            if lr_img.exists():
                st.image(str(lr_img), use_container_width=True)
            
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Validation Accuracy", "88.40%")
            with col2:
                st.metric("Training Time", "~2 min")
            with col3:
                st.metric("Features", "10K-20K")
            
            with st.expander("🔍 Technical Details"):
                st.markdown("""
                **Hyperparameters Tuned:**
                - `max_features`: 10,000 - 20,000
                - `ngram_range`: (1,1) - (1,2)
                - `C` (regularization): 0.1 - 10
                
                **Pipeline:**
                1. Text preprocessing (lowercase, remove special chars)
                2. TF-IDF vectorization with English stop words
                3. Logistic Regression with L2 regularization
                
                **Strengths:**
                - Fast training and inference
                - Interpretable feature weights
                - Low computational requirements
                
                **Limitations:**
                - Cannot capture complex linguistic patterns
                - Fixed vocabulary size
                - Requires manual feature engineering
                """)
        
        with model_tabs[2]:
            st.markdown("### Model 2: Random Forest + TF-IDF")
            st.markdown("""
            **Architecture Type:** Ensemble Learning  
            **Base Estimators:** Decision Trees  
            **Optimization:** GridSearchCV with 3-Fold Cross-Validation
            """)
            
            rf_img = models_dir / "model2_random_forest.png"
            if rf_img.exists():
                st.image(str(rf_img), use_container_width=True)
            
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Validation Accuracy", "85.12%")
            with col2:
                st.metric("Training Time", "~5 min")
            with col3:
                st.metric("Trees", "100-200")
            
            with st.expander("🔍 Technical Details"):
                st.markdown("""
                **Hyperparameters Tuned:**
                - `n_estimators`: 100 - 200 trees
                - `max_depth`: 20 or None
                - `min_samples_split`: 2 - 5
                
                **Pipeline:**
                1. TF-IDF vectorization (20,000 features, bigrams)
                2. Random Forest with bootstrap aggregating
                3. Majority voting for final prediction
                
                **Strengths:**
                - Robust to overfitting
                - Handles non-linear relationships
                - Feature importance analysis
                
                **Limitations:**
                - Slower inference than Logistic Regression
                - Less interpretable individual predictions
                - Higher memory footprint
                """)
        
        with model_tabs[3]:
            st.markdown("### Model 3: LSTM Neural Network")
            st.markdown("""
            **Architecture Type:** Deep Learning (Recurrent Neural Network)  
            **Sequence Modeling:** Bidirectional LSTM  
            **Optimization:** Optuna (10 trials) + 5-Fold Cross-Validation
            """)
            
            lstm_img = models_dir / "model3_lstm.png"
            if lstm_img.exists():
                st.image(str(lstm_img), use_container_width=True)
            
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("CV Mean Accuracy", "87.38%")
            with col2:
                st.metric("Best Fold", "88.12%")
            with col3:
                st.metric("Parameters", "~2.5M")
            with col4:
                st.metric("Training Time", "~15 min")
            
            with st.expander("🔍 Technical Details"):
                st.markdown("""
                **Architecture Components:**
                - **Embedding Layer:** vocab_size=30,002, embed_dim=224
                - **Bidirectional LSTM:** 2 layers, hidden_dim=192
                - **Fully Connected:** FC1(128) → FC2(64) → Output(2)
                - **Regularization:** Dropout (0.3-0.6)
                
                **Optuna Hyperparameters:**
                - Embedding dimension: 96-256
                - Hidden dimension: 128-512
                - Number of layers: 1-3
                - Dropout rate: 0.3-0.6
                - Learning rate: 5e-4 to 5e-3
                
                **Training Strategy:**
                - 5-Fold Cross-Validation
                - Early stopping (patience=6)
                - AdamW optimizer with weight decay
                - Cosine annealing learning rate scheduler
                
                **Strengths:**
                - Captures sequential dependencies
                - Bidirectional context understanding
                - Learns word embeddings from scratch
                
                **Limitations:**
                - Requires substantial training data
                - Longer training time
                - Current checkpoint needs retraining (49% accuracy)
                """)
        
        with model_tabs[4]:
            st.markdown("### Model 4: DistilBERT (Transformer)")
            st.markdown("""
            **Architecture Type:** Transformer (Pre-trained Language Model)  
            **Base Model:** DistilBERT (distilled from BERT)  
            **Training:** Fine-tuning with Early Stopping
            """)
            
            bert_img = models_dir / "model4_distilbert.png"
            if bert_img.exists():
                st.image(str(bert_img), use_container_width=True)
            
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Validation Accuracy", "91.61% 🏆", delta="BEST MODEL")
            with col2:
                st.metric("Parameters", "66M")
            with col3:
                st.metric("Transformer Layers", "6")
            with col4:
                st.metric("Training Time", "~45 min")
            
            with st.expander("🔍 Technical Details"):
                st.markdown("""
                **Architecture Components:**
                - **Tokenizer:** WordPiece (vocab=30,522, max_length=256)
                - **Transformer Blocks:** 6 layers
                  - Multi-Head Self-Attention (12 heads)
                  - Feed-Forward Networks (3072 hidden units)
                  - Layer Normalization & Residual Connections
                - **Classification Head:** Linear layer (2 classes)
                
                **Fine-Tuning Configuration:**
                - Learning rate: 2e-5
                - Batch size: 32
                - Early stopping: patience=3
                - FP16 mixed precision training
                - Max epochs: 10
                
                **Pre-training:**
                - Trained on 16GB English text corpus
                - Distilled from BERT-base (40% fewer parameters)
                - Retains 97% of BERT's language understanding
                
                **Strengths:**
                - State-of-the-art accuracy
                - Transfer learning from massive corpus
                - Attention mechanism captures context
                - Handles complex linguistic nuances
                
                **Limitations:**
                - Highest computational requirements
                - Longest inference time
                - Requires GPU for practical deployment
                - Black-box interpretability
                """)
        
        st.markdown("---")
        st.markdown("### 📚 References & Resources")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Papers:**
            - [DistilBERT: A distilled version of BERT](https://arxiv.org/abs/1910.01108)
            - [Attention Is All You Need (Transformers)](https://arxiv.org/abs/1706.03762)
            - [Long Short-Term Memory Networks](https://www.bioinf.jku.at/publications/older/2604.pdf)
            """)
        
        with col2:
            st.markdown("""
            **Tools Used:**
            - **Optimization:** Optuna, GridSearchCV
            - **Frameworks:** PyTorch, scikit-learn, Hugging Face Transformers
            - **Hardware:** NVIDIA A100 GPU (Google Colab)
            - **Dataset:** 50,000 IMDB Movie Reviews
            """)

# Footer
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.caption("Powered by Advanced Machine Learning")

with col2:
    st.caption("Connected to MongoDB Atlas")

with col3:
    st.caption(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
