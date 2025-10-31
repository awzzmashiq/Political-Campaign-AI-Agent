# TVKCampaignAI: Open-Source AI Agent for TVK Political Campaigning Analysis
# MIT License - Free to use, modify, distribute

import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from graphviz import Digraph
import pandas as pd
from wordcloud import WordCloud
import os
import re
import logging
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import warnings
warnings.filterwarnings('ignore')

# Optional PyTorch integration for advanced sentiment
try:
    import torch
    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TextPreprocessor:
    """Clean and preprocess text data"""
    
    @staticmethod
    def clean_text(text):
        """Remove URLs, mentions, extra whitespace, and normalize text"""
        if not isinstance(text, str):
            return ""
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove user mentions (but keep for later analysis)
        # text = re.sub(r'@\w+', '', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s!?.,]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @staticmethod
    def extract_hashtags(text):
        """Extract hashtags from text"""
        if not isinstance(text, str):
            return []
        hashtags = re.findall(r'#\w+', text)
        return [h.lower() for h in hashtags]
    
    @staticmethod
    def extract_mentions(text):
        """Extract user mentions from text"""
        if not isinstance(text, str):
            return []
        mentions = re.findall(r'@\w+', text)
        return [m.lower() for m in mentions]


class TVKCampaignAI:
    """Main AI agent for TVK political campaign analysis"""
    
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, bearer_token=None):
        """Initialize the agent with API credentials
        
        Args:
            consumer_key: X API Consumer Key
            consumer_secret: X API Consumer Secret
            access_token: X API Access Token
            access_token_secret: X API Access Token Secret
            bearer_token: Optional Bearer Token for v2 API (helpful for free tier)
        """
        try:
            # Initialize v1.1 client
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(auth, wait_on_rate_limit=True)
            
            # Initialize v2 client (can use OAuth or Bearer token)
            self.client_v2 = tweepy.Client(
                bearer_token=bearer_token,
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
                wait_on_rate_limit=True
            )
            
            logger.info("X API authentication successful (v1.1 + v2)")
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise
        
        self.sia = SentimentIntensityAnalyzer()
        self.preprocessor = TextPreprocessor()
        self.df = None
        self.results = {}
        self.output_dir = "tvk_campaign_output"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set style for visualizations
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
        
        logger.info("TVKCampaignAI initialized successfully")
    
    def fetch_data(self, query, count=100, since_date=None, until_date=None, use_v2=False):
        """Fetch real-time X posts with filters
        
        Args:
            query: Search query
            count: Number of tweets to fetch
            since_date: Start date (YYYY-MM-DD)
            until_date: End date (YYYY-MM-DD)
            use_v2: If True, use v2 API (for free tier). If False, try v1.1 first.
        """
        try:
            if since_date is None:
                # Default to last 7 days
                since_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            
            logger.info(f"Fetching data for query: '{query}'")
            logger.info(f"Parameters: count={count}, since={since_date}, use_v2={use_v2}")
            
            tweets = []
            
            # Try v1.1 first unless explicitly told to use v2
            if not use_v2:
                try:
                    logger.info("Attempting to fetch with v1.1 API...")
                    cursor = tweepy.Cursor(
                        self.api.search_tweets,
                        q=query,
                        lang="en",
                        since=since_date,
                        until=until_date,
                        tweet_mode="extended"
                    ).items(count)
                    
                    for tweet in cursor:
                        try:
                            tweets.append({
                                "id": tweet.id,
                                "text": tweet.full_text,
                                "author": tweet.user.screen_name,
                                "author_name": tweet.user.name,
                                "author_followers": tweet.user.followers_count,
                                "likes": tweet.favorite_count,
                                "retweets": tweet.retweet_count,
                                "replies": tweet.reply_count,
                                "engagement": tweet.favorite_count + tweet.retweet_count,
                                "timestamp": tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                                "hashtags": self.preprocessor.extract_hashtags(tweet.full_text),
                                "mentions": self.preprocessor.extract_mentions(tweet.full_text),
                                "location": tweet.user.location if hasattr(tweet.user, 'location') else None
                            })
                        except Exception as e:
                            logger.warning(f"Error processing tweet {tweet.id}: {e}")
                            continue
                    
                    logger.info("Successfully fetched with v1.1 API")
                    
                except tweepy.Unauthorized as e:
                    logger.warning("v1.1 API not available, falling back to v2 API")
                    use_v2 = True  # Fallback to v2
                except Exception as e:
                    logger.warning(f"v1.1 API error: {e}, falling back to v2 API")
                    use_v2 = True  # Fallback to v2
            
            # Use v2 API (for free tier or as fallback)
            if use_v2 or len(tweets) == 0:
                try:
                    logger.info("Fetching with v2 API (free tier compatible)...")
                    
                    # v2 API has different parameters
                    max_results = min(count, 100)  # v2 max is 100 per request
                    
                    # Convert date format for v2
                    # v2 uses ISO format or specific date format
                    start_time = None
                    if since_date:
                        try:
                            start_time = datetime.strptime(since_date, "%Y-%m-%d")
                            start_time = start_time.isoformat() + "Z"
                        except:
                            start_time = None
                    
                    # Fetch with v2 API
                    response = self.client_v2.search_recent_tweets(
                        query=query,
                        max_results=max_results,
                        tweet_fields=['created_at', 'public_metrics', 'author_id', 'text'],
                        user_fields=['username', 'name', 'public_metrics', 'location'],
                        expansions=['author_id'],
                        start_time=start_time
                    )
                    
                    if response and hasattr(response, 'data') and response.data:
                        # Get users for mapping
                        users_dict = {}
                        if hasattr(response, 'includes') and hasattr(response.includes, 'users'):
                            for user in response.includes.users:
                                users_dict[user.id] = user
                        
                        for tweet in response.data:
                            try:
                                # Get user info
                                user = users_dict.get(tweet.author_id)
                                author_username = user.username if user else "unknown"
                                author_name = user.name if user else "unknown"
                                # v2 API has public_metrics object for user
                                user_metrics = user.public_metrics if hasattr(user, 'public_metrics') else {}
                                author_followers = user_metrics.get('followers_count', 0) if isinstance(user_metrics, dict) else 0
                                location = user.location if user and hasattr(user, 'location') else None
                                
                                # Get metrics
                                metrics = tweet.public_metrics if hasattr(tweet, 'public_metrics') else {}
                                likes = metrics.get('like_count', 0)
                                retweets = metrics.get('retweet_count', 0)
                                replies = metrics.get('reply_count', 0)
                                
                                tweets.append({
                                    "id": tweet.id,
                                    "text": tweet.text,
                                    "author": author_username,
                                    "author_name": author_name,
                                    "author_followers": author_followers,
                                    "likes": likes,
                                    "retweets": retweets,
                                    "replies": replies,
                                    "engagement": likes + retweets,
                                    "timestamp": tweet.created_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(tweet.created_at, 'strftime') else str(tweet.created_at),
                                    "hashtags": self.preprocessor.extract_hashtags(tweet.text),
                                    "mentions": self.preprocessor.extract_mentions(tweet.text),
                                    "location": location
                                })
                            except Exception as e:
                                logger.warning(f"Error processing tweet {tweet.id}: {e}")
                                continue
                        
                        logger.info("Successfully fetched with v2 API")
                    else:
                        logger.warning("No data in v2 API response")
                        
                except tweepy.TooManyRequests:
                    logger.error("Rate limit exceeded. Please wait and try again later.")
                    return None
                except tweepy.TweepyException as e:
                    logger.error(f"v2 API error: {e}")
                    return None
            
            self.df = pd.DataFrame(tweets)
            
            if self.df.empty:
                logger.warning("No data fetched. Check query or API limits.")
                return None
            
            # Preprocess text
            self.df['cleaned_text'] = self.df['text'].apply(self.preprocessor.clean_text)
            
            logger.info(f"Successfully fetched {len(self.df)} posts")
            return self.df
                
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return None
    
    def analyze_sentiment(self):
        """Classify posts as positive/negative/neutral using VADER"""
        if self.df is None or self.df.empty:
            logger.warning("No data available for sentiment analysis")
            return None
        
        logger.info("Performing sentiment analysis...")
        
        def get_sentiment(text):
            scores = self.sia.polarity_scores(text)
            compound = scores['compound']
            
            if compound > 0.05:
                return 'positive'
            elif compound < -0.05:
                return 'negative'
            else:
                return 'neutral'
        
        self.df['sentiment'] = self.df['cleaned_text'].apply(get_sentiment)
        self.df['sentiment_score'] = self.df['cleaned_text'].apply(
            lambda x: self.sia.polarity_scores(x)['compound']
        )
        
        sentiment_counts = self.df['sentiment'].value_counts()
        self.results['sentiment'] = sentiment_counts.to_dict()
        
        logger.info(f"Sentiment analysis complete: {sentiment_counts.to_dict()}")
        return sentiment_counts
    
    def detect_trends(self, top_n=20):
        """Extract top keywords and hashtags using TF-IDF"""
        if self.df is None or self.df.empty:
            logger.warning("No data available for trend detection")
            return None
        
        logger.info("Detecting trends...")
        
        # TF-IDF analysis
        try:
            vectorizer = TfidfVectorizer(
                stop_words='english',
                max_features=top_n,
                ngram_range=(1, 2),
                min_df=2
            )
            tfidf_matrix = vectorizer.fit_transform(self.df['cleaned_text'])
            feature_names = vectorizer.get_feature_names_out()
            
            # Get top keywords
            scores = tfidf_matrix.sum(axis=0).A1
            top_indices = scores.argsort()[-top_n:][::-1]
            top_keywords = [feature_names[i] for i in top_indices]
            keyword_scores = [scores[i] for i in top_indices]
            
            self.results['top_keywords'] = dict(zip(top_keywords, keyword_scores))
            logger.info(f"Top keywords: {top_keywords[:10]}")
            
        except Exception as e:
            logger.error(f"Error in TF-IDF analysis: {e}")
            top_keywords = []
        
        # Hashtag analysis
        all_hashtags = []
        for hashtags in self.df['hashtags']:
            all_hashtags.extend(hashtags)
        
        hashtag_counts = pd.Series(all_hashtags).value_counts()
        top_hashtags = hashtag_counts.head(top_n).to_dict()
        self.results['top_hashtags'] = top_hashtags
        
        logger.info(f"Top hashtags: {list(top_hashtags.keys())[:10]}")
        
        return {
            'keywords': self.results.get('top_keywords', {}),
            'hashtags': self.results.get('top_hashtags', {})
        }
    
    def cluster_topics(self, num_clusters=3):
        """Group posts into topics using K-Means"""
        if self.df is None or self.df.empty:
            logger.warning("No data available for topic clustering")
            return None
        
        logger.info(f"Clustering topics into {num_clusters} groups...")
        
        try:
            # Adjust clusters based on data size
            if len(self.df) < num_clusters:
                num_clusters = max(1, len(self.df) - 1)
                logger.warning(f"Adjusting clusters to {num_clusters} based on data size")
            
            vectorizer = TfidfVectorizer(
                stop_words='english',
                max_features=100,
                min_df=2
            )
            X = vectorizer.fit_transform(self.df['cleaned_text'])
            
            kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
            self.df['cluster'] = kmeans.fit_predict(X)
            
            # Get representative terms for each cluster
            cluster_terms = {}
            for i in range(num_clusters):
                cluster_texts = self.df[self.df['cluster'] == i]['cleaned_text']
                if len(cluster_texts) > 0:
                    cluster_vectorizer = TfidfVectorizer(
                        stop_words='english',
                        max_features=5
                    )
                    try:
                        cluster_tfidf = cluster_vectorizer.fit_transform(cluster_texts)
                        terms = cluster_vectorizer.get_feature_names_out()
                        cluster_terms[i] = terms.tolist()
                    except:
                        cluster_terms[i] = []
            
            self.results['clusters'] = {
                'cluster_counts': self.df['cluster'].value_counts().to_dict(),
                'cluster_terms': cluster_terms
            }
            
            logger.info("Topic clustering complete")
            return self.results['clusters']
            
        except Exception as e:
            logger.error(f"Error in clustering: {e}")
            return None
    
    def map_influencers(self):
        """Build network graphs for users based on mentions/replies"""
        if self.df is None or self.df.empty:
            logger.warning("No data available for influencer mapping")
            return None
        
        logger.info("Mapping influencer network...")
        
        try:
            G = nx.DiGraph()
            
            for _, row in self.df.iterrows():
                author = row['author']
                
                # Add author as node with attributes
                if not G.has_node(author):
                    G.add_node(
                        author,
                        followers=row['author_followers'],
                        likes=row['likes'],
                        retweets=row['retweets']
                    )
                
                # Add edges for mentions
                mentions = row['mentions']
                for mention in mentions:
                    mention_clean = mention.replace('@', '')
                    if not G.has_node(mention_clean):
                        G.add_node(mention_clean)
                    G.add_edge(author, mention_clean, weight=1)
            
            if len(G.nodes) == 0:
                logger.warning("No nodes to visualize")
                return None
            
            # Calculate centrality metrics
            try:
                degree_centrality = nx.degree_centrality(G)
                betweenness_centrality = nx.betweenness_centrality(G)
                top_influencers = sorted(
                    degree_centrality.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10]
                
                self.results['top_influencers'] = [
                    {'user': user, 'centrality': score}
                    for user, score in top_influencers
                ]
                
                logger.info(f"Top influencers: {[u[0] for u in top_influencers[:5]]}")
                
            except Exception as e:
                logger.warning(f"Could not calculate centrality: {e}")
                self.results['top_influencers'] = []
            
            return G
            
        except Exception as e:
            logger.error(f"Error in influencer mapping: {e}")
            return None
    
    def visualize_sentiment(self):
        """Generate sentiment distribution bar chart"""
        if 'sentiment' not in self.results:
            logger.warning("No sentiment data to visualize")
            return None
        
        try:
            sentiment_counts = pd.Series(self.results['sentiment'])
            
            plt.figure(figsize=(10, 6))
            sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette=['#ff4444', '#dddddd', '#44ff44'])
            plt.title("Sentiment Distribution", fontsize=16, fontweight='bold')
            plt.xlabel("Sentiment", fontsize=12)
            plt.ylabel("Number of Posts", fontsize=12)
            plt.tight_layout()
            
            filepath = os.path.join(self.output_dir, "sentiment_bar.png")
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            logger.info(f"Sentiment visualization saved to {filepath}")
            plt.close()
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error visualizing sentiment: {e}")
            return None
    
    def visualize_trends(self):
        """Generate wordcloud for trending topics"""
        if self.df is None or self.df.empty:
            logger.warning("No data available for wordcloud")
            return None
        
        try:
            # Combine top keywords and hashtags
            text_parts = []
            
            # Add top keywords (weighted)
            if 'top_keywords' in self.results:
                for keyword, score in self.results['top_keywords'].items():
                    # Repeat based on score to make them more prominent
                    text_parts.extend([keyword] * int(score * 100))
            
            # Add hashtags
            if 'top_hashtags' in self.results:
                for hashtag, count in self.results['top_hashtags'].items():
                    text_parts.extend([hashtag] * count)
            
            if not text_parts:
                # Fallback to all text
                text_parts = self.df['cleaned_text'].str.cat(sep=' ')
            
            text = ' '.join(text_parts if isinstance(text_parts, list) else [text_parts])
            
            if not text.strip():
                logger.warning("No text available for wordcloud")
                return None
            
            plt.figure(figsize=(12, 8))
            wc = WordCloud(
                width=1200,
                height=800,
                background_color='white',
                max_words=100,
                collocations=False
            ).generate(text)
            
            plt.imshow(wc, interpolation='bilinear')
            plt.axis("off")
            plt.title("Trending Topics Wordcloud", fontsize=16, fontweight='bold', pad=20)
            plt.tight_layout()
            
            filepath = os.path.join(self.output_dir, "trends_wordcloud.png")
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            logger.info(f"Trends wordcloud saved to {filepath}")
            plt.close()
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error visualizing trends: {e}")
            return None
    
    def visualize_clusters(self):
        """Generate cluster visualization"""
        if self.df is None or 'cluster' not in self.df.columns:
            logger.warning("No cluster data to visualize")
            return None
        
        try:
            # Use dimensionality reduction for better visualization
            from sklearn.decomposition import PCA
            from sklearn.preprocessing import StandardScaler
            
            vectorizer = TfidfVectorizer(stop_words='english', max_features=50)
            X = vectorizer.fit_transform(self.df['cleaned_text'])
            X_dense = X.toarray()
            
            # Standardize and apply PCA
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_dense)
            
            pca = PCA(n_components=2, random_state=42)
            X_pca = pca.fit_transform(X_scaled)
            
            plt.figure(figsize=(12, 8))
            scatter = plt.scatter(
                X_pca[:, 0],
                X_pca[:, 1],
                c=self.df['cluster'],
                cmap='viridis',
                s=50,
                alpha=0.6
            )
            plt.colorbar(scatter, label='Cluster')
            plt.title("Topic Clusters (PCA Visualization)", fontsize=16, fontweight='bold')
            plt.xlabel(f"First Principal Component ({pca.explained_variance_ratio_[0]:.2%})")
            plt.ylabel(f"Second Principal Component ({pca.explained_variance_ratio_[1]:.2%})")
            plt.tight_layout()
            
            filepath = os.path.join(self.output_dir, "clusters_scatter.png")
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            logger.info(f"Cluster visualization saved to {filepath}")
            plt.close()
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error visualizing clusters: {e}")
            return None
    
    def visualize_influencer_network(self, max_nodes=50):
        """Generate influencer network graph"""
        G = self.map_influencers()
        
        if G is None or len(G.nodes) == 0:
            logger.warning("No network data to visualize")
            return None
        
        try:
            # Limit nodes for visibility
            if len(G.nodes) > max_nodes:
                # Keep top nodes by degree
                degrees = dict(G.degree())
                top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:max_nodes]
                top_node_names = [node for node, _ in top_nodes]
                G = G.subgraph(top_nodes).copy()
            
            plt.figure(figsize=(16, 12))
            
            # Layout
            try:
                pos = nx.spring_layout(G, k=2, iterations=50)
            except:
                pos = nx.circular_layout(G)
            
            # Draw nodes
            node_sizes = [G.nodes[node].get('followers', 0) / 1000 for node in G.nodes()]
            nx.draw_networkx_nodes(
                G, pos,
                node_size=node_sizes,
                node_color='lightblue',
                alpha=0.7
            )
            
            # Draw edges
            nx.draw_networkx_edges(G, pos, alpha=0.3, arrows=True, arrowsize=10)
            
            # Draw labels
            nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
            
            plt.title("Influencer Network Graph", fontsize=16, fontweight='bold')
            plt.axis('off')
            plt.tight_layout()
            
            filepath = os.path.join(self.output_dir, "influencer_graph.png")
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            logger.info(f"Influencer network saved to {filepath}")
            plt.close()
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error visualizing network: {e}")
            return None
    
    def visualize_workflow(self):
        """Generate agent workflow flowchart"""
        try:
            dot = Digraph(comment='TVK Campaign AI Workflow', format='png')
            dot.attr(rankdir='TB', size='12,8')
            dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue')
            
            dot.node('A', 'User Input\n(Query + API Keys)')
            dot.node('B', 'Fetch Data\n(X API)')
            dot.node('C', 'Preprocess\n(Text Cleaning)')
            dot.node('D1', 'Sentiment\nAnalysis')
            dot.node('D2', 'Trend\nDetection')
            dot.node('D3', 'Topic\nClustering')
            dot.node('D4', 'Influencer\nMapping')
            dot.node('E', 'Visualizations')
            dot.node('F', 'Generate\nReports')
            dot.node('G', 'Strategy\nInsights')
            
            dot.edges([('A', 'B'), ('B', 'C')])
            dot.edge('C', 'D1')
            dot.edge('C', 'D2')
            dot.edge('C', 'D3')
            dot.edge('C', 'D4')
            dot.edge('D1', 'E')
            dot.edge('D2', 'E')
            dot.edge('D3', 'E')
            dot.edge('D4', 'E')
            dot.edge('E', 'F')
            dot.edge('F', 'G')
            
            filepath = os.path.join(self.output_dir, "agent_flow.png")
            dot.render(filepath.replace('.png', ''), format='png', cleanup=True)
            logger.info(f"Workflow diagram saved to {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error visualizing workflow: {e}")
            return None
    
    def generate_strategy_insights(self):
        """Generate campaign strategy recommendations based on analysis"""
        insights = []
        
        # Sentiment insights
        if 'sentiment' in self.results:
            sentiment = self.results['sentiment']
            total = sum(sentiment.values())
            if total > 0:
                pos_ratio = sentiment.get('positive', 0) / total
                neg_ratio = sentiment.get('negative', 0) / total
                
                if pos_ratio > 0.5:
                    insights.append("✅ Strong positive sentiment! Continue current messaging strategy.")
                elif neg_ratio > 0.5:
                    insights.append("⚠️ High negative sentiment detected. Consider messaging adjustments and addressing concerns.")
                else:
                    insights.append("⚖️ Neutral sentiment. Opportunity to strengthen positive messaging.")
        
        # Trend insights
        if 'top_keywords' in self.results and self.results['top_keywords']:
            top_keywords = list(self.results['top_keywords'].keys())[:5]
            insights.append(f"📊 Top trending keywords: {', '.join(top_keywords)}")
            insights.append("💡 Consider incorporating these trending terms in campaign messaging.")
        
        if 'top_hashtags' in self.results and self.results['top_hashtags']:
            top_hashtags = list(self.results['top_hashtags'].keys())[:5]
            insights.append(f"🏷️ Top hashtags: {', '.join(top_hashtags)}")
            insights.append("💡 Monitor and engage with posts using these hashtags for maximum visibility.")
        
        # Influencer insights
        if 'top_influencers' in self.results and self.results['top_influencers']:
            influencers = self.results['top_influencers'][:5]
            inf_names = [inf['user'] for inf in influencers]
            insights.append(f"👥 Key influencers: {', '.join(inf_names)}")
            insights.append("💡 Consider collaboration opportunities with these influential voices.")
        
        # Engagement insights
        if self.df is not None and not self.df.empty:
            avg_engagement = self.df['engagement'].mean()
            insights.append(f"📈 Average engagement per post: {avg_engagement:.1f} interactions")
            
            if avg_engagement > 50:
                insights.append("💡 High engagement rate! Content is resonating well with audience.")
            elif avg_engagement < 10:
                insights.append("💡 Lower engagement detected. Experiment with different content formats and timing.")
        
        # Cluster insights
        if 'clusters' in self.results and 'cluster_terms' in self.results['clusters']:
            cluster_terms = self.results['clusters']['cluster_terms']
            num_clusters = len(cluster_terms)
            insights.append(f"🎯 Identified {num_clusters} distinct topic clusters in discussions.")
            insights.append("💡 Create targeted messaging for each topic cluster to maximize relevance.")
        
        self.results['strategy_insights'] = insights
        return insights
    
    def generate_html_report(self):
        """Generate comprehensive HTML report"""
        try:
            html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>TVK Campaign AI - Analysis Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; }
        .stats { display: flex; flex-wrap: wrap; gap: 20px; margin: 20px 0; }
        .stat-card { background: #ecf0f1; padding: 15px; border-radius: 5px; flex: 1; min-width: 200px; }
        .stat-value { font-size: 32px; font-weight: bold; color: #3498db; }
        .stat-label { color: #7f8c8d; font-size: 14px; }
        .insight { background: #e8f5e9; border-left: 4px solid #4caf50; padding: 15px; margin: 10px 0; border-radius: 3px; }
        .insight.warning { background: #fff3e0; border-left-color: #ff9800; }
        .insight.positive { background: #e3f2fd; border-left-color: #2196f3; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #3498db; color: white; }
        tr:hover { background-color: #f5f5f5; }
        .image-container { text-align: center; margin: 30px 0; }
        .image-container img { max-width: 100%; height: auto; border-radius: 5px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .timestamp { color: #95a5a6; font-size: 14px; text-align: right; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: 'Courier New', monospace; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 TVK Campaign AI - Analysis Report</h1>
        <div class="timestamp">Generated: {timestamp}</div>
        
        <h2>📊 Executive Summary</h2>
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{total_posts}</div>
                <div class="stat-label">Total Posts Analyzed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{time_period}</div>
                <div class="stat-label">Analysis Period</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{unique_users}</div>
                <div class="stat-label">Unique Users</div>
            </div>
        </div>
        
        <h2>😊 Sentiment Analysis</h2>
        {sentiment_html}
        
        <h2>📈 Top Trends</h2>
        {trends_html}
        
        <h2>🎯 Topic Clusters</h2>
        {clusters_html}
        
        <h2>👥 Influencer Network</h2>
        {influencers_html}
        
        <h2>💡 Strategic Recommendations</h2>
        {insights_html}
        
        <h2>📊 Visualizations</h2>
        {visualizations_html}
        
        <div class="insight positive">
            <strong>⚖️ Legal Disclaimer:</strong> This analysis is for research purposes only. 
            Users must comply with X's Terms of Service, Indian election laws, and applicable regulations.
        </div>
        
        <div class="timestamp">
            <p>Report generated by TVKCampaignAI v1.0 | MIT License</p>
        </div>
    </div>
</body>
</html>
"""
            
            # Build HTML sections
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            total_posts = len(self.df) if self.df is not None else 0
            unique_users = len(self.df['author'].unique()) if self.df is not None and not self.df.empty else 0
            time_period = "Last 7 days"  # Could be made dynamic
            
            # Sentiment section
            sentiment_html = ""
            if 'sentiment' in self.results:
                sentiment = self.results['sentiment']
                sentiment_html = f"""
                <table>
                    <tr><th>Sentiment</th><th>Count</th><th>Percentage</th></tr>
                    {''.join([f'<tr><td>{s.capitalize()}</td><td>{count}</td><td>{(count/sum(sentiment.values())*100):.1f}%</td></tr>' 
                              for s, count in sentiment.items()])}
                </table>
                """
            
            # Trends section
            trends_html = ""
            if 'top_keywords' in self.results:
                keywords = list(self.results['top_keywords'].items())[:10]
                trends_html = f"""
                <h3>Top Keywords</h3>
                <table>
                    <tr><th>Keyword</th><th>TF-IDF Score</th></tr>
                    {''.join([f'<tr><td>{kw}</td><td>{score:.4f}</td></tr>' for kw, score in keywords])}
                </table>
                """
            
            if 'top_hashtags' in self.results:
                hashtags = list(self.results['top_hashtags'].items())[:10]
                trends_html += f"""
                <h3>Top Hashtags</h3>
                <table>
                    <tr><th>Hashtag</th><th>Mentions</th></tr>
                    {''.join([f'<tr><td>#{ht.replace("#", "")}</td><td>{count}</td></tr>' for ht, count in hashtags])}
                </table>
                """
            
            # Clusters section
            clusters_html = ""
            if 'clusters' in self.results and 'cluster_terms' in self.results['clusters']:
                cluster_terms = self.results['clusters']['cluster_terms']
                cluster_counts = self.results['clusters'].get('cluster_counts', {})
                clusters_html = "<table><tr><th>Cluster</th><th>Posts</th><th>Key Terms</th></tr>"
                for cluster_id, terms in cluster_terms.items():
                    count = cluster_counts.get(cluster_id, 0)
                    terms_str = ', '.join(terms) if terms else 'N/A'
                    clusters_html += f"<tr><td>{cluster_id}</td><td>{count}</td><td>{terms_str}</td></tr>"
                clusters_html += "</table>"
            
            # Influencers section
            influencers_html = ""
            if 'top_influencers' in self.results and self.results['top_influencers']:
                influencers_html = "<table><tr><th>Username</th><th>Centrality Score</th></tr>"
                for inf in self.results['top_influencers'][:10]:
                    influencers_html += f"<tr><td>@{inf['user']}</td><td>{inf['centrality']:.4f}</td></tr>"
                influencers_html += "</table>"
            
            # Insights section
            insights_html = ""
            if 'strategy_insights' in self.results:
                for insight in self.results['strategy_insights']:
                    css_class = 'positive' if '✅' in insight else ('warning' if '⚠️' in insight else '')
                    insights_html += f'<div class="insight {css_class}">{insight}</div>'
            
            # Visualizations section
            visualization_files = ['sentiment_bar.png', 'trends_wordcloud.png', 'clusters_scatter.png', 'influencer_graph.png', 'agent_flow.png']
            visualizations_html = ""
            for vis_file in visualization_files:
                filepath = os.path.join(self.output_dir, vis_file)
                if os.path.exists(filepath):
                    vis_name = vis_file.replace('_', ' ').replace('.png', '').title()
                    visualizations_html += f"""
                    <div class="image-container">
                        <h3>{vis_name}</h3>
                        <img src="{vis_file}" alt="{vis_name}">
                    </div>
                    """
            
            # Fill in the template
            html_content = html_content.format(
                timestamp=timestamp,
                total_posts=total_posts,
                time_period=time_period,
                unique_users=unique_users,
                sentiment_html=sentiment_html,
                trends_html=trends_html,
                clusters_html=clusters_html,
                influencers_html=influencers_html,
                insights_html=insights_html,
                visualizations_html=visualizations_html
            )
            
            # Save HTML report
            filepath = os.path.join(self.output_dir, "campaign_report.html")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"HTML report saved to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating HTML report: {e}")
            return None
    
    def generate_pdf_report(self):
        """Generate PDF report using reportlab or similar"""
        try:
            # Try using reportlab if available, otherwise use weasyprint or skip
            try:
                from reportlab.lib.pagesizes import letter, A4
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.units import inch
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
                from reportlab.lib.enums import TA_CENTER, TA_LEFT
                from reportlab.pdfgen import canvas
                from reportlab.lib import colors
                
                REPORTLAB_AVAILABLE = True
            except ImportError:
                REPORTLAB_AVAILABLE = False
                logger.warning("reportlab not available. Skipping PDF generation.")
                return None
            
            if not REPORTLAB_AVAILABLE:
                return None
            
            logger.info("Generating PDF report...")
            
            filepath = os.path.join(self.output_dir, "campaign_report.pdf")
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            
            # Container for content
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            story.append(Paragraph("🎯 TVK Campaign AI - Analysis Report", title_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Summary
            story.append(Paragraph("📊 Executive Summary", styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            if self.df is not None and not self.df.empty:
                summary_data = [
                    ['Metric', 'Value'],
                    ['Total Posts', str(len(self.df))],
                    ['Unique Users', str(len(self.df['author'].unique()))],
                    ['Analysis Period', 'Last 7 days']
                ]
                if 'sentiment' in self.results:
                    sentiment = self.results['sentiment']
                    summary_data.append(['Positive Sentiment', f"{sentiment.get('positive', 0)} posts"])
                    summary_data.append(['Negative Sentiment', f"{sentiment.get('negative', 0)} posts"])
                
                summary_table = Table(summary_data)
                summary_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(summary_table)
                story.append(Spacer(1, 0.3*inch))
            
            # Sentiment
            if 'sentiment' in self.results:
                story.append(Paragraph("😊 Sentiment Analysis", styles['Heading2']))
                story.append(Spacer(1, 0.1*inch))
                
                sentiment = self.results['sentiment']
                sentiment_data = [['Sentiment', 'Count', 'Percentage']]
                total = sum(sentiment.values())
                for s, count in sentiment.items():
                    pct = (count/total*100) if total > 0 else 0
                    sentiment_data.append([s.capitalize(), str(count), f"{pct:.1f}%"])
                
                sent_table = Table(sentiment_data)
                sent_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(sent_table)
                story.append(Spacer(1, 0.3*inch))
            
            # Strategic Insights
            if 'strategy_insights' in self.results:
                story.append(Paragraph("💡 Strategic Recommendations", styles['Heading2']))
                story.append(Spacer(1, 0.1*inch))
                
                for insight in self.results['strategy_insights']:
                    story.append(Paragraph(insight, styles['Normal']))
                    story.append(Spacer(1, 0.05*inch))
                
                story.append(Spacer(1, 0.2*inch))
            
            # Legal disclaimer
            disclaimer_style = ParagraphStyle(
                'Disclaimer',
                parent=styles['Normal'],
                fontStyle='italic',
                textColor=colors.grey
            )
            story.append(Paragraph("⚖️ <i>Legal Disclaimer:</i> This analysis is for research purposes only. Users must comply with X's Terms of Service, Indian election laws, and applicable regulations.", disclaimer_style))
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph("Report generated by TVKCampaignAI v1.0 | MIT License", disclaimer_style))
            
            # Build PDF
            doc.build(story)
            logger.info(f"PDF report saved to {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating PDF report: {e}")
            return None
    
    def run_parallel_analysis(self):
        """Run all analyses in parallel for efficiency"""
        logger.info("Running parallel analysis pipeline...")
        
        def run_sentiment():
            return self.analyze_sentiment()
        
        def run_trends():
            return self.detect_trends()
        
        def run_clusters():
            return self.cluster_topics()
        
        def run_influencers():
            return self.map_influencers()
        
        # Run analyses in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                'sentiment': executor.submit(run_sentiment),
                'trends': executor.submit(run_trends),
                'clusters': executor.submit(run_clusters),
                'influencers': executor.submit(run_influencers)
            }
            
            # Wait for all to complete
            for name, future in futures.items():
                try:
                    future.result()
                    logger.info(f"{name} analysis complete")
                except Exception as e:
                    logger.error(f"Error in {name} analysis: {e}")
    
    def run(self, query, count=100, since_date=None, generate_reports=True):
        """Main execution pipeline"""
        logger.info("=" * 60)
        logger.info("Starting TVK Campaign AI Analysis")
        logger.info("=" * 60)
        
        # Fetch data
        df = self.fetch_data(query, count=count, since_date=since_date)
        
        if df is None or df.empty:
            logger.error("No data to analyze. Exiting.")
            return None
        
        print(f"\n✅ Fetched {len(self.df)} posts successfully!")
        
        # Run analyses
        self.run_parallel_analysis()
        
        # Generate visualizations
        print("\n📊 Generating visualizations...")
        self.visualize_sentiment()
        self.visualize_trends()
        self.visualize_clusters()
        self.visualize_influencer_network()
        self.visualize_workflow()
        print("✅ All visualizations generated!")
        
        # Generate strategy insights
        print("\n💡 Generating strategic insights...")
        insights = self.generate_strategy_insights()
        for insight in insights:
            print(f"  {insight}")
        
        # Generate reports
        if generate_reports:
            print("\n📄 Generating reports...")
            self.generate_html_report()
            self.generate_pdf_report()
            print("✅ Reports generated!")
        
        # Summary
        print("\n" + "=" * 60)
        print("🎉 Analysis Complete!")
        print("=" * 60)
        print(f"\nOutput directory: {os.path.abspath(self.output_dir)}")
        print("\nGenerated files:")
        for file in os.listdir(self.output_dir):
            print(f"  - {file}")
        
        return self.results


# Example usage
if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                   TVK Campaign AI - Example Usage                     ║
    ║                                                                       ║
    ║  This agent requires valid X (Twitter) API credentials to fetch      ║
    ║  real-time data. Replace the placeholders below with your actual     ║
    ║  credentials from the X Developer Portal.                            ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    
    To use this agent:
    1. Sign up at https://developer.twitter.com
    2. Create a new app and generate API keys
    3. Replace the credentials in the code below
    4. Run: python tvk_agent.py
    
    ⚠️  IMPORTANT: 
    - Comply with X's Terms of Service
    - Follow Indian election laws
    - Use responsibly and ethically
    
    """)
    
    # Example credentials (REPLACE WITH YOUR ACTUAL KEYS)
    CONSUMER_KEY = "your_consumer_key_here"
    CONSUMER_SECRET = "your_consumer_secret_here"
    ACCESS_TOKEN = "your_access_token_here"
    ACCESS_TOKEN_SECRET = "your_access_token_secret_here"
    
    # Uncomment and modify the query below to run analysis
    """
    # Initialize agent
    agent = TVKCampaignAI(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    
    # Run analysis
    results = agent.run(
        query="TVK Tamil Nadu elections 2026",
        count=100,
        generate_reports=True
    )
    """
    
    print("\n📝 Note: Edit the CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN,")
    print("   and ACCESS_TOKEN_SECRET variables with your actual credentials")
    print("   to run the analysis.")
