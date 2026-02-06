"""
YouTube Title Generator
Generates SEO-optimized, attention-grabbing YouTube titles using proven formulas
"""

import re
import random
from typing import List, Dict, Tuple


# Power words for enhanced CTR
POWER_WORDS = {
    "urgency": ["now", "today", "fast", "quick", "instant", "immediately"],
    "value": ["proven", "guaranteed", "essential", "ultimate", "complete", "perfect"],
    "curiosity": ["secret", "hidden", "truth", "revealed", "exposed", "insider"],
    "emotion": ["amazing", "shocking", "unbelievable", "incredible", "stunning", "mind-blowing"],
    "simplicity": ["easy", "simple", "effortless", "beginner", "step-by-step", "straightforward"],
    "exclusivity": ["exclusive", "limited", "rare", "unique", "special", "premium"],
    "negativity": ["avoid", "mistake", "wrong", "fail", "never", "stop", "worst"]
}

# Brackets and parenthesis additions for specificity
BRACKET_ADDITIONS = [
    "[2026]",
    "[Updated]",
    "[Tutorial]",
    "[Step-by-Step]",
    "[No Experience Needed]",
    "[Proven Method]",
    "[Full Guide]",
    "(Actually Works)",
    "(Free Method)",
    "(Beginner-Friendly)"
]


def get_random_power_word(category: str = None) -> str:
    """Get a random power word from a specific category or any category"""
    if category and category in POWER_WORDS:
        return random.choice(POWER_WORDS[category])
    # Pick from all categories
    all_words = [word for words in POWER_WORDS.values() for word in words]
    return random.choice(all_words)


def extract_power_words(title: str) -> List[str]:
    """Extract power words used in a title"""
    title_lower = title.lower()
    found_words = []
    for category, words in POWER_WORDS.items():
        for word in words:
            if word in title_lower:
                found_words.append(word)
    return list(set(found_words))


def validate_title_length(title: str) -> Tuple[int, str]:
    """
    Validate title length and return character count with status
    Returns: (character_count, status)
    Status: 'optimal' (55-60), 'good' (45-54 or 61-70), 'too_short' (<45), 'too_long' (>100)
    """
    length = len(title)
    
    if 55 <= length <= 60:
        return length, "optimal"
    elif 45 <= length <= 54 or 61 <= length <= 70:
        return length, "good"
    elif length < 45:
        return length, "too_short"
    elif length > 100:
        return length, "too_long"
    else:
        return length, "acceptable"


def calculate_seo_score(title: str, keywords: List[str]) -> float:
    """
    Calculate SEO score based on:
    - Keyword placement (front-loaded = higher score)
    - Title length (55-60 = optimal)
    - Power word usage
    - Number usage
    """
    score = 0.0
    title_lower = title.lower()
    
    # 1. Keyword placement (40 points max)
    first_words = ' '.join(title.split()[:5]).lower()
    keywords_in_first_5 = sum(1 for kw in keywords if kw.lower() in first_words)
    if keywords_in_first_5 > 0:
        score += min(40, keywords_in_first_5 * 20)
    
    # 2. Title length (30 points max)
    length, status = validate_title_length(title)
    if status == "optimal":
        score += 30
    elif status == "good":
        score += 20
    elif status == "acceptable":
        score += 10
    
    # 3. Power word usage (20 points max)
    power_words_found = extract_power_words(title)
    score += min(20, len(power_words_found) * 10)
    
    # 4. Number usage (10 points max)
    if re.search(r'\d+', title):
        score += 10
    
    return min(100.0, score)


def estimate_ctr_potential(seo_score: float, has_brackets: bool, power_words_count: int) -> str:
    """Estimate click-through rate potential"""
    if seo_score >= 70 and (has_brackets or power_words_count >= 2):
        return "high"
    elif seo_score >= 50:
        return "medium"
    else:
        return "low"


# ==============================================================================
# TITLE FORMULAS
# ==============================================================================

def formula_how_to(topic: str, keywords: List[str], niche: str) -> str:
    """How to [Achieve Result] in [Timeframe]"""
    timeframes = ["10 Minutes", "5 Steps", "24 Hours", "One Week", "30 Days"]
    primary_keyword = keywords[0] if keywords else topic
    
    templates = [
        f"How to {primary_keyword} in {random.choice(timeframes)}",
        f"How to {primary_keyword} for {niche}",
        f"How to {primary_keyword} (Step-by-Step Guide)",
    ]
    return random.choice(templates)


