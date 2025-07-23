# RSS News Parser

A comprehensive Python script for fetching, parsing, and analyzing RSS news feeds with advanced filtering, deduplication, and optional AI-powered insights.

## Features

- 📰 **Multi-source RSS feed parsing** - Fetch from multiple news sources simultaneously
- 🔍 **Keyword-based filtering** - Filter articles by relevant keywords (finance, AI, technology, etc.)
- 🔄 **Intelligent deduplication** - Remove duplicates based on URL and title similarity
- 📊 **JSON output format** - Structured data storage for further processing
- 🤖 **LLM integration ready** - Optional AI-powered tagging and insight extraction
- 📈 **Statistics and analytics** - Detailed reporting on collected articles
- ⚙️ **Configurable settings** - Easy customization through configuration files
- 🔧 **Error handling** - Robust error handling with retry mechanisms

## Installation

1. **Clone or download the project files**

2. **Install required dependencies:**
```bash
pip install -r requirements.txt
```

3. **Optional: For LLM integration (AI features):**
```bash
pip install openai
export OPENAI_API_KEY="your-api-key-here"
```

## Quick Start

### Basic Usage

```python
from rss_news_parser import RSSNewsParser

# Create parser with default settings
parser = RSSNewsParser()

# Define RSS feeds to parse
feeds = [
    'https://techcrunch.com/feed/',
    'https://feeds.reuters.com/reuters/businessNews',
    'https://feeds.bloomberg.com/markets/news.rss'
]

# Fetch and parse feeds
entries = parser.fetch_multiple_feeds(feeds)

# Save results to JSON
parser.save_to_json(entries, "news_data.json")

print(f"Collected {len(entries)} articles")
```

### Run the Main Script

```bash
python rss_news_parser.py
```

This will:
- Fetch articles from default RSS feeds
- Filter by default keywords
- Remove duplicates
- Save results to `news_feed_data.json`
- Display statistics

## Configuration

### Custom Keywords

```python
# Focus on specific topics
keywords = [
    'artificial intelligence', 'AI', 'machine learning', 
    'finance', 'investment', 'startup', 'automation'
]

parser = RSSNewsParser(keywords=keywords, max_entries_per_feed=25)
```

### Custom RSS Feeds

Edit `config.py` to add your preferred news sources:

```python
RSS_FEEDS = [
    'https://your-favorite-news-site.com/rss',
    'https://another-source.com/feed.xml',
    # Add more feeds here
]
```

### Filtering Options

The parser supports various filtering keywords organized by category:

- **Finance & Business**: finance, CFO, investment, market, revenue, profit
- **Technology & AI**: AI, machine learning, automation, blockchain, cybersecurity  
- **Business Operations**: strategy, operations, supply chain, e-commerce
- **Emerging Topics**: sustainability, ESG, remote work, electric vehicle

## Output Format

The script generates JSON files with the following structure:

```json
{
  "metadata": {
    "total_entries": 45,
    "generated_at": "2024-01-15T10:30:00Z",
    "keywords_used": ["finance", "AI", "technology"],
    "sources": ["TechCrunch", "Reuters", "Bloomberg"]
  },
  "entries": [
    {
      "title": "AI Startup Raises $50M for Financial Risk Management",
      "summary": "Company develops machine learning solutions...",
      "url": "https://example.com/article",
      "publication_date": "2024-01-15T09:00:00Z",
      "source_feed": "TechCrunch",
      "extracted_at": "2024-01-15T10:30:00Z",
      "tags": [],
      "author": "Jane Doe"
    }
  ]
}
```

## Advanced Features

### LLM Integration (AI-Powered Analysis)

Enable AI-powered insights by setting up OpenAI API:

```python
from llm_integration import LLMProcessor

# Initialize LLM processor
llm = LLMProcessor()

# Enhance entries with AI insights
enhanced_entries = llm.enhance_entries(entries, max_entries=10)
```

AI features include:
- **Automatic tagging** - Generate relevant tags for each article
- **Sentiment analysis** - Determine article sentiment (positive/negative/neutral)
- **Topic classification** - Categorize articles by business topics
- **Key insights extraction** - Extract main business implications

### Custom Processing

```python
# Example: Focus on AI and automation news
ai_parser = RSSNewsParser(
    keywords=['AI', 'artificial intelligence', 'automation', 'robot'],
    max_entries_per_feed=20
)

entries = ai_parser.fetch_multiple_feeds([
    'https://techcrunch.com/feed/',
    'https://feeds.feedburner.com/venturebeat/SZYF'
])

# Custom analysis
for entry in entries:
    if 'startup' in entry['title'].lower():
        print(f"Startup news: {entry['title']}")
```

### Statistics and Analytics

