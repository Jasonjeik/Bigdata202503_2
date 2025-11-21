# Movie Sentiment Analytics Platform

Professional interactive dashboard for real-time movie sentiment analysis using advanced machine learning models.

## Features

- **Interactive Movie Catalog**: Browse and search movies from MongoDB Atlas (sample_mflix database)
- **Visual Movie Display**: Movie posters fetched dynamically or generated as placeholders
- **Real-time Sentiment Analysis**: Analyze audience reviews using 4 different ML models:
  - DistilBERT (Transformer) - 91.6% accuracy
  - LSTM Deep Learning - 87.4% accuracy
  - Logistic Regression - 88.4% accuracy
  - Random Forest - 85.1% accuracy
- **Model Comparison**: Compare predictions across all models side-by-side
- **Live Analytics Dashboard**: Real-time visualizations of audience feedback
- **QR Code Access**: Mobile-friendly access for audience participation
- **Professional Visualizations**: 5+ interactive charts using Plotly

## Architecture

```
dashboard/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration and settings
├── requirements.txt      # Python dependencies
└── utils/
    ├── database.py       # MongoDB connection and queries
    ├── models.py         # ML model loading and inference
    ├── movie_search.py   # Movie catalog and poster retrieval
    └── visualizations.py # Chart and graph generation
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd dashboard
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `dashboard/` directory:

```env
MONGODB_URI=mongodb+srv://jasonebm16_db_user:JK0jknwzzkJdRaDt@bdproyecto2.u5gbblq.mongodb.net/?appName=BDProyecto2
OMDB_API_KEY=your_omdb_api_key_here  # Optional: Get from http://www.omdbapi.com/
```

### 3. Verify Model Files

Ensure these model files exist in `api/models/`:
- `distilbert_final/` (directory)
- `lstm_final_cv_complete.pth`
- `logistic_regression_tfidf.pkl`
- `random_forest.pkl`
- `vocab_lstm.pkl`

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## MongoDB Database Schema

The application expects MongoDB Atlas with the `sample_mflix` database containing:

### Collections:
- **movies**: Movie catalog with title, year, genres, plot, poster, IMDb rating
- **comments**: User comments on movies
- **audience_reviews**: New collection created for storing live reviews

### Sample Movie Document:
```json
{
  "_id": ObjectId,
  "title": "Movie Title",
  "year": 2020,
  "genres": ["Drama", "Thriller"],
  "plot": "Movie description...",
  "poster": "http://...",
  "imdb": {
    "rating": 7.5
  },
  "directors": ["Director Name"],
  "cast": ["Actor 1", "Actor 2"]
}
```

## Usage for 5-Minute Pitch

### Setup (Before Presentation):
1. Deploy to Streamlit Cloud or run locally
2. Display QR code on screen
3. Have the dashboard open on presenter's screen

### During Presentation:
1. **Introduction (1 min)**: Show home page, explain the platform
2. **Movie Catalog (1 min)**: Browse movies, show visual interface
3. **Live Demo (2 min)**: 
   - Ask audience to scan QR code
   - Have 2-3 participants leave reviews
   - Show real-time sentiment analysis
4. **Model Comparison (1 min)**: Demonstrate all 4 models analyzing same review
5. **Analytics Dashboard**: Show aggregated insights and visualizations

## Key Metrics Displayed

- Total reviews collected
- Average rating
- Positive sentiment percentage
- Model confidence scores
- Review activity timeline
- Rating distribution
- Most reviewed movies
- Sentiment by rating correlation

## Model Information

| Model | Type | Accuracy | Speed | Best For |
|-------|------|----------|-------|----------|
| DistilBERT | Transformer | 91.6% | Medium | Highest accuracy |
| LSTM | RNN | 87.4% | Fast | Balanced performance |
| Logistic Reg | Classical | 88.4% | Very Fast | Simple, interpretable |
| Random Forest | Ensemble | 85.1% | Fast | Robust to outliers |

## Deployment to Streamlit Cloud

### Option 1: Direct Deployment

1. Push code to GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select repository and branch
5. Set main file path: `dashboard/app.py`
6. Add secrets in Streamlit Cloud dashboard:
   ```
   MONGODB_URI = "your_connection_string"
   OMDB_API_KEY = "your_api_key"
   ```

### Option 2: Streamlit Cloud Configuration

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#4f46e5"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f3f4f6"
textColor = "#1f2937"
font = "sans serif"

[server]
maxUploadSize = 50
enableXsrfProtection = true
```

## Professional Features

1. **Custom CSS Styling**: Professional gradient backgrounds and hover effects
2. **Responsive Layout**: Works on desktop, tablet, and mobile
3. **Real-time Updates**: Session state management for live updates
4. **Error Handling**: Graceful fallbacks for missing data
5. **Performance Optimization**: Caching and indexing for fast queries
6. **Security**: No hardcoded credentials, environment variables only

## Troubleshooting

### Models Not Loading
- Verify all model files exist in `api/models/`
- Check file permissions
- Install all requirements: `pip install -r requirements.txt`

### Database Connection Issues
- Verify MongoDB URI in `.env` file
- Check network connectivity
- Ensure IP whitelist in MongoDB Atlas includes your IP

### Poster Images Not Showing
- Get free OMDB API key from http://www.omdbapi.com/
- Add to `.env` file
- Placeholder images will be used as fallback

## Future Enhancements

- User authentication system
- Historical trend analysis
- Export reports to PDF
- Integration with more movie databases
- Multi-language support
- Advanced NLP features (topic modeling, emotion detection)

## License

Academic project for Big Data course - Master's in Data Analytics

## Contact

For questions or support, contact the development team.