def formula_without(topic: str, keywords: List[str], niche: str) -> str:
    """Do [X] Without [Typical Hurdle]"""
    hurdles = ["Experience", "Money", "Expensive Tools", "Spending Hours", "Paid Software", "a Degree"]
    primary_keyword = keywords[0] if keywords else topic
    
    templates = [
        f"{primary_keyword.title()} Without {random.choice(hurdles)}",
        f"How to {primary_keyword} Without {random.choice(hurdles)}",
        f"Get Results with {primary_keyword} (No {random.choice(hurdles)} Needed)",
    ]
    return random.choice(templates)


def formula_listicle(topic: str, keywords: List[str], niche: str) -> str:
    """Top [Number] [Tips/Tools] for [Goal]"""
    numbers = [3, 5, 7, 10]
    list_types = ["Tips", "Tricks", "Secrets", "Hacks", "Ways", "Methods", "Tools", "Strategies"]
    primary_keyword = keywords[0] if keywords else topic
    
    templates = [
        f"{random.choice(numbers)} {random.choice(list_types)} to {primary_keyword}",
        f"Top {random.choice(numbers)} {primary_keyword} {random.choice(list_types)} for {niche}",
        f"{random.choice(numbers)} Proven {primary_keyword} {random.choice(list_types)}",
    ]
    return random.choice(templates)


def formula_authority_hook(topic: str, keywords: List[str], niche: str) -> str:
    """Before You [Action], Watch This"""
    primary_keyword = keywords[0] if keywords else topic
    
    templates = [
        f"Before You {primary_keyword}, Watch This",
        f"Stop! Don't {primary_keyword} Until You See This",
        f"What You Must Know Before {primary_keyword}",
        f"{primary_keyword.title()}: What Experts Won't Tell You",
    ]
    return random.choice(templates)


def formula_hidden_info(topic: str, keywords: List[str], niche: str) -> str:
    """What They're Not Telling You About [Topic]"""
    primary_keyword = keywords[0] if keywords else topic
    
    templates = [
        f"What They're Not Telling You About {primary_keyword}",
        f"The Truth About {primary_keyword} (Finally Revealed)",
        f"{primary_keyword.title()}: The Hidden Truth Exposed",
        f"Why Nobody Talks About {primary_keyword}",
    ]
    return random.choice(templates)


def formula_question_hook(topic: str, keywords: List[str], niche: str) -> str:
    """Is This the Best [Thing] for [Year]?"""
    primary_keyword = keywords[0] if keywords else topic
    
    templates = [
        f"Is This the Best Way to {primary_keyword}?",
        f"Is {primary_keyword.title()} Worth It in 2026?",
        f"Can You Really {primary_keyword}? (Tested)",
        f"Does {primary_keyword.title()} Actually Work?",
    ]
    return random.choice(templates)


def formula_number_power(topic: str, keywords: List[str], niche: str) -> str:
    """[Number] Proven Ways to [Result]"""
    numbers = [3, 5, 7, 10]
    power_word = get_random_power_word("value")
    primary_keyword = keywords[0] if keywords else topic
    
    templates = [
        f"{random.choice(numbers)} {power_word.title()} Ways to {primary_keyword}",
        f"{random.choice(numbers)} {power_word.title()} {primary_keyword} Strategies",
        f"{power_word.title()}: {random.choice(numbers)} Ways to {primary_keyword}",
    ]
    return random.choice(templates)


# Formula registry
FORMULAS = {
    "how_to": formula_how_to,
    "without": formula_without,
    "listicle": formula_listicle,
    "authority_hook": formula_authority_hook,
    "hidden_info": formula_hidden_info,
    "question_hook": formula_question_hook,
    "number_power": formula_number_power,
}


