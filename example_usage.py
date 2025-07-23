#!/usr/bin/env python3
"""
Example usage of the RSS News Parser

This script demonstrates various ways to use the RSS parser with custom configurations.
"""

from rss_news_parser import RSSNewsParser
from config import RSS_FEEDS, FILTER_KEYWORDS, PARSER_SETTINGS
import json


def example_basic_usage():
    """Basic usage example with default settings."""
    print("="*60)
    print("EXAMPLE 1: Basic Usage")
    print("="*60)
    
    # Create parser with default keywords
    parser = RSSNewsParser()
    
    # Fetch from a few feeds
    test_feeds = [
        'https://techcrunch.com/feed/',
        'https://feeds.reuters.com/reuters/businessNews',
    ]
    
    entries = parser.fetch_multiple_feeds(test_feeds)
    
    if entries:
        parser.save_to_json(entries, "basic_example.json")
        print(f"Collected {len(entries)} entries")
        
        # Show first entry as example
        if entries:
            print("\nFirst entry example:")
            print(f"Title: {entries[0]['title']}")
            print(f"Source: {entries[0]['source_feed']}")
            print(f"Date: {entries[0]['publication_date']}")
    else:
        print("No entries collected")


def example_custom_keywords():
    """Example with custom keyword filtering."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Custom Keywords")
    print("="*60)
    
    # Custom keywords focused on AI and automation
    ai_keywords = [
        'artificial intelligence', 'AI', 'machine learning', 'automation',
        'robot', 'chatbot', 'neural network', 'deep learning', 'algorithm'
    ]
    
    parser = RSSNewsParser(keywords=ai_keywords, max_entries_per_feed=20)
    
    # Tech-focused feeds
    tech_feeds = [
        'https://techcrunch.com/feed/',
        'https://feeds.feedburner.com/venturebeat/SZYF',
    ]
    
    entries = parser.fetch_multiple_feeds(tech_feeds)
    
    if entries:
        parser.save_to_json(entries, "ai_focused_news.json")
        print(f"Collected {len(entries)} AI-related entries")
        
        # Show statistics
        stats = parser.get_statistics(entries)
        print(f"Sources: {stats['sources_count']}")
        for source, count in stats['sources_breakdown'].items():
            print(f"  {source}: {count} entries")
    else:
        print("No AI-related entries found")


def example_financial_focus():
    """Example focused on financial news."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Financial Focus")
    print("="*60)
    
    # Financial keywords
    finance_keywords = [
        'finance', 'financial', 'investment', 'market', 'stock', 'trading',
        'economy', 'economic', 'revenue', 'profit', 'earnings', 'CFO', 'CEO',
        'merger', 'acquisition', 'IPO', 'venture capital', 'funding'
    ]
    
    parser = RSSNewsParser(keywords=finance_keywords, max_entries_per_feed=25)
    
    # Financial news feeds
    finance_feeds = [
        'https://feeds.bloomberg.com/markets/news.rss',
        'https://feeds.reuters.com/reuters/businessNews',
        'https://rss.cnn.com/rss/money_news_international.rss',
    ]
    
    entries = parser.fetch_multiple_feeds(finance_feeds)
    
    if entries:
        parser.save_to_json(entries, "financial_news.json")
        print(f"Collected {len(entries)} financial entries")
        
        # Show some titles
        print("\nSample financial headlines:")
        for i, entry in enumerate(entries[:5]):
            print(f"{i+1}. {entry['title']}")
    else:
        print("No financial entries found")


def example_comprehensive_analysis():
    """Comprehensive example using configuration file settings."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Comprehensive Analysis")
    print("="*60)
    
    # Use settings from config file
    parser = RSSNewsParser(
        keywords=FILTER_KEYWORDS,
        max_entries_per_feed=PARSER_SETTINGS['max_entries_per_feed']
    )
    
    # Use all configured feeds
    entries = parser.fetch_multiple_feeds(RSS_FEEDS)
    
    if entries:
        # Save with configured filename
        parser.save_to_json(entries, PARSER_SETTINGS['output_filename'])
        
        # Detailed statistics
        stats = parser.get_statistics(entries)
        print(f"Total entries: {stats['total_entries']}")
        print(f"Number of sources: {stats['sources_count']}")
        
        print("\nDetailed source breakdown:")
        for source, count in sorted(stats['sources_breakdown'].items(), 
                                   key=lambda x: x[1], reverse=True):
            print(f"  {source}: {count} entries")
        
        if stats['date_range']['earliest']:
            print(f"\nDate range: {stats['date_range']['earliest']} to {stats['date_range']['latest']}")
        
        # Analyze keywords in titles
        keyword_mentions = {}
        for entry in entries:
            title_lower = entry['title'].lower()
            for keyword in FILTER_KEYWORDS:
                if keyword.lower() in title_lower:
                    keyword_mentions[keyword] = keyword_mentions.get(keyword, 0) + 1
        
        print("\nTop mentioned keywords:")
        sorted_keywords = sorted(keyword_mentions.items(), key=lambda x: x[1], reverse=True)
        for keyword, count in sorted_keywords[:10]:
            print(f"  {keyword}: {count} mentions")
        
    else:
        print("No entries collected")


def example_custom_processing():
    """Example showing custom processing of collected data."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Custom Data Processing")
    print("="*60)
    
    parser = RSSNewsParser(keywords=['technology', 'AI', 'startup'], max_entries_per_feed=15)
    
    entries = parser.fetch_multiple_feeds([
        'https://techcrunch.com/feed/',
        'https://feeds.reuters.com/reuters/businessNews',
    ])
    
    if entries:
        # Custom processing: categorize by source and create summary
        processed_data = {
            'summary': {
                'total_articles': len(entries),
                'sources': {},
                'recent_articles': [],
                'keyword_analysis': {}
            },
            'articles_by_source': {}
        }
        
        for entry in entries:
            source = entry['source_feed']
            
            # Count by source
            if source not in processed_data['summary']['sources']:
                processed_data['summary']['sources'][source] = 0
                processed_data['articles_by_source'][source] = []
            
            processed_data['summary']['sources'][source] += 1
            processed_data['articles_by_source'][source].append({
                'title': entry['title'],
                'url': entry['url'],
                'date': entry['publication_date'],
                'summary': entry['summary'][:200] + "..." if len(entry['summary']) > 200 else entry['summary']
            })
        
        # Save processed data
        with open('processed_news_data.json', 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)
        
        print(f"Processed {len(entries)} entries into structured format")
        print("Results saved to: processed_news_data.json")
        
        # Show summary
        print("\nProcessing Summary:")
        for source, count in processed_data['summary']['sources'].items():
            print(f"  {source}: {count} articles")
    
    else:
        print("No entries to process")


if __name__ == "__main__":
    print("RSS News Parser - Usage Examples")
    print("This script demonstrates different ways to use the parser.\n")
    
    # Run all examples
    try:
        example_basic_usage()
        example_custom_keywords()
        example_financial_focus()
        example_comprehensive_analysis()
        example_custom_processing()
        
        print("\n" + "="*60)
        print("All examples completed successfully!")
        print("Check the generated JSON files for results.")
        print("="*60)
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure you have installed the required dependencies:")
        print("pip install -r requirements.txt")