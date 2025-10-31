# Setup Instructions for TVKCampaignAI

## Prerequisites

1. **Python 3.8 or higher** - Download from [python.org](https://www.python.org/downloads/)
2. **X (Twitter) Developer Account** - Sign up at [developer.twitter.com](https://developer.twitter.com)
3. **Git** (optional) - For cloning the repository

## Step-by-Step Setup

### 1. Install Python Dependencies

Open terminal/command prompt and navigate to the project directory:

```bash
# Install all required packages
pip install -r requirements.txt
```

**Optional**: For PDF report generation:
```bash
pip install reportlab
```

**Optional**: For using environment variables:
```bash
pip install python-dotenv
```

**Optional**: For advanced ML features:
```bash
pip install torch transformers
```

### 2. Get X API Credentials

1. Go to [https://developer.twitter.com](https://developer.twitter.com)
2. Sign in or create an account
3. Apply for a Developer Account (usually approved quickly for research purposes)
4. Create a new App or Project
5. Generate the following keys:
   - **Consumer Key** (also called API Key)
   - **Consumer Secret** (also called API Secret Key)
   - **Access Token**
   - **Access Token Secret**

### 3. Configure Credentials

#### Option A: Using a .env file (Recommended)

1. Create a `.env` file in the project root:
```env
TWITTER_CONSUMER_KEY=your_consumer_key_here
TWITTER_CONSUMER_SECRET=your_consumer_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
```

2. Update `example.py` to load from environment:
```python
from dotenv import load_dotenv

load_dotenv()
CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
# ... etc
```

#### Option B: Direct configuration (Not recommended for production)

Edit the credentials in `example.py` or `tvk_campaign_ai/tvk_agent.py`:
```python
CONSUMER_KEY = "your_actual_consumer_key"
CONSUMER_SECRET = "your_actual_consumer_secret"
ACCESS_TOKEN = "your_actual_access_token"
ACCESS_TOKEN_SECRET = "your_actual_access_token_secret"
```

### 4. Run the Agent

#### Basic Run
```bash
python example.py
```

#### Advanced Run (Programmatic)
```python
python -c "
from tvk_campaign_ai import TVKCampaignAI

agent = TVKCampaignAI(
    consumer_key='your_key',
    consumer_secret='your_secret',
    access_token='your_token',
    access_token_secret='your_token_secret'
)

results = agent.run('TVK Tamil Nadu elections 2026', count=100)
print('Analysis complete!')
"
```

## Troubleshooting

### Issue: "No module named 'tweepy'"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Authentication failed"
**Solution**: Check your API credentials are correct and have proper permissions

### Issue: "Rate limit exceeded"
**Solution**: The agent automatically waits, but you may need to wait longer or reduce `count` parameter

### Issue: "No data fetched"
**Solution**: 
- Try a broader search query
- Check if there are any posts matching your query
- Try without date filters

### Issue: "Error generating PDF"
**Solution**: 
```bash
pip install reportlab
```

### Issue: "Graphviz not found" (for workflow diagrams)
**Solution**: 
- **Windows**: Download from [Graphviz website](https://graphviz.org/download/)
- **Mac**: `brew install graphviz`
- **Linux**: `sudo apt-get install graphviz`

### Issue: Python version too old
**Solution**: Upgrade Python to 3.8 or higher

## Testing Without API Credentials

If you want to test the code structure without X API access, you can create mock data:

```python
import pandas as pd
from tvk_campaign_ai import TVKCampaignAI

# Create mock agent (without API initialization)
agent = TVKCampaignAI.__new__(TVKCampaignAI)
agent.preprocessor = None  # Will be created by __init__

# Create sample data
agent.df = pd.DataFrame({
    'text': ['Great campaign!', 'Not impressed', 'Neutral comment'],
    'author': ['user1', 'user2', 'user3'],
    'likes': [10, 5, 2],
    'hashtags': [['#TVK'], ['#Election'], ['#TamilNadu']]
})

# Run analysis (will skip data fetching)
agent.analyze_sentiment()
agent.visualize_sentiment()
```

## Next Steps

1. Read the [README.md](README.md) for detailed usage instructions
2. Review the [LICENSE](LICENSE) file for terms of use
3. Check out the code examples in `tvk_campaign_ai/tvk_agent.py`
4. Join the community for support and contributions

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review X API documentation at [developer.twitter.com/en/docs](https://developer.twitter.com/en/docs)

## Legal Reminders

⚠️ **Important**: 
- Comply with X Terms of Service
- Follow Indian election laws
- Use responsibly and ethically
- Never commit API credentials to version control
- Respect user privacy and data protection laws

