"""
Visualization utilities for creating professional charts and graphs
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
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

def create_sentiment_gauge(positive_percentage):
    """
    Create a gauge chart showing sentiment percentage
    
    Args:
        positive_percentage: Percentage of positive sentiment (0-100)
    
    Returns:
        Plotly figure object
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=positive_percentage,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Positive Sentiment", 'font': {'size': 24}},
        delta={'reference': 50, 'increasing': {'color': AppConfig.COLOR_SCHEME['positive']}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': AppConfig.COLOR_SCHEME['primary']},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 33], 'color': '#fee2e2'},
                {'range': [33, 66], 'color': '#fef3c7'},
                {'range': [66, 100], 'color': '#d1fae5'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="white",
        font={'color': "darkblue", 'family': "Arial"},
        height=300
    )
    
    return fig

def create_rating_distribution(reviews_df):
    """
    Create a bar chart showing rating distribution
    
    Args:
        reviews_df: DataFrame with review data
    
    Returns:
        Plotly figure object
    """
    rating_counts = reviews_df['rating'].value_counts().sort_index()
    
    fig = go.Figure(data=[
        go.Bar(
            x=rating_counts.index,
            y=rating_counts.values,
            marker_color=AppConfig.COLOR_SCHEME['primary'],
            text=rating_counts.values,
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Rating Distribution",
        xaxis_title="Rating (Stars)",
        yaxis_title="Number of Reviews",
        xaxis=dict(tickmode='linear', tick0=1, dtick=1),
        showlegend=False,
        height=300,
        paper_bgcolor='white',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    
    return fig

def create_timeline_chart(reviews_df):
    """
    Create a timeline chart showing review activity
    
    Args:
        reviews_df: DataFrame with review data
    
    Returns:
        Plotly figure object
    """
    # Group by time intervals
    reviews_df['timestamp'] = pd.to_datetime(reviews_df['timestamp'])
    reviews_df['time_bucket'] = reviews_df['timestamp'].dt.floor('5min')
    
    # Determine appropriate text column for counting reviews
    text_col_candidates = [
        'review_text', 'text', 'original_text', 'translated_text'
    ]
    available_text_col = None
    for c in text_col_candidates:
        if c in reviews_df.columns:
            available_text_col = c
            break
    if available_text_col is None:
        # Fallback: create a dummy column to count rows
        available_text_col = '_row'
        reviews_df[available_text_col] = 1
    agg_map = {available_text_col: 'count'}
    if 'sentiment_score' in reviews_df.columns:
        agg_map['sentiment_score'] = 'mean'
    if 'rating' in reviews_df.columns:
        agg_map['rating'] = 'mean'
    timeline_data = reviews_df.groupby('time_bucket').agg(agg_map).reset_index()
    
    fig = go.Figure()
    
    # Add review count line
    count_col = available_text_col
    fig.add_trace(go.Scatter(
        x=timeline_data['time_bucket'],
        y=timeline_data[count_col],
        mode='lines+markers',
        name='Review Count',
        line=dict(color=AppConfig.COLOR_SCHEME['primary'], width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Review Activity Timeline",
        xaxis_title="Time",
        yaxis_title="Number of Reviews",
        hovermode='x unified',
        height=300,
        paper_bgcolor='white',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    
    return fig

def create_model_comparison_chart(results_df):
    """
    Create a comparison chart for model predictions
    
    Args:
        results_df: DataFrame with model comparison results
    
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    # Add confidence bars
    fig.add_trace(go.Bar(
        x=results_df['Model'],
        y=results_df['Confidence'],
        name='Confidence',
        marker_color=AppConfig.COLOR_SCHEME['primary'],
        text=results_df['Confidence'].apply(lambda x: f"{x:.1%}"),
        textposition='auto',
    ))
    
    fig.update_layout(
        title="Model Confidence Comparison",
        xaxis_title="Model",
        yaxis_title="Confidence Score",
        yaxis=dict(tickformat='.0%', range=[0, 1]),
        height=400,
        paper_bgcolor='white',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    
    return fig

def create_sentiment_by_rating_chart(reviews_df):
    """
    Create a box plot showing sentiment distribution by rating
    
    Args:
        reviews_df: DataFrame with review data
    
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    for rating in sorted(reviews_df['rating'].unique()):
        data = reviews_df[reviews_df['rating'] == rating]['sentiment_score']
        
        fig.add_trace(go.Box(
            y=data,
            name=f"{rating} Stars",
            marker_color=AppConfig.COLOR_SCHEME['primary']
        ))
    
    fig.update_layout(
        title="Sentiment Score Distribution by Rating",
        xaxis_title="Rating",
        yaxis_title="Sentiment Score",
        height=400,
        paper_bgcolor='white',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    
    return fig

def create_word_frequency_chart(reviews_df, top_n=20):
    """
    Create a bar chart of most frequent words in reviews
    
    Args:
        reviews_df: DataFrame with review data
        top_n: Number of top words to show
    
    Returns:
        Plotly figure object
    """
    from collections import Counter
    import re
    
    # Extract all words
    all_text = ' '.join(reviews_df['review_text'].astype(str))
    words = re.findall(r'\b[a-z]{4,}\b', all_text.lower())
    
    # Remove common stop words
    stop_words = {'this', 'that', 'with', 'from', 'have', 'been', 'were', 'they', 
                  'what', 'your', 'about', 'would', 'there', 'their', 'which'}
    words = [w for w in words if w not in stop_words]
    
    # Count frequencies
    word_freq = Counter(words).most_common(top_n)
    
    if word_freq:
        words, counts = zip(*word_freq)
        
        fig = go.Figure(data=[
            go.Bar(
                y=list(words),
                x=list(counts),
                orientation='h',
                marker_color=AppConfig.COLOR_SCHEME['secondary'],
                text=list(counts),
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title=f"Top {top_n} Words in Reviews",
            xaxis_title="Frequency",
            yaxis_title="Word",
            height=500,
            paper_bgcolor='white',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
        
        return fig
    else:
        # Return empty figure if no data
        fig = go.Figure()
        fig.update_layout(
            title="Word Frequency Analysis",
            annotations=[{
                'text': 'No data available',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 20}
            }]
        )
        return fig

def create_heatmap_sentiment_time(reviews_df):
    """
    Create a heatmap showing sentiment over time
    
    Args:
        reviews_df: DataFrame with review data
    
    Returns:
        Plotly figure object
    """
    reviews_df['timestamp'] = pd.to_datetime(reviews_df['timestamp'])
    reviews_df['hour'] = reviews_df['timestamp'].dt.hour
    reviews_df['minute_group'] = (reviews_df['timestamp'].dt.minute // 10) * 10
    
    heatmap_data = reviews_df.groupby(['hour', 'minute_group'])['sentiment_score'].mean().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='minute_group', columns='hour', values='sentiment_score')
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        colorscale='RdYlGn',
        zmid=0.5
    ))
    
    fig.update_layout(
        title="Sentiment Heatmap by Time",
        xaxis_title="Hour",
        yaxis_title="Minute",
        height=400,
        paper_bgcolor='white'
    )
    
    return fig

def create_3d_scatter(reviews_df):
    """
    Create a 3D scatter plot of rating, sentiment, and review length
    
    Args:
        reviews_df: DataFrame with review data
    
    Returns:
        Plotly figure object
    """
    reviews_df['review_length'] = reviews_df['review_text'].str.len()
    
    fig = px.scatter_3d(
        reviews_df,
        x='rating',
        y='sentiment_score',
        z='review_length',
        color='sentiment_label',
        color_discrete_map={
            'Positive': AppConfig.COLOR_SCHEME['positive'],
            'Negative': AppConfig.COLOR_SCHEME['negative']
        },
        title="3D Review Analysis",
        labels={
            'rating': 'Rating',
            'sentiment_score': 'Sentiment Score',
            'review_length': 'Review Length'
        }
    )
    
    fig.update_layout(height=600, paper_bgcolor='white')
    
    return fig
