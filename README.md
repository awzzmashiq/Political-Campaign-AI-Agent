# TVKCampaignAI 🎯

**Open-Source AI Agent for Analyzing X (Twitter) Data Related to TVK's Political Campaigning**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

TVKCampaignAI is an open-source, modular AI agent designed to analyze social media data from X (Twitter) to support political campaigning efforts for the 2026 Tamil Nadu elections. Built with free, open-source libraries and focusing on ethical usage, extensibility, and comprehensive analysis.

## 🌐 Web Interface

**Beautiful Streamlit-based web UI for easy interaction!**

The web interface includes:
- ✅ Pre-configured credentials for quick setup
- ✅ Interactive analysis tools with real-time progress tracking
- ✅ Beautiful data visualizations (charts, wordclouds, networks)
- ✅ Export options (CSV, HTML, PDF reports)
- ✅ Free tier compatible mode with v2 API support

Launch with: `streamlit run app.py`

## ✨ Features

- **📊 Data Collection**: Fetch real-time X posts with keyword/semantic search, date/location filters, and engagement metrics
- **😊 Sentiment Analysis**: Classify posts as positive/negative/neutral using VADER sentiment analyzer
- **📈 Trend Detection**: Extract top keywords and hashtags using TF-IDF vectorization
- **👥 Influencer Mapping**: Build network graphs with NetworkX based on mentions and replies
- **🎯 Topic Clustering**: Group posts into distinct topics using K-Means clustering
- **📊 Visualizations**: Generate comprehensive charts including:
  - Sentiment distribution bar charts
  - Trending topics wordclouds
  - Topic cluster scatter plots (with PCA)
  - Influencer network graphs
  - Workflow flowcharts
