# AIDA UGC Script Template

```python
ugc_prompt_aida = PromptTemplate(
    template="""Act as a WORLD-CLASS UGC Scriptwriter. Create a {length}-second authentic,  high-energy, relatable video script for {platform}.

## BRAND/PRODUCT:
{idea}

## TARGET AUDIENCE:
{niche}

## TONE:
{tone}

## LANGUAGE:
{language}

##===== CRITICAL INSTRUCTION =====##
YOU MUST FOLLOW THE "AIDA" FRAMEWORK (Gold Standard for Direct-Response):

### 🎯 ATTENTION (0-3 seconds) - Pattern Interrupt
Use ONE of these PSYCHOLOGICAL HOOKS:
  - "Stop scrolling if you [problem]..."
  - "I wish I knew about this sooner..."
  - "I'm going to stop gatekeeping my favorite..."
  - "This is why your [X] isn't working..." 
  - "POV: You finally found the perfect [product]..."

### 🤔 INTEREST (3-10 seconds) - Agitate Pain Point
Show the "BEFORE" state. Make it RELATABLE:
  - Use specific, visceral language about the struggle
  - "I used to [struggle] and it was SO frustrating..."
  - Show emotional vulnerability

### ✨ DESIRE (10-25 seconds) - Introduce Solution ("The Bridge")
The HERO moment:
  -  "Then I tried {idea} and honestly..."
  - Show the "AFTER" state (Before vs. After technique)
  -  Features → Benefits ("The 'So What?' Test")
  - "Without this, I'd still be..."
  - Use "Us vs. Them" positioning (don't name competitors)

### 🎬 ACTION (25-30 seconds) - Single, Clear CTA
  - Direct command: "Go grab yours now"
  - Urgency: "Limited time / Use code..."
  - Where: "Link in bio"

##===== PROMOTIONAL TECHNIQUES (Choose 1-2) =====##
1. **The Bridge**: Before (Struggle) → After (Success)
2. **Green Screen**: Talk over review screenshot or website
3. **The Haul/Unboxing**: Focus on physical tactile experience
4. **The Aesthetic POV**: "POV: You finally..."

##===== SHOT-BY-SHOT BREAKDOWN =====##
Generate {num_shots} shots. For EACH shot:

1. **shot_number**: 1, 2, 3...
2. **type**: attention, interest, desire, action (map from AIDA)
3. **duration**: 3-7 seconds (total = {length}s)
4. **scene**: Visual instruction [Creator action]. ENGLISH ONLY.
5. **script**: AUTHENTIC dialogue ("okay so", "literally", "honestly"). IN {language}.
6. **emotion**: excited, curious, frustrated, relieved, confident
7. **camera**: selfie-angle, slow-zoom, handheld, static
8. **image_prompt**: First-frame image prompt (Midjourney/DALL-E). ENGLISH ONLY.
9. **video_prompt**: Motion/action for video gen (Stable Video Diffusion). ENGLISH ONLY.

##===== OPTIMIZATION CHECKLIST (Auto-Apply) =====##
✅ **Native Feel**: Sounds like a real person, not corporate jargon
✅ **Visual Storytelling**: Include B-roll instructions ([Product close-up], [Screen recording])
✅ **"So What?" Test**: Every feature explains how it helps the viewer

##===== CRITICAL RULES =====##
- Use FIRST-PERSON ("I", "my")
- Natural speech patterns ("umm", "like", "okay so")
- NO robotic/salesy language
- Total duration = {length} seconds
- **Image/Video Prompts**: ENGLISH
- **Scene descriptions**: ENGLISH  
- **Script/Dialogue**: {language}
  - If Urdu: Use Urdu script (کیا حال ہے)
  - If English: Use English

##===== OUTPUT FORMAT (JSON ONLY) =====##
{{
  "video_concept": {{
    "hook_strategy": "Psychological hook used (English)",
    "problem_agitation": "Pain point (English)",
    "solution_bridge": "Product positioning (English)",
    "proof_technique": "Credibility method (English)",
    "cta_action": "Call to action (English)"
  }},
  "shots": [
    {{
      "shot_number": 1,
      "type": "attention",
      "duration": 3,
      "scene": "[Creator looks at camera, holding product]",
      "script": "Stop scrolling if you've been struggling with...",
      "emotion": "urgent",
      "camera": "selfie-angle",
      "image_prompt": "Close-up portrait of person holding product to camera, bright natural lighting",
      "video_prompt": "Person talking directly to camera with product, slight head movement, eye contact"
    }},
    ... ({num_shots} total shots following AIDA)
  ],
  "production_notes": {{
    "character_description": "Ideal creator persona",
    "setting": "Primary location",
    "total_estimated_duration": {length},
    "aida_breakdown": "Attention: 0-3s, Interest: 3-10s, Desire: 10-25s, Action: 25-30s",
    "tips": ["Tip 1", "Tip 2", "Tip 3"]
  }},
  "voice_script": {{
    "full_text": "Complete narration combining all dialogue in {language}...",
    "suggested_voice": "Voice profile",
    "estimated_duration": {length}
  }}
}}

Generate the AIDA UGC script NOW:""",
    input_variables=["idea", "niche", "tone", "platform", "length", "num_shots", "language"]
)
```
