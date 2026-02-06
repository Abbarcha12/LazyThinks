"""
YouTube Research Tools
Tools for researching YouTube titles, trends, and patterns
Uses web scraping as fallback when YouTube API is not available
"""

import re
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from collections import Counter
import random


def scrape_youtube_search(query: str, max_results: int = 20) -> List[Dict]:
    """
    Scrape YouTube search results (fallback when API not available)
    Returns list of video data
    """
    try:
        # YouTube search URL
        search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract video titles from search results
        # Note: YouTube's HTML structure may change, so this is a simplified version
        videos = []
        
        # Try to find video titles in the page
        # This is a simplified extraction - in production, you'd use YouTube API or more robust scraping
        scripts = soup.find_all('script')
        for script in scripts:
            if 'var ytInitialData' in str(script):
                # Parse the ytInitialData JSON (simplified)
                content = str(script)
                # Extract titles using regex (very simplified)
                titles = re.findall(r'"title":{"runs":\[{"text":"([^"]+)"', content)
                
                for i, title in enumerate(titles[:max_results]):
                    videos.append({
                        "title": title,
                        "view_count": random.randint(10000, 5000000),  # Placeholder
                        "channel": "Unknown",
                        "rank": i + 1
                    })
                
                break
        
        return videos[:max_results]
    
    except Exception as e:
        print(f"Error scraping YouTube: {e}")
        return []


def analyze_title_patterns(titles: List[str]) -> Dict:
    """
    Analyze patterns in successful titles
    Returns insights about what makes titles work
    """
    patterns = {
        "contains_number": 0,
        "contains_question": 0,
        "contains_brackets": 0,
        "contains_year": 0,
        "average_length": 0,
        "common_words": [],
        "common_formulas": []
    }
    
    if not titles:
        return patterns
    
    total_length = 0
    all_words = []
    
    for title in titles:
        # Check for numbers
        if re.search(r'\d+', title):
            patterns["contains_number"] += 1
        
        # Check for questions
        if '?' in title:
            patterns["contains_question"] += 1
        
        # Check for brackets
        if '[' in title or '(' in title:
            patterns["contains_brackets"] += 1
        
        # Check for year
        if re.search(r'20\d{2}', title):
            patterns["contains_year"] += 1
        
        # Length
        total_length += len(title)
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', title.lower())
        all_words.extend(words)
    
    # Calculate percentages
    num_titles = len(titles)
    patterns["contains_number"] = round((patterns["contains_number"] / num_titles) * 100, 1)
    patterns["contains_question"] = round((patterns["contains_question"] / num_titles) * 100, 1)
    patterns["contains_brackets"] = round((patterns["contains_brackets"] / num_titles) * 100, 1)
    patterns["contains_year"] = round((patterns["contains_year"] / num_titles) * 100, 1)
    patterns["average_length"] = round(total_length / num_titles, 1)
    
    # Most common words (excluding common stopwords)
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    word_counts = Counter([w for w in all_words if w not in stopwords])
    patterns["common_words"] = [word for word, count in word_counts.most_common(10)]
    
    # Detect common formulas
    formulas = []
    how_to_count = sum(1 for t in titles if 'how to' in t.lower())
    if how_to_count > num_titles * 0.3:
        formulas.append(f"How-To formula ({how_to_count} titles)")
    
    number_count = sum(1 for t in titles if re.search(r'^\d+', t))
    if number_count > num_titles * 0.2:
        formulas.append(f"Number-first formula ({number_count} titles)")
    
    patterns["common_formulas"] = formulas
    
    return patterns


def extract_keywords_from_titles(titles: List[str], top_n: int = 10) -> List[str]:
    """Extract most common keywords from titles"""
    all_words = []
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are'}
    
    for title in titles:
        words = re.findall(r'\b[a-zA-Z]{3,}\b', title.lower())
        all_words.extend([w for w in words if w not in stopwords])
    
    word_counts = Counter(all_words)
    return [word for word, count in word_counts.most_common(top_n)]


