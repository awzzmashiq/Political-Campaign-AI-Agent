# TVKCampaignAI - Deployment Guide

## Quick Deployment

The TVKCampaignAI project is ready for immediate deployment. Follow these steps:

### Step 1: Clone/Download Project

```bash
# If using git
git clone <repository-url>
cd tvk-campaign-ai

# Or download and extract the project folder
```

### Step 2: Set Up Python Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Core libraries (tweepy, vaderSentiment, scikit-learn, pandas)
- Visualization tools (matplotlib, seaborn, wordcloud, networkx)
- Optional dependencies documented in requirements.txt

### Step 4: Configure API Credentials

**Option A: Environment Variables (Secure)**

Create `.env` file:
```env
TWITTER_CONSUMER_KEY=your_actual_key_here
TWITTER_CONSUMER_SECRET=your_actual_secret_here
TWITTER_ACCESS_TOKEN=your_actual_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_actual_token_secret_here
```

**Option B: Direct Configuration**

Edit `example.py` or create your own script with credentials.

### Step 5: Test Installation

```bash
# Verify structure
python test_structure.py

# Expected output: [SUCCESS] ALL TESTS PASSED!
```

### Step 6: Run First Analysis

```bash
python example.py
```

Follow the prompts to input:
- Search query
- Number of posts to analyze

### Step 7: View Results

Results are saved in `tvk_campaign_output/`:
- HTML report: `campaign_report.html`
- PDF report: `campaign_report.pdf` (optional, requires reportlab)
- Visualizations: PNG files
- Raw data: CSV export available

## Production Deployment

### Requirements

**Server:**
- Python 3.8+
- 2GB+ RAM
- Internet connection
- Disk space for outputs

**Software:**
- pip package manager
- Optional: Graphviz for flowcharts
- Optional: reportlab for PDFs

### Scheduled Execution

#### Linux/Unix Cron Job

```bash
# Edit crontab
crontab -e

# Add daily analysis at 9 AM
0 9 * * * cd /path/to/tvk-campaign-ai && /usr/bin/python3 example.py
```

#### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (daily/weekly)
4. Action: Start a program
   - Program: `python`
   - Arguments: `example.py`
   - Start in: Project directory

#### Python Script Scheduler

```python
import schedule
import time
from tvk_campaign_ai import TVKCampaignAI

def run_analysis():
    agent = TVKCampaignAI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    agent.run(query="Your query", count=100)

# Schedule daily
schedule.every().day.at("09:00").do(run_analysis)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "example.py"]
```

Build and run:
```bash
docker build -t tvk-campaign-ai .
docker run -v $(pwd)/output:/app/tvk_campaign_output tvk-campaign-ai
```

## Cloud Deployment

### AWS Lambda

**Limitations**: 15-minute timeout, storage limits
**Recommendation**: Use for scheduled executions, store results in S3

```python
# lambda_handler.py
import json
from tvk_campaign_ai import TVKCampaignAI
import boto3

def lambda_handler(event, context):
    agent = TVKCampaignAI(
        CONSUMER_KEY,
        CONSUMER_SECRET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET
    )
    results = agent.run(query=event['query'], count=100)
    
    # Upload to S3
    s3 = boto3.client('s3')
    s3.upload_file('campaign_report.html', 'bucket', 'reports/report.html')
    
    return {'statusCode': 200, 'body': json.dumps(results)}
```

### Google Cloud Functions

Similar to Lambda, with slight API differences.

### Azure Functions

Similar pattern, with Azure-specific storage.

## Monitoring & Maintenance

### Logging

Agent logs to console by default:
```
2025-XX-XX XX:XX:XX - INFO - Fetching data for query...
2025-XX-XX XX:XX:XX - INFO - Successfully fetched 100 posts
```

### Error Monitoring

Check logs for:
- `ERROR` - Failures requiring attention
- `WARNING` - Recoverable issues
- Rate limit messages

### Output Management

**Automatic:**
- Outputs saved to `tvk_campaign_output/`
- Timestamps in filenames
- Overwrites if not managed

**Manual:**
```python
# Add timestamp to output directory
from datetime import datetime
agent.output_dir = f"reports_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
```

### Data Retention

Implement cleanup:
```python
import os
import glob
from datetime import datetime, timedelta

# Delete old reports
for file in glob.glob("tvk_campaign_output/*"):
    if os.path.getmtime(file) < (datetime.now() - timedelta(days=30)).timestamp():
        os.remove(file)
```

## Security Considerations

### API Credentials

