# 🚀 How to Use TVKCampaignAI

## 📋 Quick Decision Guide

**Choose your interface:**

### 🌐 Web Interface (Easiest!)
**Best for**: Most users, visual learners, presentations

👉 **Run**: `streamlit run app.py`

### 💻 Terminal Interface  
**Best for**: Automation, scripts, advanced users

👉 **Run**: `python example.py`

---

## 🌐 Using the Web Interface

### Step 1: Start the Web Server

```bash
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501`

### Step 2: Initialize the Agent

In the **sidebar** (left side):
1. ✅ "Use Pre-configured Credentials" is already checked
2. Click **"🔌 Initialize Agent"**
3. Wait for **"✅ Agent Ready"** message

### Step 3: Run Analysis

In the **main area**:
1. Enter your **search query** (e.g., "TVK Tamil Nadu elections 2026")
2. Choose **number of posts** (default: 100)
3. Click **"🚀 Run Analysis"**
4. Wait for results (progress bar shows status)

### Step 4: Explore Results

Results appear in **5 tabs**:
- **📊 Sentiment** - How people feel
- **📈 Trends** - Top keywords & hashtags
- **🎯 Topics** - Cluster groups
- **👥 Influencers** - Key users
- **💡 Insights** - Recommendations

### Step 5: Export

- Click **"📥 Download CSV"** to save data
- View generated reports in `tvk_campaign_output/` folder

**That's it!** Easy, right? 🎉

---

## 💻 Using the Terminal Interface

### Step 1: Run the Script

```bash
python example.py
```

### Step 2: Follow Prompts

```
Enter your search query (or press Enter for default): 
```
→ Type your query or press Enter

```
How many posts to analyze? (default: 100):
```
→ Enter number or press Enter

### Step 3: Wait for Results

The script will:
1. Fetch data
2. Analyze sentiment
3. Detect trends
4. Cluster topics
5. Map influencers
6. Generate reports
7. Show summary

### Step 4: View Outputs

Check the `tvk_campaign_output/` folder for:
- Charts (PNG files)
- Reports (HTML/PDF)
- Data (CSV)

**Done!** Results saved automatically.

---

## ⚙️ Configuration Options

### Query Examples

**Simple**:
- "TVK Tamil Nadu"
- "elections 2026"
- "#TVK"

**Advanced**:
- "TVK OR Vijayakanth"
- "Tamil Nadu elections 2026"
- "(TVK OR TVKParty) AND elections"

### Parameters

**Number of Posts**:
- 10-50: Quick check
- 100-200: Standard analysis
- 300-500: Comprehensive study
- 500+: Deep research

**Date Filters**:
- Last 7 days (default)
- Last 30 days
- Custom range

---

## 🎯 Pro Tips

### For Better Results

1. **Use specific queries** - Avoid too broad searches
2. **Recent data** - Stay within last 30 days
3. **Right size** - 100-500 posts is optimal
4. **Check regularly** - Run weekly for trends

### For Performance

1. **Start small** - Test with 50 posts first
2. **Increase gradually** - Scale up if needed
3. **Use filters** - Narrow down searches
4. **Export data** - Save for later analysis

### For Team Use

1. **Web UI** - Perfect for meetings
2. **Export reports** - Share insights
3. **Document findings** - Keep notes
4. **Schedule runs** - Regular updates

---

## 🔧 Troubleshooting

### "Agent Not Initialized"
**Fix**: 
- Check sidebar credentials
- Click "Initialize Agent" again
- Verify API access

### "No Data Found"
**Fix**:
- Broaden search query
- Check API access tier
- Try different keywords

### "Analysis Failed"
**Fix**:
- Check internet connection
- Verify credentials
- Review error message
- Check API limits

### Web UI Won't Start
**Fix**:
```bash
pip install streamlit
streamlit run app.py
```

### Terminal Errors
**Fix**:
```bash
pip install -r requirements.txt
python example.py
```

---

## 📚 Need More Help?

### Documentation Files

1. **[README.md](README.md)** - Complete guide
2. **[START_HERE.md](START_HERE.md)** - Best starting point
3. **[WEB_UI_GUIDE.md](WEB_UI_GUIDE.md)** - Web interface details
4. **[QUICKSTART.md](QUICKSTART.md)** - Quick reference
5. **[API_ACCESS_REQUIREMENTS.md](API_ACCESS_REQUIREMENTS.md)** - API info

### Quick Links

- Web UI: `streamlit run app.py`
- Terminal: `python example.py`
- Documentation: See files above
- Support: Check error messages

---

## ✅ Checklist

Before running:

- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Credentials configured (already done!)
- [ ] Choose interface (Web or Terminal)
- [ ] Know your search query
- [ ] Ready to analyze!

After running:

- [ ] Results displayed
- [ ] Visualizations shown
- [ ] Data exported (if needed)
- [ ] Reports generated
- [ ] Insights reviewed

---

## 🎉 You're Ready!

**Choose your interface and start analyzing!**

- 🌐 **Web**: `streamlit run app.py`
- 💻 **Terminal**: `python example.py`

**Enjoy TVKCampaignAI!** 🚀

---

**Questions?** Check the documentation files listed above!

