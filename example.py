"""
Example script demonstrating TVKCampaignAI usage
Replace the API credentials with your actual X Developer credentials
"""

from tvk_campaign_ai import TVKCampaignAI
import os
from dotenv import load_dotenv

# Load environment variables if using .env file
# load_dotenv()

def main():
    """
    Example usage of TVKCampaignAI
    """
    print("""
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                   TVK Campaign AI - Example Run                       ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Option 1: Load from environment variables (recommended for security)
    # CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
    # CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
    # ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    # ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    
    # Option 2: Direct configuration
    # Your X API credentials
    CONSUMER_KEY = "TqceYUtn10fky0fFknZA59XS7"
    CONSUMER_SECRET = "DFgn0Je4C8db3cDozfXw1Rr71XlM0Rh5W4EAnArfrAqdnUe7xc"
    ACCESS_TOKEN = "1624801416-1vDoeigmNu1utvZlK2NpyOg6WGRhyohHmIqZ3Mx"
    ACCESS_TOKEN_SECRET = "dNvj2S7sTM1UNMbajTySqXP17EcaBgukCrGGz0oH4M4Cn"
    
    # Bearer Token (for v2 API - free tier)
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAJSf5AEAAAAAG8gOwPA9Wlib5UVxEgc0GH6RMrk%3DIPYqK0bVdHc6cZtkyN5st6ncETfqTDuoYVYvIXJlfGDPisMjdt"
    
    # Check if credentials are set
    if not all([CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
        print("""
        ⚠️  WARNING: Missing API credentials!
        
        Please ensure all 4 credentials are set in example.py:
        - Consumer Key
        - Consumer Secret
        - Access Token
        - Access Token Secret
        
        For detailed instructions, see: API_CREDENTIALS_GUIDE.md
        
        """)
        return
    
    try:
        # Initialize the agent
        print("Initializing TVKCampaignAI agent...")
        agent = TVKCampaignAI(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET,
            bearer_token=BEARER_TOKEN
        )
        print("✅ Agent initialized successfully!\n")
        
        # Define your search query
        # Example queries:
        # - "TVK Tamil Nadu elections 2026"
        # - "#TVK OR #Vijaykanth OR #Vijayakanth"
        # - "Tamil Nadu elections AND (Vijayakanth OR TVK)"
        
        query = input("Enter your search query (or press Enter for default): ").strip()
        if not query:
            query = "TVK Tamil Nadu elections 2026"  # Default query
        
        # Get number of posts to analyze
        count_input = input("How many posts to analyze? (default: 100): ").strip()
        count = int(count_input) if count_input.isdigit() else 100
        
        print(f"\nStarting analysis with query: '{query}'")
        print(f"Fetching up to {count} posts...\n")
        
        # Run the complete analysis pipeline
        results = agent.run(
            query=query,
            count=count,
            generate_reports=True
        )
        
        if results:
            print("\n" + "="*60)
            print("Analysis Summary:")
            print("="*60)
            
            # Display key results
            if 'sentiment' in results:
                print("\nSentiment Distribution:")
                for sentiment, count in results['sentiment'].items():
                    print(f"  {sentiment.capitalize()}: {count}")
            
            if 'top_keywords' in results:
                print("\nTop Keywords:")
                for i, (keyword, score) in enumerate(list(results['top_keywords'].items())[:10], 1):
                    print(f"  {i}. {keyword}: {score:.4f}")
            
            if 'top_hashtags' in results:
                print("\nTop Hashtags:")
                for i, (hashtag, count) in enumerate(list(results['top_hashtags'].items())[:10], 1):
                    print(f"  {i}. #{hashtag}: {count} mentions")
            
            if 'top_influencers' in results and results['top_influencers']:
                print("\nTop Influencers:")
                for i, inf in enumerate(results['top_influencers'][:5], 1):
                    print(f"  {i}. @{inf['user']}: {inf['centrality']:.4f}")
            
            if 'strategy_insights' in results:
                print("\nStrategic Recommendations:")
                for insight in results['strategy_insights']:
                    print(f"  {insight}")
            
            print("\n" + "="*60)
            print("🎉 Analysis complete!")
            print("="*60)
            print(f"\nAll outputs saved to: {os.path.abspath(agent.output_dir)}")
            
        else:
            print("\n❌ Analysis failed or returned no results.")
            print("Possible reasons:")
            print("  - No matching posts found for the query")
            print("  - API rate limits exceeded")
            print("  - Invalid API credentials")
            print("  - Network connectivity issues")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease check:")
        print("  - Your API credentials are correct")
        print("  - You have internet connectivity")
        print("  - X API is accessible")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