```python
# Get detailed statistics
stats = parser.get_statistics(entries)

print(f"Total articles: {stats['total_entries']}")
print(f"Sources: {stats['sources_count']}")
print("Articles per source:")
for source, count in stats['sources_breakdown'].items():
    print(f"  {source}: {count}")
```

## Example Scripts

### 1. Basic Example
```bash
python example_usage.py
```

### 2. Financial News Focus
```python
from rss_news_parser import RSSNewsParser

finance_keywords = ['finance', 'investment', 'market', 'CFO', 'earnings']
parser = RSSNewsParser(keywords=finance_keywords)

feeds = [
    'https://feeds.bloomberg.com/markets/news.rss',
    'https://feeds.reuters.com/reuters/businessNews'
]

entries = parser.fetch_multiple_feeds(feeds)
parser.save_to_json(entries, "financial_news.json")
```

### 3. AI and Technology Focus
```python
ai_keywords = ['AI', 'artificial intelligence', 'machine learning', 'automation']
parser = RSSNewsParser(keywords=ai_keywords)

tech_feeds = [
    'https://techcrunch.com/feed/',
    'https://feeds.feedburner.com/venturebeat/SZYF'
]

entries = parser.fetch_multiple_feeds(tech_feeds)
parser.save_to_json(entries, "ai_tech_news.json")
```

## File Structure

```
rss-news-parser/
├── rss_news_parser.py      # Main parser script
├── config.py               # Configuration settings
├── llm_integration.py      # AI integration module
├── example_usage.py        # Usage examples
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Configuration Options

### Parser Settings (`config.py`)

```python
PARSER_SETTINGS = {
    'max_entries_per_feed': 30,        # Max articles per RSS feed
    'output_filename': 'news_feed_data.json',
    'log_level': 'INFO'                # DEBUG, INFO, WARNING, ERROR
}
```

### LLM Settings

```python
LLM_SETTINGS = {
    'enabled': False,                   # Enable/disable AI features
    'model': 'gpt-3.5-turbo',          # OpenAI model to use
    'api_key_env_var': 'OPENAI_API_KEY',
    'max_tokens': 100,
    'temperature': 0.3
}
```

## Error Handling

The parser includes robust error handling:

- **Network timeouts** - Automatic retries with exponential backoff
- **Invalid feeds** - Graceful handling of malformed RSS feeds
- **Missing data** - Safe extraction of available fields
- **Rate limiting** - Respectful delays between API calls

## Logging

Monitor parser activity with built-in logging:

```bash
2024-01-15 10:30:00 - INFO - Fetching feed: https://techcrunch.com/feed/
2024-01-15 10:30:01 - INFO - Processing feed: TechCrunch
2024-01-15 10:30:02 - INFO - Processed 15 entries from TechCrunch
2024-01-15 10:30:05 - INFO - Total entries collected: 45
2024-01-15 10:30:06 - INFO - Saved 45 entries to news_feed_data.json
```

## Use Cases

### Business Intelligence
- Monitor industry news and trends
- Track competitor mentions
- Identify market opportunities
- Analyze sentiment around topics

### Investment Research  
- Follow financial markets and earnings
- Track startup funding and acquisitions
- Monitor regulatory changes
- Analyze economic indicators

### Technology Monitoring
- Stay updated on AI and automation trends
- Track emerging technologies
- Monitor cybersecurity threats
- Follow digital transformation news

### Content Curation
- Aggregate relevant news for newsletters
- Create topic-specific news feeds
- Filter noise from information overload
- Prepare briefings for executives

## Future Enhancements

- [ ] **Web interface** - Browser-based configuration and viewing
- [ ] **Database storage** - PostgreSQL/MongoDB integration
- [ ] **Real-time updates** - WebSocket-based live feeds
- [ ] **Email notifications** - Automated news digests
- [ ] **More LLM providers** - Anthropic, Google, etc.
- [ ] **Advanced analytics** - Trend analysis and predictions
- [ ] **API endpoints** - RESTful API for integration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions, issues, or feature requests:
1. Check the existing documentation
2. Review example scripts
3. Open an issue with detailed information
4. Include sample RSS feeds and error messages

## Troubleshooting

### Common Issues

**"No entries collected"**
- Check if RSS feeds are accessible
- Verify keywords match article content
- Try with fewer/broader keywords

**"API key not found"**
- Set OPENAI_API_KEY environment variable
- Ensure API key has sufficient credits
- Check API key permissions

**"Feed parsing errors"**
- Some RSS feeds may be temporarily unavailable
- Check feed URLs in a browser
- Try different feeds to isolate issues

**Memory issues with large feeds**
- Reduce `max_entries_per_feed` setting
- Process feeds individually
- Implement pagination for very large datasets