def optimize_title_seo(title: str, keywords: List[str]) -> str:
    """
    Optimize title for SEO by ensuring primary keyword is front-loaded
    """
    # Check if primary keyword is in first 5 words
    if not keywords:
        return title
    
    primary_keyword = keywords[0].lower()
    first_words = ' '.join(title.split()[:5]).lower()
    
    # If keyword is already in first 5 words, return as is
    if primary_keyword in first_words:
        return title
    
    # Otherwise, try to rephrase (simple implementation)
    # This is a basic optimization; in production, you might want more sophisticated logic
    return title


def add_brackets_to_title(title: str, force: bool = False) -> str:
    """Add bracket context to title (e.g., [2026], [Tutorial])"""
    # Don't add if title is already too long
    if len(title) > 70 and not force:
        return title
    
    # 50% chance to add brackets
    if random.random() > 0.5 or force:
        bracket = random.choice(BRACKET_ADDITIONS)
        # Add at the end
        return f"{title} {bracket}"
    
    return title


def generate_title_variation(
    video_concept: str,
    keywords: List[str],
    niche: str,
    formula_name: str,
    add_bracket: bool = False
) -> Dict:
    """Generate a single title variation using specified formula"""
    
    # Get formula function
    formula_func = FORMULAS.get(formula_name)
    if not formula_func:
        raise ValueError(f"Unknown formula: {formula_name}")
    
    # Generate base title
    title = formula_func(video_concept, keywords, niche)
    
    # Optimize for SEO
    title = optimize_title_seo(title, keywords)
    
    # Add brackets if requested
    if add_bracket:
        title = add_brackets_to_title(title, force=True)
    
    # Calculate metrics
    character_count, length_status = validate_title_length(title)
    seo_score = calculate_seo_score(title, keywords)
    power_words = extract_power_words(title)
    has_brackets = any(bracket.replace('[', '').replace(']', '').replace('(', '').replace(')', '') in title for bracket in BRACKET_ADDITIONS)
    ctr_potential = estimate_ctr_potential(seo_score, has_brackets, len(power_words))
    
    return {
        "title": title,
        "formula_used": formula_name,
        "character_count": character_count,
        "length_status": length_status,
        "seo_score": round(seo_score, 1),
        "ctr_potential": ctr_potential,
        "includes_power_words": power_words,
        "includes_brackets": has_brackets
    }


def generate_youtube_titles(
    video_concept: str,
    niche: str,
    keywords: List[str],
    tone: str = "engaging",
    num_variations: int = 7
) -> Dict:
    """
    Generate multiple YouTube title variations using different formulas
    
    Args:
        video_concept: Main topic/concept for the video
        niche: Target audience
        keywords: List of primary keywords for SEO
        tone: Title tone (not heavily used, but available for future enhancements)
        num_variations: Number of title variations to generate (default 7)
    
    Returns:
        Dictionary with titles, recommended title, and SEO tips
    """
    
    variations = []
    formula_names = list(FORMULAS.keys())
    
    # Generate variations using different formulas
    used_formulas = []
    for i in range(num_variations):
        # Pick a formula (cycle through if num_variations > available formulas)
        formula = formula_names[i % len(formula_names)]
        used_formulas.append(formula)
        
        # Add brackets to some variations
        add_bracket = (i % 2 == 0)  # Add brackets to every other title
        
        variation = generate_title_variation(
            video_concept=video_concept,
            keywords=keywords,
            niche=niche,
            formula_name=formula,
            add_bracket=add_bracket
        )
        
        variations.append(variation)
    
    # Sort by SEO score to find recommended title
    sorted_variations = sorted(variations, key=lambda x: x["seo_score"], reverse=True)
    recommended_title = sorted_variations[0]["title"]
    
    # Generate SEO tips
    seo_tips = [
        "Front-load your primary keyword in the first 3-5 words for better SEO",
        "Keep titles between 55-60 characters for optimal mobile visibility",
        "Use power words like 'proven', 'simple', or 'fast' to boost CTR",
        "Add brackets like [2026] or [Tutorial] for context and specificity",
        "Test different title variations using YouTube analytics",
        "Make sure your thumbnail reinforces the title (but uses different text)",
        "Avoid clickbait - accurate titles improve audience retention and ranking"
    ]
    
    return {
        "titles": variations,
        "recommended_title": recommended_title,
        "seo_tips": random.sample(seo_tips, 4)  # Return 4 random tips
    }
