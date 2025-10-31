# TVKCampaignAI - Quick Start Guide

Get up and running with TVKCampaignAI in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] X (Twitter) Developer account created
- [ ] API credentials obtained

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `tweepy` - X API integration
- `vaderSentiment` - Sentiment analysis
- `scikit-learn` - ML algorithms
- `matplotlib`, `seaborn` - Visualizations
- `networkx` - Network analysis
- `wordcloud` - Word clouds
- `graphviz` - Flow charts
- `pandas` - Data manipulation

**Optional** (for enhanced features):
```bash
pip install reportlab  # PDF reports
pip install torch transformers  # Advanced ML
```

## Step 2: Get X API Credentials

1. Visit [developer.twitter.com](https://developer.twitter.com)
2. Sign up for a developer account
3. Create a new app
4. Generate and save these credentials:
   - Consumer Key (API Key)
   - Consumer Secret (API Secret Key)
   - Access Token
   - Access Token Secret

⚠️ **Important**: Keep these credentials secret!

## Step 3: Run Your First Analysis

### Option A: Using the Example Script

```bash
python example.py
```

The script will prompt you for:
- Search query (e.g., "TVK Tamil Nadu elections 2026")
- Number of posts to analyze

### Option B: Direct Usage

```python
from tvk_campaign_ai import TVKCampaignAI

# Initialize agent
agent = TVKCampaignAI(
    consumer_key="YOUR_KEY",
    consumer_secret="YOUR_SECRET",
    access_token="YOUR_TOKEN",
    access_token_secret="YOUR_TOKEN_SECRET"
)

# Run analysis
results = agent.run(
    query="TVK Tamil Nadu elections 2026",
    count=100
)
```

### Option C: Using Environment Variables

1. Create a `.env` file:
```
TWITTER_CONSUMER_KEY=your_key
TWITTER_CONSUMER_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_TOKEN_SECRET=your_token_secret
```

2. Run:
```python
from dotenv import load_dotenv
import os

load_dotenv()

agent = TVKCampaignAI(
    consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
    consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
)
```

## Step 4: Explore the Results

After running, check the `tvk_campaign_output/` folder:

### Visualizations
- `sentiment_bar.png` - Sentiment distribution
- `trends_wordcloud.png` - Top keywords
- `clusters_scatter.png` - Topic clusters
- `influencer_graph.png` - Network graph
- `agent_flow.png` - Workflow diagram

### Reports
- `campaign_report.html` - Full HTML report
- `campaign_report.pdf` - PDF summary

### Console Output
You'll see:
- Progress updates
- Key statistics
- Strategic recommendations

## Example Output

```
=============================================================
Starting TVK Campaign AI Analysis
=============================================================

Fetching data for query: 'TVK Tamil Nadu elections 2026'
Successfully fetched 100 posts

[OK] Sentiment analysis complete: {'positive': 45, 'neutral': 30, 'negative': 25}
[OK] Top keywords: ['tamil', 'nadu', 'elections', 'tvk', ...]
[OK] Topic clustering complete

📊 Generating visualizations...
[OK] All visualizations generated!

💡 Generating strategic insights...
  ✅ Strong positive sentiment! Continue current messaging strategy.
  📊 Top trending keywords: tamil, nadu, elections
  💡 Consider incorporating these trending terms in campaign messaging.
  📈 Average engagement per post: 23.5 interactions
  💡 High engagement rate! Content is resonating well with audience.

=============================================================
🎉 Analysis Complete!
=============================================================
```

## Customization Examples

### Change Analysis Parameters

```python
# More detailed analysis
results = agent.run(
    query="TVK Tamil Nadu",
    count=500,  # Analyze 500 posts
    since_date="2025-01-01"  # From specific date
)
```

### Custom Visualization

```python
# Generate only sentiment chart
agent.fetch_data("TVK", count=100)
agent.analyze_sentiment()
agent.visualize_sentiment()

# Generate only trends
agent.detect_trends(top_n=30)
agent.visualize_trends()

# Custom clustering
agent.cluster_topics(num_clusters=5)
agent.visualize_clusters()
```

### Export Raw Data

```python
# Get the DataFrame
df = agent.df

# Export to CSV
df.to_csv('tweets_data.csv', index=False)

# Access results
print(agent.results['sentiment'])
print(agent.results['top_keywords'])
print(agent.results['strategy_insights'])
```

## Common Use Cases

### 1. Daily Campaign Monitoring

```python
# Run daily analysis
results = agent.run(
    query="#TVK OR #Vijaykanth",
    count=200
)

# Check sentiment trends
if results['sentiment']['positive'] / sum(results['sentiment'].values()) < 0.4:
    print("⚠️ Warning: Low positive sentiment detected")
```

### 2. Competitor Analysis

```python
# Analyze competitor mentions
competitor_query = "(competitor1 OR competitor2) AND Tamil Nadu"
results = agent.run(query=competitor_query, count=300)
```

### 3. Influencer Engagement

```python
# Find and engage with top influencers
agent.run("TVK", count=200)
influencers = agent.results['top_influencers']

for inf in influencers[:10]:
    print(f"Consider engaging with @{inf['user']}")
```

### 4. Hashtag Strategy

```python
# Identify trending hashtags
agent.run("Tamil Nadu elections", count=500)
top_hashtags = agent.results['top_hashtags']

# Use top hashtags in your posts
print("Recommended hashtags:", list(top_hashtags.keys())[:10])
```

## Troubleshooting

### "Authentication failed"
- ✅ Check API credentials are correct
- ✅ Verify X Developer account is active
- ✅ Ensure credentials have read permissions

### "No data fetched"
- ✅ Try broader search query
- ✅ Check spelling in query
- ✅ Try removing date filters
- ✅ Wait and retry if rate limited

### "Rate limit exceeded"
- ✅ Agent auto-waits, but may take time
- ✅ Reduce `count` parameter
- ✅ Wait 15 minutes and retry

### Import errors
- ✅ Run `pip install -r requirements.txt`
- ✅ Check Python version (3.8+)
- ✅ Use virtual environment

### Graphviz errors
- **Windows**: Install from [graphviz.org](https://graphviz.org/download/)
- **Mac**: `brew install graphviz`
- **Linux**: `sudo apt-get install graphviz`

## Next Steps

- 📖 Read the [README.md](README.md) for detailed documentation
- 🔧 See [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) for advanced setup
- 💡 Check code examples in `tvk_campaign_ai/tvk_agent.py`
- 🤝 Contribute to the project

## Need Help?

- Open an issue on GitHub
- Check existing documentation
- Review X API docs: [developer.twitter.com/docs](https://developer.twitter.com/en/docs)

---

**Remember**: Use responsibly, comply with X Terms of Service and Indian election laws!

**MIT License** - Free to use, modify, and distribute.

