#!/usr/bin/env python3
"""
RSS News Parser - Demonstration Script

This script demonstrates the main features of the RSS news parser:
- Basic RSS feed parsing
- Keyword filtering
- Duplicate removal
- JSON output
- Statistics and analytics
"""

from rss_news_parser import RSSNewsParser
import json

def main():
    print("🔍 RSS News Parser - Live Demonstration")
    print("=" * 50)
    
    # Demo 1: Quick parsing with default settings
    print("\n📰 Demo 1: Quick News Parsing")
    print("-" * 30)
    
    parser = RSSNewsParser(
        keywords=['AI', 'technology', 'startup', 'business'],
        max_entries_per_feed=10
    )
    
    # Use reliable feeds for demo
    demo_feeds = [
        'https://techcrunch.com/feed/',
        'https://feeds.feedburner.com/venturebeat/SZYF',
    ]
    
    print("Fetching from demo RSS feeds...")
    entries = parser.fetch_multiple_feeds(demo_feeds)
    
    if entries:
        print(f"✅ Successfully collected {len(entries)} articles")
        
        # Show sample headlines
        print("\n📄 Sample Headlines:")
        for i, entry in enumerate(entries[:5]):
            print(f"{i+1}. {entry['title']}")
            print(f"   Source: {entry['source_feed']}")
            print(f"   Date: {entry['publication_date']}")
            print()
        
        # Generate statistics
        stats = parser.get_statistics(entries)
        print("📊 Collection Statistics:")
        print(f"   Total articles: {stats['total_entries']}")
        print(f"   Number of sources: {stats['sources_count']}")
        print("   Articles per source:")
        for source, count in stats['sources_breakdown'].items():
            print(f"     • {source}: {count}")
        
        # Save to JSON
        parser.save_to_json(entries, "demo_results.json")
        print(f"\n💾 Results saved to: demo_results.json")
        
        # Show JSON structure
        with open("demo_results.json", 'r') as f:
            data = json.load(f)
        
        print("\n🔧 JSON Structure Preview:")
        print(f"   Metadata keys: {list(data['metadata'].keys())}")
        print(f"   First entry keys: {list(data['entries'][0].keys())}")
        
        # Demonstrate filtering
        print("\n🎯 Keyword Filtering Demo:")
        ai_count = sum(1 for entry in entries if 'AI' in entry['title'] or 'AI' in entry['summary'])
        tech_count = sum(1 for entry in entries if 'technology' in entry['title'].lower() or 'technology' in entry['summary'].lower())
        print(f"   Articles mentioning 'AI': {ai_count}")
        print(f"   Articles mentioning 'technology': {tech_count}")
        
    else:
        print("❌ No articles collected. Check internet connection or feed URLs.")
    
    # Demo 2: Show configuration options
    print("\n⚙️  Demo 2: Configuration Options")
    print("-" * 30)
    print("Available customization options:")
    print("   • Custom keyword lists")
    print("   • Maximum entries per feed")
    print("   • Multiple RSS feed sources")
    print("   • JSON output formatting")
    print("   • Duplicate detection and removal")
    print("   • Date parsing and sorting")
    
    # Demo 3: Show file structure
    print("\n📁 Demo 3: Generated Files")
    print("-" * 30)
    import os
    json_files = [f for f in os.listdir('.') if f.endswith('.json')]
    print("Generated JSON files:")
    for file in json_files:
        size = os.path.getsize(file)
        print(f"   • {file} ({size:,} bytes)")
    
    print("\n🚀 Next Steps:")
    print("   1. Customize RSS feeds in config.py")
    print("   2. Modify keywords for your use case")
    print("   3. Set up LLM integration (optional)")
    print("   4. Schedule regular runs with cron")
    print("   5. Integrate with your data pipeline")
    
    print("\n📚 For more examples, run:")
    print("   python3 example_usage.py")
    
    print("\n✨ RSS News Parser Demo Complete!")


if __name__ == "__main__":
    main()