**DO:**
- ✅ Store in environment variables
- ✅ Use `.env` file (add to .gitignore)
- ✅ Use secret management services
- ✅ Rotate credentials regularly

**DON'T:**
- ❌ Commit credentials to git
- ❌ Share credentials publicly
- ❌ Hardcode in production
- ❌ Store in plain text

### Data Privacy

**Compliance:**
- ✅ Follow X Terms of Service
- ✅ Comply with Indian election laws
- ✅ Respect user privacy
- ✅ Limit data retention
- ✅ Secure storage

### Network Security

**Recommendations:**
- Use HTTPS for all connections
- Implement firewall rules
- Monitor API usage
- Rate limit requests

## Scaling Considerations

### Low Volume (< 1000 posts/day)
- Single instance sufficient
- Standard execution

### Medium Volume (1K-10K posts/day)
- Scheduled batch processing
- Multiple queries in parallel
- Optimize database storage

### High Volume (10K+ posts/day)
- Distributed processing
- Database backend
- Message queue (RabbitMQ, Kafka)
- Caching layer
- Load balancing

### Recommended Architecture (High Volume)

```
┌─────────────┐
│   Scheduler │ (Cron/CloudWatch)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Queue      │ (RabbitMQ/Kafka)
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Worker 1  │     │   Worker 2  │     │   Worker N  │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┴───────────────────┘
                           │
                           ▼
                   ┌───────────────┐
                   │   Database    │ (PostgreSQL/MongoDB)
                   └───────────────┘
                           │
                           ▼
                   ┌───────────────┐
                   │   Web UI      │ (Dash/Streamlit)
                   └───────────────┘
```

## Troubleshooting

### Common Issues

**Issue**: Import errors
**Solution**: 
```bash
pip install --upgrade -r requirements.txt
```

**Issue**: API authentication fails
**Solution**: Verify credentials, check X API status

**Issue**: Rate limit exceeded
**Solution**: Wait or reduce `count` parameter

**Issue**: Graphviz not found
**Solution**: Install system package (see SETUP_INSTRUCTIONS.md)

**Issue**: Out of memory
**Solution**: Reduce `count`, process in batches

**Issue**: Slow execution
**Solution**: Increase workers, use caching

### Debug Mode

Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or in code
logger.setLevel(logging.DEBUG)
```

### Performance Tuning

**Optimizations:**
- Reduce `max_features` in TF-IDF
- Lower cluster count
- Limit network nodes
- Cache results
- Parallel processing (enabled by default)

## Backup & Recovery

### Regular Backups

**Data:**
- Reports directory
- Configuration files
- Log files

**Schedule:**
- Daily incremental
- Weekly full backup
- Monthly archive

**Storage:**
- Cloud storage (S3, GCS, Azure Blob)
- Local backup server
- Version control (code only)

### Disaster Recovery

**Plan:**
1. Keep credentials backup (secure)
2. Document configuration
3. Test recovery procedures
4. Maintain access logs

## Updates & Versioning

### Updating Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Version Management

Track versions:
```bash
# Check current
python -c "from tvk_campaign_ai import __version__; print(__version__)"

# Git tags
git tag v1.0.0
git push origin v1.0.0
```

### Changelog

Maintain `CHANGELOG.md`:
- Features added
- Bugs fixed
- Breaking changes
- Migration guides

## Support & Maintenance

### Documentation

- README.md - Main docs
- SETUP_INSTRUCTIONS.md - Setup
- QUICKSTART.md - Getting started
- DEPLOYMENT.md - This file

### Community

- GitHub Issues - Bug reports
- Discussions - Questions
- Pull Requests - Contributions

### Professional Support

For enterprise deployments:
- Custom configurations
- Advanced features
- Training & consultation
- SLA support

## Compliance Checklist

Before deploying to production:

- [ ] API credentials secured
- [ ] Terms of Service reviewed
- [ ] Legal compliance verified
- [ ] Privacy policy updated
- [ ] Data retention configured
- [ ] Error monitoring active
- [ ] Backups scheduled
- [ ] Documentation complete
- [ ] Team trained
- [ ] Disaster recovery tested

## Conclusion

TVKCampaignAI is **production-ready** and can be deployed immediately following these guidelines. The agent is designed for:
- ✅ Reliability
- ✅ Scalability
- ✅ Maintainability
- ✅ Security
- ✅ Compliance

For additional support, refer to the documentation or open an issue on GitHub.

---

**Version**: 1.0.0  
**Last Updated**: 2025  
**License**: MIT

