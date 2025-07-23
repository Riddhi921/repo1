#!/usr/bin/env python3
"""
RSS News Feed Parser

A comprehensive RSS feed parser that fetches news headlines and summaries,
filters by keywords, removes duplicates, and stores results in JSON format.

Features:
- Multi-source RSS feed support
- Keyword-based filtering
- Duplicate removal (by URL and title)
- JSON output format
- Extensible for LLM integration
"""

import feedparser
import json
import re
from datetime import datetime
from typing import List, Dict, Set, Optional, Union
from urllib.parse import urlparse
import hashlib
import logging
from dateutil import parser as date_parser
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RSSNewsParser:
    """
    A comprehensive RSS news feed parser with filtering and deduplication capabilities.
    """
    
    def __init__(self, keywords: List[str] = None, max_entries_per_feed: int = 50):
        """
        Initialize the RSS parser.
        
        Args:
            keywords: List of keywords to filter entries
            max_entries_per_feed: Maximum number of entries to process per feed
        """
        self.keywords = keywords or [
            'finance', 'financial', 'risk', 'CFO', 'AI', 'artificial intelligence',
            'automation', 'technology', 'business', 'economy', 'investment',
            'market', 'revenue', 'profit', 'earnings', 'startup', 'innovation'
        ]
        self.max_entries_per_feed = max_entries_per_feed
        self.seen_urls: Set[str] = set()
        self.seen_titles: Set[str] = set()
        self.session = self._create_session()
        
    def _create_session(self) -> requests.Session:
        """Create a requests session with retry strategy."""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.headers.update({
            'User-Agent': 'RSS News Parser 1.0 (Python/feedparser)'
        })
        return session
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison by removing extra whitespace and converting to lowercase."""
        if not text:
            return ""
        return re.sub(r'\s+', ' ', text.strip()).lower()
    
    def _extract_clean_text(self, html_text: str) -> str:
        """Extract clean text from HTML content."""
        if not html_text:
            return ""
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', html_text)
        # Decode HTML entities
        clean_text = html_text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        clean_text = clean_text.replace('&quot;', '"').replace('&#39;', "'")
        return clean_text.strip()
    
    def _matches_keywords(self, text: str) -> bool:
        """Check if text contains any of the specified keywords."""
        if not self.keywords:
            return True
        
        normalized_text = self._normalize_text(text)
        return any(keyword.lower() in normalized_text for keyword in self.keywords)
    
    def _is_duplicate(self, entry_data: Dict) -> bool:
        """Check if entry is a duplicate based on URL or title."""
        url = entry_data.get('url', '')
        title = entry_data.get('title', '')
        
        # Check URL duplicates
        if url and url in self.seen_urls:
            return True
        
        # Check title duplicates (normalized)
        normalized_title = self._normalize_text(title)
        title_hash = hashlib.md5(normalized_title.encode()).hexdigest()
        if title_hash in self.seen_titles:
            return True
        
        # Add to seen sets
        if url:
            self.seen_urls.add(url)
        if normalized_title:
            self.seen_titles.add(title_hash)
        
        return False
    
    def _parse_date(self, date_str: str) -> Optional[str]:
        """Parse various date formats and return ISO format string."""
        if not date_str:
            return None
        
        try:
            # Try parsing with dateutil (handles most formats)
            parsed_date = date_parser.parse(date_str)
            return parsed_date.isoformat()
        except (ValueError, TypeError):
            logger.warning(f"Could not parse date: {date_str}")
            return date_str
    
    def _extract_entry_data(self, entry, feed_title: str = "") -> Optional[Dict]:
        """Extract relevant data from a feed entry."""
        try:
            # Extract basic information
            title = self._extract_clean_text(entry.get('title', ''))
            summary = self._extract_clean_text(entry.get('summary', entry.get('description', '')))
            url = entry.get('link', entry.get('id', ''))
            
            # Extract publication date
            pub_date = None
            for date_field in ['published', 'updated', 'created']:
                if hasattr(entry, date_field):
                    pub_date = self._parse_date(getattr(entry, date_field))
                    break
            
            # Create entry data
            entry_data = {
                'title': title,
                'summary': summary,
                'url': url,
                'publication_date': pub_date,
                'source_feed': feed_title,
                'extracted_at': datetime.now().isoformat(),
                'tags': [],  # Placeholder for future LLM tagging
            }
            
            # Add optional fields if available
            if hasattr(entry, 'author'):
                entry_data['author'] = entry.author
            
            if hasattr(entry, 'tags') and entry.tags:
                entry_data['feed_tags'] = [tag.term for tag in entry.tags]
            
            return entry_data
            
        except Exception as e:
            logger.error(f"Error extracting entry data: {e}")
            return None
    
    def fetch_feed(self, feed_url: str) -> List[Dict]:
        """
        Fetch and parse a single RSS feed.
        
        Args:
            feed_url: URL of the RSS feed
            
        Returns:
            List of parsed entries
        """
        logger.info(f"Fetching feed: {feed_url}")
        
        try:
            # Parse the feed
            feed = feedparser.parse(feed_url)
            
            if feed.bozo and hasattr(feed, 'bozo_exception'):
                logger.warning(f"Feed parsing warning for {feed_url}: {feed.bozo_exception}")
            
            feed_title = feed.feed.get('title', urlparse(feed_url).netloc)
            logger.info(f"Processing feed: {feed_title}")
            
            entries = []
            processed_count = 0
            
            for entry in feed.entries[:self.max_entries_per_feed]:
                entry_data = self._extract_entry_data(entry, feed_title)
                
                if not entry_data:
                    continue
                
                # Filter by keywords
                searchable_text = f"{entry_data['title']} {entry_data['summary']}"
                if not self._matches_keywords(searchable_text):
                    continue
                
                # Check for duplicates
                if self._is_duplicate(entry_data):
                    logger.debug(f"Skipping duplicate: {entry_data['title']}")
                    continue
                
                entries.append(entry_data)
                processed_count += 1
            
            logger.info(f"Processed {processed_count} entries from {feed_title}")
            return entries
            
        except Exception as e:
            logger.error(f"Error fetching feed {feed_url}: {e}")
            return []
    
    def fetch_multiple_feeds(self, feed_urls: List[str]) -> List[Dict]:
        """
        Fetch and parse multiple RSS feeds.
        
        Args:
            feed_urls: List of RSS feed URLs
            
        Returns:
            Combined list of parsed entries from all feeds
        """
        all_entries = []
        
        for feed_url in feed_urls:
            entries = self.fetch_feed(feed_url)
            all_entries.extend(entries)
        
        logger.info(f"Total entries collected: {len(all_entries)}")
        return all_entries
    
    def save_to_json(self, entries: List[Dict], filename: str = "news_feed_data.json") -> None:
        """
        Save entries to a JSON file.
        
        Args:
            entries: List of entry dictionaries
            filename: Output filename
        """
        try:
            # Sort entries by publication date (newest first)
            sorted_entries = sorted(
                entries,
                key=lambda x: x.get('publication_date', ''),
                reverse=True
            )
            
            output_data = {
                'metadata': {
                    'total_entries': len(sorted_entries),
                    'generated_at': datetime.now().isoformat(),
                    'keywords_used': self.keywords,
                    'sources': list(set(entry.get('source_feed', '') for entry in sorted_entries))
                },
                'entries': sorted_entries
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(sorted_entries)} entries to {filename}")
            
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")
    
    def get_statistics(self, entries: List[Dict]) -> Dict:
        """Get statistics about the collected entries."""
        if not entries:
            return {}
        
        sources = {}
        dates = []
        
        for entry in entries:
            source = entry.get('source_feed', 'Unknown')
            sources[source] = sources.get(source, 0) + 1
            
            if entry.get('publication_date'):
                dates.append(entry['publication_date'])
        
        return {
            'total_entries': len(entries),
            'sources_count': len(sources),
            'sources_breakdown': sources,
            'date_range': {
                'earliest': min(dates) if dates else None,
                'latest': max(dates) if dates else None
            }
        }


def main():
    """Main function to demonstrate the RSS parser."""
    
    # Default RSS feeds (you can modify these)
    default_feeds = [
        'https://feeds.bloomberg.com/markets/news.rss',
        'https://feeds.reuters.com/reuters/businessNews',
        'https://rss.cnn.com/rss/money_news_international.rss',
        'https://feeds.feedburner.com/venturebeat/SZYF',  # VentureBeat AI
        'https://techcrunch.com/feed/',
        'https://www.wsj.com/xml/rss/3_7085.xml',  # WSJ Technology
    ]
    
    # Keywords for filtering
    keywords = [
        'finance', 'financial', 'risk', 'CFO', 'AI', 'artificial intelligence',
        'automation', 'technology', 'business', 'economy', 'investment',
        'market', 'revenue', 'profit', 'earnings', 'startup', 'innovation',
        'digital transformation', 'fintech', 'blockchain', 'cryptocurrency'
    ]
    
    # Initialize parser
    parser = RSSNewsParser(keywords=keywords, max_entries_per_feed=30)
    
    # Fetch feeds
    logger.info("Starting RSS feed parsing...")
    entries = parser.fetch_multiple_feeds(default_feeds)
    
    # Save results
    if entries:
        parser.save_to_json(entries, "news_feed_data.json")
        
        # Print statistics
        stats = parser.get_statistics(entries)
        print("\n" + "="*50)
        print("RSS FEED PARSING RESULTS")
        print("="*50)
        print(f"Total entries collected: {stats['total_entries']}")
        print(f"Number of sources: {stats['sources_count']}")
        print("\nEntries per source:")
        for source, count in stats['sources_breakdown'].items():
            print(f"  {source}: {count}")
        
        if stats['date_range']['earliest']:
            print(f"\nDate range: {stats['date_range']['earliest']} to {stats['date_range']['latest']}")
        
        print(f"\nResults saved to: news_feed_data.json")
    else:
        print("No entries were collected.")


if __name__ == "__main__":
    main()