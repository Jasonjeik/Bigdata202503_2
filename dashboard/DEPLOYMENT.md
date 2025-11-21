# Deployment Guide - Movie Sentiment Analytics Platform

## Overview
This guide covers deploying your Streamlit application to production for your 5-minute presentation.

## Pre-Deployment Checklist

### 1. Verify All Files Are Present
```
dashboard/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml
└── utils/
    ├── __init__.py
    ├── database.py
    ├── models.py
    ├── movie_search.py
    └── visualizations.py
```

### 2. Verify Model Files
Ensure these files exist in `../api/models/`:
- `distilbert_final/` (full directory)
- `lstm_final_cv_complete.pth`
- `logistic_regression_tfidf.pkl`
- `random_forest.pkl`
- `vocab_lstm.pkl`

### 3. Test Locally First
```bash
cd dashboard
pip install -r requirements.txt
streamlit run app.py
```

## Deployment Options

### Option 1: Streamlit Cloud (Recommended for Demo)

#### Step 1: Prepare Repository
```bash
# Create a new GitHub repository
git init
git add .
git commit -m "Initial commit - Movie Sentiment Analytics Platform"
git remote add origin https://github.com/yourusername/movie-sentiment-app.git
git push -u origin main
```

#### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set branch: `main`
6. Set main file path: `dashboard/app.py`
7. Click "Deploy"

#### Step 3: Configure Secrets
In Streamlit Cloud dashboard, add secrets:
```toml
# .streamlit/secrets.toml format
MONGODB_URI = "mongodb+srv://jasonebm16_db_user:JK0jknwzzkJdRaDt@bdproyecto2.u5gbblq.mongodb.net/?appName=BDProyecto2"
OMDB_API_KEY = "your_api_key_here"
APP_URL = "https://your-app-name.streamlit.app"
```

#### Step 4: Update QR Code
Once deployed, update `APP_URL` in secrets with your actual Streamlit URL.

### Option 2: Local Network Deployment (For In-Person Presentation)

#### Step 1: Find Your Local IP
```bash
# Windows
ipconfig

# macOS/Linux
ifconfig
```

#### Step 2: Run Streamlit with External Access
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

#### Step 3: Generate QR Code
Your local URL will be: `http://YOUR_LOCAL_IP:8501`

Update the QR code in the app to point to this URL.

### Option 3: Azure App Service

#### Step 1: Create Requirements for Azure
Create `requirements-azure.txt`:
```
streamlit>=1.28.0
pymongo>=4.5.0
torch>=2.1.0
transformers>=4.35.0
# ... all other requirements
gunicorn>=21.0.0
```

#### Step 2: Create startup script
```bash
# startup.sh
python -m streamlit run dashboard/app.py --server.port 8000 --server.address 0.0.0.0
```

#### Step 3: Deploy via Azure CLI
```bash
az webapp up --runtime PYTHON:3.11 --sku B1 --name movie-sentiment-app
```

## Model File Handling

### For Streamlit Cloud:
Model files may be too large for GitHub. Options:

1. **Use Git LFS** (Large File Storage):
```bash
git lfs install
git lfs track "*.pth"
git lfs track "*.pkl"
git add .gitattributes
git commit -m "Track model files with Git LFS"
```

2. **Upload to Cloud Storage**:
```python
# In config.py, download models on startup
import requests
import os

def download_model(url, output_path):
    if not os.path.exists(output_path):
        response = requests.get(url)
        with open(output_path, 'wb') as f:
            f.write(response.content)
```

3. **Use Streamlit Caching**:
```python
@st.cache_resource
def load_models():
    return ModelManager()
```

## Performance Optimization

### 1. Enable Caching
Add to your app.py:
```python
@st.cache_resource
def get_database_manager():
    return DatabaseManager()

@st.cache_resource
def get_model_manager():
    return ModelManager()

@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_movies(_db_manager, query):
    return _db_manager.search_movies(query)
```

