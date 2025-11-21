# Quick Start Guide
# Movie Sentiment Analytics Platform

## Prerequisites
- Python 3.9 or higher
- MongoDB Atlas account (already configured)
- Pre-trained models in `api/models/`

## Installation (5 minutes)

### Step 1: Navigate to Dashboard Directory
```bash
cd "dashboard"
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- Streamlit (web framework)
- PyMongo (database)
- PyTorch (deep learning)
- Transformers (NLP models)
- Plotly (visualizations)
- And all other dependencies

### Step 4: Configure Environment
```bash
# Copy example environment file
copy .env.example .env

# Edit .env file with your credentials (already pre-filled)
```

### Step 5: Test System
```bash
python test_system.py
```

This will verify:
- All packages are installed
- Model files exist
- Database connection works
- Application structure is correct

### Step 6: Run Application
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## First Time Setup

### 1. Verify Database Connection
- Check the sidebar shows "Database Connected"
- Should see total movie count

### 2. Test Movie Catalog
- Click "Movie Catalog" in sidebar
- Search for a movie (e.g., "Inception")
- Click on any movie poster

### 3. Submit Test Review
- Select a movie
- Write a test review: "This movie was incredible! Best film I've seen this year."
- Submit and watch sentiment analysis in action

### 4. View Analytics
- Navigate to "Live Analytics"
- See your test review in the dashboard
- Check the visualizations

### 5. Test Model Comparison
- Go to "Model Comparison"
- Enter a review text
- Click "Analyze with All Models"
- See all 4 models predictions

## Troubleshooting

### Problem: Import errors
**Solution**: 
```bash
pip install -r requirements.txt --upgrade
```

### Problem: Models not loading
**Solution**: Verify model files exist:
```bash
dir ..\api\models
```

Should see:
- distilbert_final/
- lstm_final_cv_complete.pth
- logistic_regression_tfidf.pkl
- random_forest.pkl
- vocab_lstm.pkl

### Problem: Database connection fails
**Solution**: Check internet connection and MongoDB URI in `.env`

### Problem: Slow loading
**Solution**: First load takes time to load models. Subsequent loads are cached.

## Common Commands

### Run in production mode
```bash
streamlit run app.py --server.port 80 --server.address 0.0.0.0
```

### Run with specific port
```bash
streamlit run app.py --server.port 8080
```

### Clear cache
```bash
streamlit cache clear
```

### View logs
Logs appear in terminal where you ran `streamlit run app.py`

## File Structure Overview

```
dashboard/
├── app.py                    # Main application (START HERE)
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── test_system.py          # System verification script
│
├── .streamlit/
│   └── config.toml         # Streamlit configuration
│
├── utils/
│   ├── __init__.py
│   ├── database.py         # MongoDB operations
│   ├── models.py           # ML model management
│   ├── movie_search.py     # Movie catalog functions
│   └── visualizations.py   # Chart generation
│
└── docs/
    ├── README.md           # Full documentation
    ├── DEPLOYMENT.md       # Deployment guide
    └── PRESENTATION_SCRIPT.md  # 5-min pitch script
```

## Development Workflow

### 1. Make Changes
Edit files in `dashboard/` or `dashboard/utils/`

### 2. Test Locally
```bash
streamlit run app.py
```

### 3. Check for Errors
Watch terminal output for any errors

### 4. Test System
```bash
python test_system.py
```

### 5. Commit Changes
```bash
git add .
git commit -m "Description of changes"
git push
```

## Performance Tips

1. **First Load**: Takes 30-60 seconds to load all models
2. **Subsequent Loads**: Much faster due to caching
3. **Model Selection**: Only loads the model you select
4. **Database Queries**: Cached for 10 minutes

## For Presentation

### 1 Hour Before:
```bash
# Test everything
python test_system.py

# Start application
streamlit run app.py

# Open in browser
# Test all features manually
```

### During Presentation:
- Keep terminal visible for monitoring
- Have backup browser tab ready
- Monitor sidebar connection status

### After Presentation:
```bash
# Export collected reviews
# From MongoDB Compass or Atlas UI
```

## Next Steps

1. **Customize**: Edit `config.py` to customize colors, settings
2. **Add Features**: Extend `app.py` with new functionality
3. **Deploy**: Follow `DEPLOYMENT.md` for production deployment
4. **Practice**: Use `PRESENTATION_SCRIPT.md` for your pitch

## Support Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **MongoDB Atlas**: https://www.mongodb.com/docs/atlas/
- **PyTorch**: https://pytorch.org/docs/
- **Transformers**: https://huggingface.co/docs/transformers/

## Success Checklist

Before presenting, verify:
- [ ] Application runs without errors
- [ ] Database shows correct movie count
- [ ] Can search and view movies
- [ ] Can submit a review
- [ ] Sentiment analysis works
- [ ] All 4 models respond
- [ ] Analytics dashboard updates
- [ ] QR code displays correctly

## Emergency Contacts

If you encounter issues:
1. Check terminal for error messages
2. Run `python test_system.py`
3. Check MongoDB Atlas dashboard
4. Restart application

Good luck! 🎬