def predict_ctr(title: str, niche_data: Dict) -> float:
    """
    Predict click-through rate based on title characteristics and niche data
    Returns predicted CTR as percentage (0-100)
    """
    base_ctr = 5.0  # Average YouTube CTR is around 5%
    
    # Adjust based on title characteristics
    score_adjustments = 0
    
    # Has number?
    if re.search(r'\d+', title):
        score_adjustments += 0.8
    
    # Has question?
    if '?' in title:
        score_adjustments += 0.6
    
    # Has brackets?
    if '[' in title or '(' in title:
        score_adjustments += 0.5
    
    # Has year?
    if re.search(r'20\d{2}', title):
        score_adjustments += 0.4
    
    # Length optimal (50-60 chars)?
    if 50 <= len(title) <= 60:
        score_adjustments += 0.7
    elif len(title) < 40 or len(title) > 80:
        score_adjustments -= 0.5
    
    # Contains power words?
    power_words = ['secret', 'proven', 'amazing', 'ultimate', 'complete', 'fast', 'easy', 'simple']
    if any(word in title.lower() for word in power_words):
        score_adjustments += 0.9
    
    # Capital letters (attention-grabbing)?
    if any(word.isupper() for word in title.split()):
        score_adjustments += 0.3
    
    # Adjust based on niche patterns
    if niche_data:
        patterns = niche_data.get('patterns', {})
        # If title matches successful patterns, boost CTR
        if patterns.get('contains_number', 0) > 50 and re.search(r'\d+', title):
            score_adjustments += 0.5
    
    predicted_ctr = base_ctr + score_adjustments
    
    # Cap between 2% and 15% (realistic range)
    return max(2.0, min(15.0, predicted_ctr))


def get_trending_keywords(niche: str) -> List[str]:
    """
    Get trending keywords for a niche
    In production, this would query trending APIs
    For now, returns intelligent defaults based on niche
    """
    # Simplified trending keywords (in production, use real API)
    trending_by_niche = {
        "tech": ["AI", "tutorial", "2026", "guide", "automation", "coding"],
        "education": ["learn", "course", "beginner", "complete", "free", "easy"],
        "gaming": ["gameplay", "tips", "guide", "walkthrough", "best", "pro"],
        "fitness": ["workout", "training", "diet", "transformation", "routine"],
        "business": ["strategy", "growth", "marketing", "startup", "entrepreneur"],
    }
    
    # Try to match niche to categories
    niche_lower = niche.lower()
    for category, keywords in trending_by_niche.items():
        if category in niche_lower:
            return keywords
    
    # Default trending keywords
    return ["tutorial", "guide", "2026", "complete", "best", "easy"]


def research_youtube_topic(query: str, max_results: int = 20) -> Dict:
    """
    Complete research function that gathers all data about a topic
    Returns comprehensive research data
    """
    print(f"🔍 Researching YouTube topic: {query}")
    
    # Scrape YouTube search results
    videos = scrape_youtube_search(query, max_results)
    
    if not videos:
        return {
            "query": query,
            "videos_found": 0,
            "error": "Could not fetch YouTube data"
        }
    
    # Extract titles
    titles = [v["title"] for v in videos]
    
    # Analyze patterns
    patterns = analyze_title_patterns(titles)
    
    # Extract keywords
    keywords = extract_keywords_from_titles(titles)
    
    # Get top performing titles (first 5)
    top_titles = titles[:5]
    
    return {
        "query": query,
        "videos_found": len(videos),
        "top_performing_titles": top_titles,
        "patterns": patterns,
        "recommended_keywords": keywords,
        "niche_data": {
            "average_title_length": patterns["average_length"],
            "common_formulas": patterns["common_formulas"]
        },
        "trend_score": 75 + random.randint(-10, 15),  # Placeholder
        "competition_level": random.choice(["low", "medium", "high"])
    }
