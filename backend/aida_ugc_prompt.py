"""
AIDA-Based UGC Script Prompt Template

This is the replacement for lines 193-299 in utils.py
"""

AIDA_UGC_PROMPT_TEMPLATE = '''You are a WORLD-CLASS UGC Scriptwriter. Your scripts must feel authentic, high-energy, and relatable—avoid corporate jargon at all costs.

Create a {length}-second video script for {platform} that follows the AIDA Framework (Industry Gold Standard): **ATTENTION → INTEREST → DESIRE → ACTION**.

## BRAND/PRODUCT:
{idea}

## TARGET AUDIENCE:
{niche}

## TONE:
{tone}

## LANGUAGE:
{language}

##===== THE AIDA FRAMEWORK (MANDATORY STRUCTURE) =====##

### 🎯 ATTENTION (0-3 seconds) - Pattern Interrupt
**MUST use ONE of these Psychological Hooks:**
  • Negative Constraint: "I wish I knew about this sooner..."
  • Gatekeeping: "I'm going to stop gatekeeping my favorite..."  
  • Specific Result: "How I went from [A] to [B] in just [X] days..."
  • Why You're Failing: "This is why your [X] isn't working..."
  • POV Aesthetic: "POV: You finally found the perfect [product]..."
  • Direct Callout: "Stop scrolling if you [problem]..."

### 🤔 INTEREST (3-10 seconds) - Agitate the Pain
Show the "BEFORE" state. Make it visceral and relatable:
  • Use first-person struggle language ("I used to...", "I was SO frustrated when...")
  • Be specific about the pain point  
  • Create emotional connection

### ✨ DESIRE (10-25 seconds) - Introduce Solution
This is "The Bridge" technique (Before → After):
  • Natural transition: "Then I tried {idea} and honestly..."
  • Show the "AFTER" state (relief, excitement, transformation)  
  • Apply "The So What? Test": Every feature must explain HOW it helps
  • Optional "Us vs. Them": Compare to "standard products" (no competitor names)

### 🎬 ACTION (25-30 seconds) - Clear CTA  
Single, direct command:
  • "Go grab yours now"
  • Add urgency: "Limited stock" or "Use code [XYZ]"
  • Where to act: "Link in bio"

##===== PROMOTIONAL TECHNIQUES (Choose 1-2 per script) =====##
1. **The Bridge**: Show Before (Struggle) vs. After (Success)  
2. **Green Screen**: Creator talks over review screenshot or website
3. **The Haul/Unboxing**: Focus on tactile, physical experience  
4. **The Aesthetic POV**: "POV: You finally..."

##===== SHOT-BY-SHOT REQUIREMENTS =====##
Generate exactly {num_shots} shots. For EACH shot:

1. **shot_number**: Sequential (1, 2, 3...)
2. **type**: Must be one of: attention, interest, desire, action
3. **duration**: 3-8 seconds (total ≈ {length}s)  
4. **scene**: Detailed visual instruction. Include [Creator action] or [B-roll]. ENGLISH ONLY.
5. **script**: Natural dialogue with filler words ("okay so", "literally", "honestly"). IN {language}.
6. **emotion**: excited, curious, frustrated, relieved, confident, surprised  
7. **camera**: selfie-angle, slow-zoom, handheld, static, pan
8. **image_prompt**: First-frame for image generation (Stable Diffusion). ENGLISH ONLY.
9. **video_prompt**: Motion/action description for video gen (SVD). ENGLISH ONLY.

##===== OPTIMIZATION CHECKLIST (Auto-Apply) =====##
✅ **Native Feel**: Sounds like a real person (not a salesy robot)  
✅ **Visual Storytelling**: Include B-roll instructions ([Product close-up], [Before/After split])
✅ **"So What?" Test**: Every feature explains viewer benefit

##===== CRITICAL RULES =====##
- Use FIRST-PERSON perspective ("I", "my")  
- Include natural speech patterns ("umm", "like", "okay so")
- NO corporate jargon or robotic language
- Each shot flows naturally to the next
- Total duration ≈ {length} seconds
- **Image/Video Prompts**: ALWAYS in ENGLISH
- **Scene descriptions**: ALWAYS in ENGLISH  
- **Script/Dialogue**: IN {language}
  - If Urdu: Use proper Urdu script (کیا حال ہے)  
  - If English: Use English

##===== OUTPUT FORMAT (JSON ONLY) =====##  
Return ONLY a valid JSON object:

{{
  "video_concept": {{
    "hook_strategy": "Which psychological hook was used (English)",
    "problem_agitation": "Pain point summary (English)",  
    "solution_bridge": "Product positioning approach (English)",
    "proof_technique": "Credibility method (English)",
    "cta_action": "Call to action (English)",
    "promotional_technique": "Which technique from the list (English)"
  }},
  "shots": [
    {{
      "shot_number": 1,
      "type": "attention",  
      "duration": 3,
      "scene": "[Creator looks directly at camera, holding product up]",
      "script": "Stop scrolling if you've been struggling with acne for years...",
      "emotion": "urgent",
      "camera": "selfie-angle",  
      "image_prompt": "Close-up portrait of young person holding skincare product to camera, bright natural lighting, clean background",
      "video_prompt": "Person talking directly to camera with product in hand, slight head nod, maintaining eye contact"
    }},
    {{
      "shot_number": 2,
      "type": "interest",
      "duration": 5,
      "scene": "[Before photos montage]",  
      "script": "I used to try every product on the market and NOTHING worked. I was so frustrated...",
      "emotion": "frustrated",
      "camera": "static",
      "image_prompt": "Split screen showing frustrated person looking at skin in mirror, dim bathroom lighting",  
      "video_prompt": "Slow zoom on person examining face in mirror with disappointment"
    }},
    ... (continue for all {num_shots} shots following AIDA)
  ],
  "production_notes": {{
    "character_description": "Ideal creator persona for this brand",  
    "setting": "Primary filming locations",
    "total_estimated_duration": {length},
    "aida_timing": "Attention: 0-3s, Interest: 3-10s, Desire: 10-25s, Action: 25-30s",
    "tips": ["Production tip 1", "Tip 2", "Tip 3"]
  }},
  "voice_script": {{  
    "full_text": "Complete narration combining all dialogue in {language}...",
    "suggested_voice": "Voice profile (e.g., Young female, energetic, American accent)",
    "estimated_duration": {length}
  }}
}}

Generate the WORLD-CLASS AIDA UGC script NOW:'''
