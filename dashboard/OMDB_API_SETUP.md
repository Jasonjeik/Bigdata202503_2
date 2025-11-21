# OMDB API Setup - Movie Posters

## Why Do We Need OMDB API?

The OMDB (Open Movie Database) API provides high-quality movie posters and metadata. Without it, the app will use placeholder images.

## How to Get Your Free API Key

### Step 1: Visit OMDB Website
Go to: http://www.omdbapi.com/apikey.aspx

### Step 2: Choose FREE Plan
- Select "FREE! (1,000 daily limit)"
- Enter your email address
- Click "Submit"

### Step 3: Verify Email
- Check your email inbox
- Click the activation link sent by OMDB
- Your API key will be displayed

### Step 4: Configure in Your App

#### Option A: Environment Variable (Recommended)
Create a `.env` file in the `dashboard` folder:

```bash
OMDB_API_KEY=your_api_key_here
```

#### Option B: Direct Configuration
Edit `config.py` and replace the line:

```python
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "")
```

With:

```python
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "your_api_key_here")
```

### Step 5: Restart the App
After adding the API key, restart Streamlit:

```bash
streamlit run app.py
```

## Testing
Movie posters should now load from OMDB instead of showing placeholders.

## Troubleshooting

### Posters Still Not Loading?
1. **Check your API key is correct** (no extra spaces)
2. **Verify daily limit** (1,000 requests per day on free plan)
3. **Check internet connection**
4. **Look at console logs** for error messages

### Rate Limiting
If you see "Request limit exceeded":
- You've used 1,000 requests today
- Posters will load again tomorrow
- Or upgrade to a paid plan for more requests

## Alternative: No API Key
The app works without OMDB API - it just uses placeholder images with movie titles. This is fine for development and testing.

## Benefits of Using OMDB
✅ High-quality official movie posters
✅ Better user experience
✅ Professional appearance
✅ 1,000 free requests per day
✅ Cached results (same movie doesn't count multiple times)

## Security Note
⚠️ Never commit your API key to git repositories
✅ Always use environment variables
✅ Add `.env` to your `.gitignore` file
