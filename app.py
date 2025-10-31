"""
TVKCampaignAI Web Interface
Beautiful, user-friendly web UI for political campaign analysis
"""

import streamlit as st
import pandas as pd
import os
from tvk_campaign_ai import TVKCampaignAI
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="TVK Campaign AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E90FF;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #333;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .success-box {
        padding: 15px;
        border-radius: 5px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 10px 0;
    }
    .info-box {
        padding: 15px;
        border-radius: 5px;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 10px 0;
    }
    .warning-box {
        padding: 15px;
        border-radius: 5px;
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        color: #856404;
        margin: 10px 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1E90FF;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        margin-top: 5px;
    }
    .stProgress > div > div > div > div {
        background-color: #1E90FF;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">🎯 TVK Campaign AI</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; font-size: 1.1rem;'>Open-Source AI Agent for Political Campaign Analysis on X</p>", unsafe_allow_html=True)

# Sidebar for credentials and settings
st.sidebar.title("⚙️ Configuration")

# API Credentials (stored in session state)
if 'agent' not in st.session_state:
    st.session_state.agent = None
    st.session_state.credentials_set = False

with st.sidebar:
    st.markdown("### 🔑 API Credentials")
    
    # Check if credentials are already configured
    use_preconfigured = st.checkbox("Use Pre-configured Credentials", value=True)
    
    if not use_preconfigured:
        consumer_key = st.text_input("Consumer Key (API Key)", type="password")
        consumer_secret = st.text_input("Consumer Secret", type="password")
        access_token = st.text_input("Access Token", type="password")
        access_token_secret = st.text_input("Access Token Secret", type="password")
        bearer_token = st.text_input("Bearer Token (Optional)", type="password", help="For v2 API free tier")
    else:
        # Use environment variables for security
        import os
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
        
        consumer_key = os.getenv("TWITTER_CONSUMER_KEY", "")
        consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET", "")
        access_token = os.getenv("TWITTER_ACCESS_TOKEN", "")
        access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")
        bearer_token = os.getenv("TWITTER_BEARER_TOKEN", "")
    
    # Initialize button
    if st.button("🔌 Initialize Agent", type="primary", use_container_width=True):
        if all([consumer_key, consumer_secret, access_token, access_token_secret]):
            try:
                with st.spinner("Connecting to X API..."):
                    agent = TVKCampaignAI(
                        consumer_key=consumer_key,
                        consumer_secret=consumer_secret,
                        access_token=access_token,
                        access_token_secret=access_token_secret,
                        bearer_token=bearer_token if use_preconfigured else None
                    )
                    st.session_state.agent = agent
                    st.session_state.credentials_set = True
                    st.success("✅ Agent initialized successfully!")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Initialization failed: {str(e)}")
                st.info("💡 Check your credentials and ensure you have proper X API access.")
        else:
            st.warning("⚠️ Please fill in all credentials")
    
    # Status indicator
    if st.session_state.credentials_set:
        st.markdown('<div class="success-box">✅ Agent Ready</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="warning-box">⚠️ Not Initialized</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # About section
    st.markdown("### ℹ️ About")
    st.markdown("""
    **TVKCampaignAI** analyzes X (Twitter) data for political campaigning.
    
    **Features:**
    - 📊 Sentiment Analysis
    - 📈 Trend Detection
    - 🎯 Topic Clustering
    - 👥 Influencer Mapping
    - 📄 Reports & Insights
    
    **License:** MIT
    """)
    
    st.markdown("---")
    
    # API Access Notice
    st.markdown("### ⚠️ API Notice")
    st.markdown("""
    Your account needs **X API v1.1 search access**.
    
    Current tier may have limitations.
    See `API_ACCESS_REQUIREMENTS.md` for details.
    """)

# Main content area
if not st.session_state.credentials_set:
    st.markdown("""
    <div class="info-box">
        <h3>👋 Welcome to TVK Campaign AI!</h3>
        <p>Please configure your X API credentials in the sidebar to get started.</p>
        <p><strong>Steps:</strong></p>
        <ol>
            <li>Ensure you have X Developer account</li>
            <li>Enter your API credentials (or use pre-configured)</li>
            <li>Click "Initialize Agent"</li>
            <li>Start analyzing!</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📖 Quick Start Guide")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **1️⃣ Get Credentials**
        - Sign up at [X Developer Portal](https://developer.twitter.com)
        - Create a new app
        - Generate API keys
        """)
    
    with col2:
        st.markdown("""
        **2️⃣ Initialize**
        - Enter credentials in sidebar
        - Click "Initialize Agent"
        - Wait for confirmation
        """)
    
    with col3:
        st.markdown("""
        **3️⃣ Analyze**
        - Enter search query
        - Set parameters
        - Run analysis
        - View results!
        """)
    
    st.markdown("---")
    st.markdown("### 📚 Documentation")
    st.markdown("""
    - **[README.md](README.md)** - Complete documentation
    - **[START_HERE.md](START_HERE.md)** - Quick setup guide
    - **[API_ACCESS_REQUIREMENTS.md](API_ACCESS_REQUIREMENTS.md)** - API tier info
    """)
else:
    st.markdown('<div class="success-box"><strong>✅ Agent Ready!</strong> Configure your analysis below.</div>', unsafe_allow_html=True)
    
    # Analysis configuration
    st.markdown('<p class="sub-header">🔍 Configure Analysis</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "Search Query",
            value="TVK Tamil Nadu elections 2026",
            placeholder="Enter your search query here...",
            help="Search for tweets matching your query (e.g., hashtags, keywords, mentions)"
        )
    
    with col2:
        count = st.number_input(
            "Number of Posts",
            min_value=10,
            max_value=1000,
            value=100,
            step=10,
            help="How many tweets to analyze (higher = more comprehensive)"
        )
    
    # Advanced options (collapsible)
    with st.expander("⚙️ Advanced Options"):
        col3, col4 = st.columns(2)
        with col3:
            date_option = st.radio(
                "Date Filter",
                ["Last 7 days", "Last 30 days", "Custom"],
                index=0
            )
        
        with col4:
            if date_option == "Custom":
                since_date = st.date_input("Start Date", datetime.now().replace(day=1))
            else:
                since_date = None
        
        generate_reports = st.checkbox("Generate Reports (HTML/PDF)", value=True)
        use_v2_api = st.checkbox("Use v2 API (Free Tier)", value=True, help="Check this if you have free tier only")
    
    # Run analysis button
    if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
        if not query:
            st.warning("⚠️ Please enter a search query")
        else:
            try:
                agent = st.session_state.agent
                
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Run analysis
                status_text.text("🔍 Fetching data from X...")
                progress_bar.progress(10)
                
                df = agent.fetch_data(query=query, count=count, since_date=None, use_v2=use_v2_api)
                progress_bar.progress(30)
                
                if df is not None and not df.empty:
                    # Run complete analysis pipeline (includes all visualizations and insights)
                    status_text.text("📊 Running full analysis pipeline...")
                    progress_bar.progress(40)
                    
                    # Run parallel analysis (includes sentiment, trends, clusters, influencers)
                    status_text.text("⚡ Running parallel analyses...")
                    agent.run_parallel_analysis()
                    progress_bar.progress(60)
                    
                    # Generate visualizations
                    status_text.text("🎨 Generating visualizations...")
                    agent.visualize_sentiment()
                    agent.visualize_trends()
                    agent.visualize_clusters()
                    agent.visualize_influencer_network()
                    agent.visualize_workflow()
                    progress_bar.progress(85)
                    
                    # Generate strategic insights
                    status_text.text("💡 Generating insights...")
                    agent.generate_strategy_insights()
                    progress_bar.progress(95)
                    
                    # Generate reports if requested
                    if generate_reports:
                        status_text.text("📄 Generating reports...")
                        agent.generate_html_report()
                        agent.generate_pdf_report()
                    
                    # Store results
                    st.session_state.results = agent.results
                    st.session_state.df = agent.df
                    
                    status_text.text("✅ Complete!")
                    progress_bar.progress(100)
                    time.sleep(0.5)
                    progress_bar.empty()
                    status_text.empty()
                    
                    st.balloons()
                    st.success(f"🎉 Successfully analyzed {len(agent.df)} posts!")
                    st.rerun()
                else:
                    st.warning("⚠️ No data found for your query. Try adjusting your search terms.")
                    
                    # API Access notice
                    st.info("""
                    **Possible reasons:**
                    - No matching tweets found
                    - API access tier limitations
                    - Try a broader search query
                    - Check `API_ACCESS_REQUIREMENTS.md` for access tier info
                    """)
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.info("💡 This might be due to API access limitations. See `API_ACCESS_REQUIREMENTS.md`")

    # Display results if available
    if 'results' in st.session_state and 'df' in st.session_state:
        results = st.session_state.results
        df = st.session_state.df
        
        st.markdown("---")
        st.markdown('<p class="sub-header">📊 Analysis Results</p>', unsafe_allow_html=True)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-label">Posts Analyzed</div>
            </div>
            """.format(len(df)), unsafe_allow_html=True)
        
        with col2:
            if 'sentiment' in results:
                pos_pct = (results['sentiment'].get('positive', 0) / sum(results['sentiment'].values()) * 100) if sum(results['sentiment'].values()) > 0 else 0
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">{:.1f}%</div>
                    <div class="metric-label">Positive Sentiment</div>
                </div>
                """.format(pos_pct), unsafe_allow_html=True)
        
        with col3:
            if 'sentiment' in results:
                total_sentiment = sum(results['sentiment'].values())
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">{}</div>
                    <div class="metric-label">Total Posts</div>
                </div>
                """.format(total_sentiment), unsafe_allow_html=True)
        
        with col4:
            avg_engagement = df['engagement'].mean() if 'engagement' in df.columns else 0
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{:.1f}</div>
                <div class="metric-label">Avg Engagement</div>
            </div>
            """.format(avg_engagement), unsafe_allow_html=True)
        
        # Tabs for different result views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Sentiment", "📈 Trends", "🎯 Topics", "👥 Influencers", "💡 Insights"
        ])
        
        with tab1:
            if 'sentiment' in results:
                st.markdown("### Sentiment Distribution")
                sentiment_df = pd.DataFrame(list(results['sentiment'].items()), columns=['Sentiment', 'Count'])
                st.bar_chart(sentiment_df.set_index('Sentiment'))
                
                col5, col6 = st.columns(2)
                with col5:
                    st.markdown("#### Details")
                    st.dataframe(sentiment_df, use_container_width=True, hide_index=True)
                
                with col6:
                    st.markdown("#### Visual")
                    if 'sentiment_bar.png' in os.listdir(agent.output_dir):
                        st.image(os.path.join(agent.output_dir, 'sentiment_bar.png'))
        
        with tab2:
            if 'top_keywords' in results or 'top_hashtags' in results:
                col7, col8 = st.columns(2)
                
                with col7:
                    st.markdown("### Top Keywords")
                    if 'top_keywords' in results:
                        keywords_df = pd.DataFrame(
                            list(results['top_keywords'].items())[:20],
                            columns=['Keyword', 'Score']
                        )
                        st.bar_chart(keywords_df.set_index('Keyword'))
                        st.dataframe(keywords_df, use_container_width=True, hide_index=True)
                
                with col8:
                    st.markdown("### Top Hashtags")
                    if 'top_hashtags' in results:
                        hashtags_df = pd.DataFrame(
                            list(results['top_hashtags'].items())[:20],
                            columns=['Hashtag', 'Count']
                        )
                        st.bar_chart(hashtags_df.set_index('Hashtag'))
                        st.dataframe(hashtags_df, use_container_width=True, hide_index=True)
                
                if 'trends_wordcloud.png' in os.listdir(agent.output_dir):
                    st.markdown("### Word Cloud")
                    st.image(os.path.join(agent.output_dir, 'trends_wordcloud.png'))
        
        with tab3:
            if 'clusters' in results:
                st.markdown("### Topic Clusters")
                clusters_info = results['clusters']
                
                if 'cluster_counts' in clusters_info:
                    clusters_df = pd.DataFrame(
                        list(clusters_info['cluster_counts'].items()),
                        columns=['Cluster', 'Posts']
                    )
                    st.bar_chart(clusters_df.set_index('Cluster'))
                    st.dataframe(clusters_df, use_container_width=True, hide_index=True)
                
                if 'cluster_terms' in clusters_info:
                    for cluster_id, terms in clusters_info['cluster_terms'].items():
                        st.markdown(f"**Cluster {cluster_id}:** {', '.join(terms) if terms else 'N/A'}")
                
                if 'clusters_scatter.png' in os.listdir(agent.output_dir):
                    st.markdown("### Cluster Visualization")
                    st.image(os.path.join(agent.output_dir, 'clusters_scatter.png'))
        
        with tab4:
            if 'top_influencers' in results and results['top_influencers']:
                st.markdown("### Top Influencers")
                influencers_df = pd.DataFrame(results['top_influencers'][:20])
                influencers_df.columns = ['Username', 'Centrality Score']
                st.dataframe(influencers_df, use_container_width=True, hide_index=True)
                
                if 'influencer_graph.png' in os.listdir(agent.output_dir):
                    st.markdown("### Network Graph")
                    st.image(os.path.join(agent.output_dir, 'influencer_graph.png'))
            else:
                st.info("No influencer data available yet.")
        
        with tab5:
            if 'strategy_insights' in results:
                st.markdown("### Strategic Recommendations")
                for insight in results['strategy_insights']:
                    st.markdown(f"- {insight}")
                
                # Generate reports button
                if generate_reports:
                    if st.button("📄 Generate Full Reports", type="secondary"):
                        with st.spinner("Generating HTML and PDF reports..."):
                            try:
                                agent.generate_html_report()
                                agent.generate_pdf_report()
                                st.success("✅ Reports generated successfully!")
                                st.info("📁 Reports saved in: `tvk_campaign_output/`")
                            except Exception as e:
                                st.warning(f"⚠️ Report generation had issues: {str(e)}")
            else:
                st.info("Run a full analysis to see strategic insights.")
        
        # Download data
        st.markdown("---")
        st.markdown("### 💾 Export Data")
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"tvk_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>TVKCampaignAI v1.0</strong> | MIT License | Built with ❤️ for transparent political campaigning</p>
    <p style='font-size: 0.9rem;'>
        ⚖️ Use responsibly | Comply with X Terms of Service | Follow Indian election laws
    </p>
</div>
""", unsafe_allow_html=True)