- **📄 Reporting**: Export detailed HTML and PDF reports with insights and strategic recommendations
- **⚡ Parallel Processing**: Efficient concurrent analysis for faster results
- **🔧 Extensible**: Easy to add ML models (e.g., PyTorch), new analyzers, and custom features
- **🛡️ Error Handling**: Robust management of API rate limits, empty results, and exceptions

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- X (Twitter) Developer Account and API credentials (**Basic tier or higher required**)
- Internet connection

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd political-campaign
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up X API credentials**
   
   Sign up for a X Developer account at [developer.twitter.com](https://developer.twitter.com):
   - **⚠️ IMPORTANT**: FREE tier is write-only (cannot analyze tweets)
   - You need **Basic tier ($100/month) or higher** for read access
   - Create a new app
   - Generate Consumer Key, Consumer Secret, Access Token, Access Token Secret, and Bearer Token
   - Keep these credentials secure and never commit them to version control

### Usage

#### Web UI (Recommended)

**Launch the beautiful web interface:**

```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

**Features:**
- ✅ Pre-configured credentials
- ✅ Interactive analysis
- ✅ Real-time progress tracking
- ✅ Beautiful visualizations
- ✅ Easy export options
- ✅ Free tier compatible mode

#### Terminal Usage

**For command-line usage:**

```python
from tvk_campaign_ai import TVKCampaignAI

# Initialize the agent with your X API credentials
agent = TVKCampaignAI(
    consumer_key="your_consumer_key",
    consumer_secret="your_consumer_secret",
    access_token="your_access_token",
    access_token_secret="your_access_token_secret"
)

# Run analysis
results = agent.run(
    query="TVK Tamil Nadu elections 2026",
    count=100,
    generate_reports=True
)
```

#### Advanced Usage

```python
# Custom analysis with specific parameters
agent = TVKCampaignAI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Fetch data with custom filters
df = agent.fetch_data(
    query="TVK Tamil Nadu 2026",
    count=500,
    since_date="2025-01-01"
)

# Run individual analyses
sentiment = agent.analyze_sentiment()
trends = agent.detect_trends(top_n=30)
clusters = agent.cluster_topics(num_clusters=5)
influencers = agent.map_influencers()

# Generate specific visualizations
agent.visualize_sentiment()
agent.visualize_trends()
agent.visualize_clusters()
agent.visualize_influencer_network()
agent.visualize_workflow()

# Generate insights
insights = agent.generate_strategy_insights()

# Generate reports
html_report = agent.generate_html_report()
pdf_report = agent.generate_pdf_report()
```

## 📊 Output

All outputs are saved to the `tvk_campaign_output/` directory:

### Visualizations
- `sentiment_bar.png` - Sentiment distribution chart
- `trends_wordcloud.png` - Trending topics visualization
- `clusters_scatter.png` - Topic clusters (PCA-reduced)
- `influencer_graph.png` - Influencer network graph
- `agent_flow.png` - Workflow flowchart

### Reports
- `campaign_report.html` - Comprehensive HTML report with all analyses
- `campaign_report.pdf` - PDF summary report

### Console Output
The agent provides real-time progress updates and strategic recommendations based on the analysis results.

## 🏗️ Architecture

```
TVKCampaignAI
├── Data Collection Layer
│   ├── X API Integration (Tweepy)
│   ├── Text Preprocessing
│   └── Data Validation
│
├── Analysis Layer (Parallel Processing)
│   ├── Sentiment Analysis (VADER)
│   ├── Trend Detection (TF-IDF)
│   ├── Topic Clustering (K-Means)
│   └── Influencer Mapping (NetworkX)
│
├── Visualization Layer
│   ├── Statistical Charts (Matplotlib/Seaborn)
│   ├── Network Graphs (NetworkX)
│   ├── Wordclouds (WordCloud)
│   └── Flowcharts (Graphviz)
│
└── Reporting Layer
    ├── HTML Reports
    ├── PDF Reports
    └── Strategy Insights
```

## 🔧 Extensibility

### Adding Custom Analyzers

```python
class CustomAnalyzer:
    def analyze(self, dataframe):
        # Your custom analysis logic
        return results

# Integrate with TVKCampaignAI
agent.custom_analyzer = CustomAnalyzer()
results = agent.custom_analyzer.analyze(agent.df)
```

### Adding ML Models (PyTorch Example)

```python
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class AdvancedSentimentModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("model_name")
        self.model = AutoModelForSequenceClassification.from_pretrained("model_name")
    
    def analyze_sentiment(self, text):
        # Implement sentiment analysis with transformer
        return sentiment
```

## ⚖️ Ethical Guidelines & Legal Compliance

### X (Twitter) Terms of Service
- ✅ Comply with X's API Terms of Service and Usage Policies
- ✅ Respect rate limits and throttling
- ✅ Do not store or share user data inappropriately
- ✅ Use data only for stated research/campaigning purposes

### Indian Election Laws
- ✅ Follow Election Commission of India guidelines
- ✅ Avoid spreading misinformation or fake news
- ✅ Maintain transparency in political communications
- ✅ Respect voter privacy and data protection laws

### General Ethics
- ✅ Use AI responsibly and for legitimate political discourse
- ✅ Provide transparent, verifiable insights
- ✅ Do not manipulate or deceive voters
- ✅ Respect intellectual property and attribution

**⚠️ Disclaimer**: This tool is for research and legitimate political campaigning purposes only. Users are solely responsible for ensuring their usage complies with all applicable laws, regulations, and platform terms of service.

## 🧪 Testing

```bash
# Run with sample query (requires valid API credentials)
python tvk_campaign_ai/tvk_agent.py

# Or use pytest (if tests are available)
pytest tests/
```

## ⚠️ API Access Requirements

**Important**: This agent requires read access to X API, which is **not available on the FREE tier**.

### X API Pricing Tiers

- **FREE Tier** ($0/month): ❌ **Write-only** (cannot analyze tweets)
- **Basic Tier** ($100/month): ✅ **Read & Write** (10K tweets/month) ⭐ **Recommended**
- **Pro Tier** ($5,000/month): ✅ Full access (1M tweets/month)
- **Enterprise** (Custom): ✅ Unlimited access

**For political campaign analysis, you need Basic tier or higher.**

See [FREE_TIER_LIMITATION.md](FREE_TIER_LIMITATION.md) and [TWITTER_API_COSTS.md](TWITTER_API_COSTS.md) for details.

## 📝 Dependencies

Core dependencies (see `requirements.txt` for versions):
- **tweepy**: X API integration (v1.1 + v2)
- **vaderSentiment**: Sentiment analysis
- **scikit-learn**: ML algorithms (TF-IDF, K-Means, PCA)
- **pandas**: Data manipulation
- **matplotlib/seaborn**: Statistical visualizations
- **wordcloud**: Word cloud generation
- **networkx**: Network analysis and graph visualization
- **graphviz**: Flowchart generation
- **reportlab** (optional): PDF generation
- **streamlit**: Web interface

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
black tvk_campaign_ai/
flake8 tvk_campaign_ai/

# Run tests
pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with free and open-source tools
- Designed for ethical political campaigning and research
- Inspired by democratic participation and transparent communication

## 📞 Contact & Support

For questions, issues, or contributions:
- Open an issue on GitHub
- Submit a pull request
- Contact the development team

## 🗺️ Roadmap

Future enhancements may include:
- [ ] Multi-language support (Tamil, Hindi, etc.)
- [ ] Real-time streaming analysis
- [ ] Advanced ML models integration (transformers, BERT, etc.)
- [ ] Database integration for historical analysis
- [ ] Automated report scheduling
- [ ] Web dashboard interface
- [ ] Integration with other social platforms
- [ ] Advanced topic modeling (LDA, NMF)
- [ ] Competitive analysis features

---

**Made with ❤️ for transparent political campaigning and democratic participation**

**⚠️ Please use responsibly and in compliance with all applicable laws and regulations.**

