#!/usr/bin/env python3
"""
LLM Integration Module for RSS News Parser

This module provides integration with Large Language Models for:
- Automatic tagging of news articles
- Sentiment analysis
- Content summarization
- Insight extraction
- Topic classification

Currently supports OpenAI GPT models, but can be extended for other providers.
"""

import os
import json
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime
import time

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI library not installed. LLM features will be disabled.")

from config import LLM_SETTINGS

logger = logging.getLogger(__name__)


class LLMProcessor:
    """
    LLM processor for enhancing RSS feed entries with AI-generated insights.
    """
    
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize the LLM processor.
        
        Args:
            api_key: OpenAI API key (if None, will try to get from environment)
            model: Model to use (defaults to config setting)
        """
        self.model = model or LLM_SETTINGS['model']
        self.enabled = LLM_SETTINGS['enabled'] and OPENAI_AVAILABLE
        
        if not self.enabled:
            logger.info("LLM processing is disabled")
            return
        
        # Set up API key
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv(LLM_SETTINGS['api_key_env_var'])
        
        if not self.api_key:
            logger.error(f"No API key found. Set {LLM_SETTINGS['api_key_env_var']} environment variable")
            self.enabled = False
            return
        
        # Initialize OpenAI client
        try:
            openai.api_key = self.api_key
            self.client = openai
            logger.info(f"LLM processor initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            self.enabled = False
    
    def _make_api_call(self, prompt: str, max_tokens: int = None, temperature: float = None) -> Optional[str]:
        """Make an API call to the LLM with error handling and retries."""
        if not self.enabled:
            return None
        
        max_tokens = max_tokens or LLM_SETTINGS['max_tokens']
        temperature = temperature or LLM_SETTINGS['temperature']
        
        try:
            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes news articles."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=30
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"LLM API call failed: {e}")
            return None
    
    def generate_tags(self, title: str, summary: str) -> List[str]:
        """
        Generate relevant tags for an article using LLM.
        
        Args:
            title: Article title
            summary: Article summary
            
        Returns:
            List of generated tags
        """
        if not self.enabled:
            return []
        
        prompt = LLM_SETTINGS['tagging_prompt'].format(
            title=title[:200],  # Limit length
            summary=summary[:500]  # Limit length
        )
        
        response = self._make_api_call(prompt)
        
        if response:
            # Parse tags from response
            tags = []
            for line in response.split('\n'):
                line = line.strip()
                if line and not line.startswith('Tags:'):
                    # Remove bullet points, numbers, etc.
                    tag = line.lstrip('- •*1234567890. ').strip()
                    if tag and len(tag) > 2:
                        tags.append(tag)
            
            return tags[:5]  # Limit to 5 tags
        
        return []
    
    def analyze_sentiment(self, title: str, summary: str) -> Dict[str, Any]:
        """
        Analyze sentiment of an article.
        
        Args:
            title: Article title
            summary: Article summary
            
        Returns:
            Dictionary with sentiment analysis results
        """
        if not self.enabled:
            return {'sentiment': 'neutral', 'confidence': 0.0}
        
        prompt = f"""
        Analyze the sentiment of this news article:
        
        Title: {title[:200]}
        Summary: {summary[:500]}
        
        Provide the sentiment (positive, negative, or neutral) and confidence score (0-1).
        Format: Sentiment: [sentiment], Confidence: [score]
        """
        
        response = self._make_api_call(prompt, max_tokens=50)
        
        if response:
            try:
                # Parse response
                sentiment = 'neutral'
                confidence = 0.0
                
                if 'positive' in response.lower():
                    sentiment = 'positive'
                elif 'negative' in response.lower():
                    sentiment = 'negative'
                
                # Extract confidence score
                import re
                confidence_match = re.search(r'confidence:\s*([\d.]+)', response.lower())
                if confidence_match:
                    confidence = float(confidence_match.group(1))
                
                return {
                    'sentiment': sentiment,
                    'confidence': confidence,
                    'raw_response': response
                }
            except Exception as e:
                logger.error(f"Error parsing sentiment response: {e}")
        
        return {'sentiment': 'neutral', 'confidence': 0.0}
    
    def extract_key_insights(self, title: str, summary: str) -> List[str]:
        """
        Extract key insights from an article.
        
        Args:
            title: Article title
            summary: Article summary
            
        Returns:
            List of key insights
        """
        if not self.enabled:
            return []
        
        prompt = f"""
        Extract 2-3 key business insights from this news article:
        
        Title: {title[:200]}
        Summary: {summary[:500]}
        
        Focus on:
        - Market implications
        - Business impact
        - Strategic significance
        - Financial implications
        
        Provide concise bullet points.
        """
        
        response = self._make_api_call(prompt, max_tokens=150)
        
        if response:
            insights = []
            for line in response.split('\n'):
                line = line.strip()
                if line and len(line) > 10:
                    insight = line.lstrip('- •*1234567890. ').strip()
                    if insight:
                        insights.append(insight)
            
            return insights[:3]  # Limit to 3 insights
        
        return []
    
    def classify_topic(self, title: str, summary: str) -> Dict[str, Any]:
        """
        Classify the main topic/category of an article.
        
        Args:
            title: Article title
            summary: Article summary
            
        Returns:
            Dictionary with topic classification
        """
        if not self.enabled:
            return {'primary_topic': 'general', 'secondary_topics': []}
        
        prompt = f"""
        Classify this news article into relevant business categories:
        
        Title: {title[:200]}
        Summary: {summary[:500]}
        
        Choose from these categories:
        - Technology/AI
        - Finance/Investment
        - Market Analysis
        - Corporate News
        - Startup/Innovation
        - Economic Policy
        - Industry Analysis
        - Risk Management
        - Digital Transformation
        - Sustainability/ESG
        
        Provide primary category and 1-2 secondary categories.
        Format: Primary: [category], Secondary: [category1, category2]
        """
        
        response = self._make_api_call(prompt, max_tokens=100)
        
        if response:
            try:
                primary_topic = 'general'
                secondary_topics = []
                
                # Parse primary topic
                import re
                primary_match = re.search(r'primary:\s*([^,\n]+)', response.lower())
                if primary_match:
                    primary_topic = primary_match.group(1).strip()
                
                # Parse secondary topics
                secondary_match = re.search(r'secondary:\s*([^\n]+)', response.lower())
                if secondary_match:
                    secondary_text = secondary_match.group(1)
                    secondary_topics = [topic.strip() for topic in secondary_text.split(',')]
                
                return {
                    'primary_topic': primary_topic,
                    'secondary_topics': secondary_topics[:2],
                    'raw_response': response
                }
            except Exception as e:
                logger.error(f"Error parsing topic classification: {e}")
        
        return {'primary_topic': 'general', 'secondary_topics': []}
    
    def enhance_entry(self, entry: Dict) -> Dict:
        """
        Enhance a single RSS entry with LLM-generated insights.
        
        Args:
            entry: RSS entry dictionary
            
        Returns:
            Enhanced entry with LLM insights
        """
        if not self.enabled:
            return entry
        
        title = entry.get('title', '')
        summary = entry.get('summary', '')
        
        if not title and not summary:
            return entry
        
        logger.info(f"Enhancing entry: {title[:50]}...")
        
        # Add LLM enhancements
        enhanced_entry = entry.copy()
        
        # Generate tags
        enhanced_entry['llm_tags'] = self.generate_tags(title, summary)
        
        # Analyze sentiment
        enhanced_entry['sentiment_analysis'] = self.analyze_sentiment(title, summary)
        
        # Extract insights
        enhanced_entry['key_insights'] = self.extract_key_insights(title, summary)
        
        # Classify topic
        enhanced_entry['topic_classification'] = self.classify_topic(title, summary)
        
        # Add processing metadata
        enhanced_entry['llm_processed_at'] = datetime.now().isoformat()
        enhanced_entry['llm_model_used'] = self.model
        
        # Add small delay to respect API rate limits
        time.sleep(0.1)
        
        return enhanced_entry
    
    def enhance_entries(self, entries: List[Dict], max_entries: int = None) -> List[Dict]:
        """
        Enhance multiple RSS entries with LLM insights.
        
        Args:
            entries: List of RSS entries
            max_entries: Maximum number of entries to process (for cost control)
            
        Returns:
            List of enhanced entries
        """
        if not self.enabled:
            logger.info("LLM processing disabled, returning original entries")
            return entries
        
        if max_entries:
            entries = entries[:max_entries]
        
        logger.info(f"Enhancing {len(entries)} entries with LLM insights...")
        
        enhanced_entries = []
        for i, entry in enumerate(entries):
            try:
                enhanced_entry = self.enhance_entry(entry)
                enhanced_entries.append(enhanced_entry)
                
                if (i + 1) % 5 == 0:
                    logger.info(f"Processed {i + 1}/{len(entries)} entries")
                    
            except Exception as e:
                logger.error(f"Error enhancing entry {i}: {e}")
                enhanced_entries.append(entry)  # Add original entry
        
        logger.info(f"LLM enhancement completed for {len(enhanced_entries)} entries")
        return enhanced_entries


def demo_llm_integration():
    """Demonstrate LLM integration capabilities."""
    print("="*60)
    print("LLM INTEGRATION DEMO")
    print("="*60)
    
    if not OPENAI_AVAILABLE:
        print("OpenAI library not available. Install with: pip install openai")
        return
    
    # Sample article for testing
    sample_entry = {
        'title': 'AI Startup Raises $50M Series B to Transform Financial Risk Management',
        'summary': 'TechFinance AI, a startup specializing in artificial intelligence solutions for financial risk assessment, announced today that it has closed a $50 million Series B funding round. The company plans to use the funding to expand its machine learning platform that helps banks and financial institutions better predict and manage credit risks through advanced data analytics.',
        'url': 'https://example.com/ai-startup-funding',
        'publication_date': '2024-01-15T10:00:00Z',
        'source_feed': 'TechCrunch'
    }
    
    # Initialize LLM processor
    processor = LLMProcessor()
    
    if not processor.enabled:
        print("LLM processor not enabled. Check API key and configuration.")
        return
    
    print("Processing sample article...")
    print(f"Title: {sample_entry['title']}")
    print(f"Summary: {sample_entry['summary'][:100]}...\n")
    
    # Enhance the entry
    enhanced_entry = processor.enhance_entry(sample_entry)
    
    # Display results
    print("LLM ENHANCEMENT RESULTS:")
    print("-" * 40)
    
    if 'llm_tags' in enhanced_entry:
        print(f"Generated Tags: {', '.join(enhanced_entry['llm_tags'])}")
    
    if 'sentiment_analysis' in enhanced_entry:
        sentiment = enhanced_entry['sentiment_analysis']
        print(f"Sentiment: {sentiment.get('sentiment', 'N/A')} (confidence: {sentiment.get('confidence', 0):.2f})")
    
    if 'topic_classification' in enhanced_entry:
        topic = enhanced_entry['topic_classification']
        print(f"Primary Topic: {topic.get('primary_topic', 'N/A')}")
        if topic.get('secondary_topics'):
            print(f"Secondary Topics: {', '.join(topic['secondary_topics'])}")
    
    if 'key_insights' in enhanced_entry:
        print("Key Insights:")
        for insight in enhanced_entry['key_insights']:
            print(f"  • {insight}")
    
    print(f"\nProcessed at: {enhanced_entry.get('llm_processed_at', 'N/A')}")
    print(f"Model used: {enhanced_entry.get('llm_model_used', 'N/A')}")


if __name__ == "__main__":
    demo_llm_integration()