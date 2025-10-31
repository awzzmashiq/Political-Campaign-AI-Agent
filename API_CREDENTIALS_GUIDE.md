# X API Credentials Setup Guide

## Credentials You Have

✅ **API Key**: `TqceYUtn10fky0fFknZA59XS7`
✅ **API Key Secret**: `DFgn0Je4C8db3cDozfXw1Rr71XlM0Rh5W4EAnArfrAqdnUe7xc`

## Credentials You Need

❌ **Access Token**: Need to generate
❌ **Access Token Secret**: Need to generate

## How to Get Access Token and Secret

### Option 1: Using X Developer Portal (Recommended)

1. **Log in** to [X Developer Portal](https://developer.twitter.com)
2. **Navigate** to your app dashboard
3. **Click** on your app/project
4. **Go to** "Keys and tokens" tab
5. Under **"Access Token and Secret"** section:
   - Click **"Generate"** button
   - Copy the **Access Token** (long string of characters)
   - Copy the **Access Token Secret** (long string of characters)
6. **Save** these credentials securely

### Option 2: Using OAuth 2.0 (Advanced)

If you need to generate tokens dynamically or for production use, you'll need to implement OAuth 2.0 flow.

## Quick Setup Once You Have All 4 Credentials

### Method 1: Update example.py

Edit `example.py` and replace lines 31-34 with your credentials:

```python
CONSUMER_KEY = "TqceYUtn10fky0fFknZA59XS7"
CONSUMER_SECRET = "DFgn0Je4C8db3cDozfXw1Rr71XlM0Rh5W4EAnArfrAqdnUe7xc"
ACCESS_TOKEN = "your_access_token_here"
ACCESS_TOKEN_SECRET = "your_access_token_secret_here"
```

### Method 2: Use .env file (More Secure)

Create a `.env` file in the project root:

```env
TWITTER_CONSUMER_KEY=TqceYUtn10fky0fFknZA59XS7
TWITTER_CONSUMER_SECRET=DFgn0Je4C8db3cDozfXw1Rr71XlM0Rh5W4EAnArfrAqdnUe7xc
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
```

Then uncomment line 11 in `example.py`:
```python
load_dotenv()
```

And uncomment lines 24-27:
```python
CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
```

## Security Best Practices

⚠️ **IMPORTANT**: 

1. **NEVER** commit your credentials to Git
2. The `.gitignore` file already excludes `.env` files
3. **Don't share** credentials publicly
4. **Rotate** credentials if they're exposed
5. Use environment variables for production

## Testing Your Credentials

Once you have all 4 credentials:

```bash
# Install dependencies first
pip install -r requirements.txt

# Run the example script
python example.py
```

If credentials are valid, you should see:
```
✅ Agent initialized successfully!
```

If you get an authentication error, double-check:
- All 4 credentials are correct
- No extra spaces before/after
- Credentials are from the same app/project
- Your X Developer account is active

## Troubleshooting

### "Invalid credentials" error
- Verify all 4 credentials are correct
- Ensure credentials are from the same X Developer project
- Check if your X Developer account is in good standing

### "Forbidden" or "Unauthorized" error
- Your app might need elevated access
- Apply for elevated access in X Developer Portal
- Wait for approval (usually 24-48 hours)

### "Rate limit exceeded" error
- This is normal for free tier
- Wait 15 minutes and try again
- Consider upgrading your X Developer account

## Getting More Help

- [X Developer Documentation](https://developer.twitter.com/en/docs)
- [X API v2 Documentation](https://developer.twitter.com/en/docs/twitter-api)
- [Authentication Guide](https://developer.twitter.com/en/docs/authentication/overview)

---

**Next Step**: Get your Access Token and Access Token Secret from the X Developer Portal, then run the agent!

