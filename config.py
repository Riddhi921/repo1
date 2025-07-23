"""
Configuration file for RSS News Parser

This file contains default RSS feeds and keywords that can be easily modified
without changing the main script.
"""

# Default RSS feeds to parse
RSS_FEEDS = [
    # Financial News
    'https://feeds.bloomberg.com/markets/news.rss',
    'https://feeds.reuters.com/reuters/businessNews',
    'https://rss.cnn.com/rss/money_news_international.rss',
    'https://feeds.feedburner.com/wsj/xml/rss/3_7014',  # WSJ Markets
    
    # Technology News
    'https://techcrunch.com/feed/',
    'https://feeds.feedburner.com/venturebeat/SZYF',  # VentureBeat AI
    'https://feeds.arstechnica.com/arstechnica/technology-lab',
    'https://www.wired.com/feed/rss',
    
    # Business News
    'https://feeds.harvard.edu/news/rss/business.rss',
    'https://feeds.feedburner.com/entrepreneur/latest',
    
    # AI and Automation
    'https://feeds.feedburner.com/oreilly/radar/atom',
    'https://machinelearningmastery.com/feed/',
]

# Keywords for filtering articles
FILTER_KEYWORDS = [
    # Finance & Business
    'finance', 'financial', 'risk', 'CFO', 'CEO', 'investment', 'investor',
    'market', 'revenue', 'profit', 'earnings', 'startup', 'venture capital',
    'IPO', 'merger', 'acquisition', 'valuation', 'funding', 'fintech',
    
    # Technology & AI
    'AI', 'artificial intelligence', 'machine learning', 'automation',
    'technology', 'innovation', 'digital transformation', 'blockchain',
    'cryptocurrency', 'cloud computing', 'data analytics', 'cybersecurity',
    
    # Business Operations
    'business', 'economy', 'strategy', 'operations', 'efficiency',
    'productivity', 'supply chain', 'logistics', 'manufacturing',
    'retail', 'e-commerce', 'digital marketing', 'customer experience',
    
    # Emerging Topics
    'sustainability', 'ESG', 'climate', 'renewable energy', 'electric vehicle',
    'remote work', 'hybrid work', 'workforce', 'talent', 'skills'
]

# Parser settings
PARSER_SETTINGS = {
    'max_entries_per_feed': 30,
    'output_filename': 'news_feed_data.json',
    'log_level': 'INFO',  # DEBUG, INFO, WARNING, ERROR
}

# LLM Integration Settings (for future use)
LLM_SETTINGS = {
    'enabled': False,
    'model': 'gpt-3.5-turbo',  # or any other model
    'api_key_env_var': 'OPENAI_API_KEY',
    'tagging_prompt': """
    Analyze the following news article and provide relevant tags:
    
    Title: {title}
    Summary: {summary}
    
    Please provide 3-5 relevant tags that categorize this article.
    Focus on: industry, topic, sentiment, urgency, and impact level.
    
    Tags:
    """,
    'max_tokens': 100,
    'temperature': 0.3,
}