### 2. Optimize MongoDB Queries
Ensure indexes exist:
```python
db.movies.create_index([("title", "text")])
db.movies.create_index([("imdb.rating", -1)])
```

### 3. Lazy Load Models
Only load the model that's currently selected.

## Presentation Setup

### 1 Day Before:
- [ ] Deploy application
- [ ] Test from multiple devices
- [ ] Generate QR code with final URL
- [ ] Print QR code (backup)
- [ ] Test database connection
- [ ] Verify all models load correctly
- [ ] Prepare 2-3 sample reviews for demo

### 1 Hour Before:
- [ ] Open app on presentation laptop
- [ ] Display QR code on screen/slide
- [ ] Test internet connection
- [ ] Clear any test data from database
- [ ] Have backup plan (local deployment)

### During Presentation:
1. **Slide 1**: QR code full screen
2. **Slide 2**: Live dashboard showing home page
3. **Slide 3**: Movie catalog (while audience scans)
4. **Slide 4**: Live analytics as reviews come in
5. **Slide 5**: Model comparison demo

## Troubleshooting

### Issue: Models too large for Streamlit Cloud
**Solution**: Use CPU-only PyTorch version
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Issue: Slow loading time
**Solution**: Implement lazy loading and caching
```python
@st.cache_resource
def load_model_lazy(model_name):
    # Only load when requested
    pass
```

### Issue: Database connection timeout
**Solution**: Add connection pooling and retry logic
```python
from pymongo import MongoClient
client = MongoClient(uri, maxPoolSize=50, retryWrites=True)
```

### Issue: QR code not working
**Solution**: Use a URL shortener
```python
# Use bit.ly or tinyurl to create shorter URL
short_url = "bit.ly/movie-sentiment"
```

## Monitoring

### During Presentation:
- Monitor Streamlit Cloud metrics dashboard
- Watch for errors in real-time
- Have local backup running

### After Presentation:
- Download session logs
- Export collected reviews
- Generate final analytics report

## Backup Plan

If cloud deployment fails:

1. **Local Hotspot**:
   - Run app on laptop
   - Create WiFi hotspot
   - Share hotspot details with audience

2. **Pre-recorded Demo**:
   - Record screen capture of working app
   - Have ready to play if needed

3. **Static Presentation**:
   - Export key visualizations as images
   - Create traditional PowerPoint backup

## Post-Deployment

### Update README with Live URL
```markdown
## Live Demo
Access the application at: https://your-app.streamlit.app
```

### Share Access
- Share URL via email/Slack
- Include instructions for first-time users
- Provide feedback mechanism

## Cost Considerations

| Platform | Free Tier | Cost After |
|----------|-----------|------------|
| Streamlit Cloud | Yes (1 app) | $0 for public apps |
| Azure App Service | Yes (limited) | ~$13/month (B1) |
| AWS EC2 | Yes (12 months) | ~$10/month (t2.micro) |

**Recommendation**: Use Streamlit Cloud free tier for your presentation.

## Security Notes

- Never commit `.env` file to Git
- Use Streamlit secrets for sensitive data
- Whitelist MongoDB Atlas IP addresses
- Enable HTTPS (automatic on Streamlit Cloud)
- Sanitize user input in reviews

## Final Checklist

Before going live:
- [ ] All models load successfully
- [ ] Database connection works
- [ ] QR code points to correct URL
- [ ] App loads in under 5 seconds
- [ ] Mobile view works correctly
- [ ] All visualizations render properly
- [ ] Error handling works
- [ ] Backup plan ready

## Success Criteria

Your deployment is successful when:
1. App loads without errors
2. QR code successfully opens app on mobile
3. Reviews can be submitted
4. Sentiment analysis works in real-time
5. All 4 models respond to predictions
6. Visualizations update dynamically

## Support

For deployment issues:
- Streamlit Community Forum: https://discuss.streamlit.io/
- MongoDB Atlas Support: https://www.mongodb.com/cloud/atlas/support
- GitHub Issues: Create issue in your repository

Good luck with your presentation!
