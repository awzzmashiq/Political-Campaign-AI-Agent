# 🚀 START HERE - TVKCampaignAI Quick Setup

Welcome to TVKCampaignAI! This guide will get you running in 5 minutes.

## 📋 Current Status

**✅ You Have:** Consumer Key and Consumer Secret  
**❌ You Need:** Access Token and Access Token Secret

## ⚡ Quick Start (3 Steps)

### Step 1: Get Your Access Tokens

1. Go to [X Developer Portal](https://developer.twitter.com)
2. Log in to your account
3. Click on your app/project
4. Go to **"Keys and tokens"** tab
5. Under **"Access Token and Secret"**, click **"Generate"**
6. Copy both the Access Token and Access Token Secret

### Step 2: Configure Credentials

Edit `example.py` lines 31-34:

```python
CONSUMER_KEY = "TqceYUtn10fky0fFknZA59XS7"  # ✅ Already set
CONSUMER_SECRET = "DFgn0Je4C8db3cDozfXw1Rr71XlM0Rh5W4EAnArfrAqdnUe7xc"  # ✅ Already set
ACCESS_TOKEN = "PASTE_YOUR_ACCESS_TOKEN_HERE"  # ← Add this
ACCESS_TOKEN_SECRET = "PASTE_YOUR_ACCESS_TOKEN_SECRET_HERE"  # ← Add this
```

### Step 3: Install & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the analysis
python example.py
```

## 📚 Need More Help?

- **Detailed API Setup**: See `API_CREDENTIALS_GUIDE.md`
- **Full Documentation**: See `README.md`
- **Quick Start Guide**: See `QUICKSTART.md`
- **Setup Instructions**: See `SETUP_INSTRUCTIONS.md`
- **Deployment Guide**: See `DEPLOYMENT.md`
- **Project Summary**: See `PROJECT_SUMMARY.md`

## 🎯 What This Agent Does

TVKCampaignAI analyzes X (Twitter) data for political campaigning:

✅ **Fetches** real-time X posts about TVK/Tamil Nadu elections  
✅ **Analyzes** sentiment (positive/negative/neutral)  
✅ **Detects** trending keywords and hashtags  
✅ **Clusters** posts into topics  
✅ **Maps** influencer networks  
✅ **Generates** visualizations and reports  
✅ **Provides** strategic campaign insights  

## 🔒 Security Note

Your credentials are already configured in `example.py`.  
**For security**, consider using the `.env` file method (see API_CREDENTIALS_GUIDE.md)

## ✨ Next Steps

Once you have all 4 credentials and run `python example.py`:

1. Enter your search query (e.g., "TVK Tamil Nadu elections 2026")
2. Choose how many posts to analyze (default: 100)
3. Wait for the analysis to complete
4. View results in the `tvk_campaign_output/` folder

## 📊 Output Files

Results are saved in `tvk_campaign_output/`:
- `campaign_report.html` - Full HTML report
- `campaign_report.pdf` - PDF summary
- `sentiment_bar.png` - Sentiment chart
- `trends_wordcloud.png` - Keywords visualization
- `clusters_scatter.png` - Topic clusters
- `influencer_graph.png` - Network graph
- `agent_flow.png` - Workflow diagram

## ⚠️ Legal & Ethical

**Important**: This tool must be used responsibly:
- ✅ Comply with X's Terms of Service
- ✅ Follow Indian election laws
- ✅ Respect user privacy
- ✅ Use for legitimate campaigning only

## 🆘 Troubleshooting

**Problem**: "ModuleNotFoundError: No module named 'tweepy'"  
**Solution**: Run `pip install -r requirements.txt`

**Problem**: "Authentication failed"  
**Solution**: Verify all 4 credentials are correct in `example.py`

**Problem**: "No data fetched"  
**Solution**: Try a broader search query or remove date filters

**Problem**: "Rate limit exceeded"  
**Solution**: Wait 15 minutes or reduce the number of posts

## 📞 Support

For issues or questions:
- Check the documentation files listed above
- Review X API docs: https://developer.twitter.com/en/docs
- Open an issue on GitHub (if applicable)

---

**Ready?** Get your Access Tokens and run `python example.py`! 🚀

