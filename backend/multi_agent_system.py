"""
Multi-Agent System for YouTube Title Validation
Implements Research, Competitor, and Validator agents with A2A communication
"""

import os
from typing import List, Dict, Optional
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from a2a_protocol import protocol, AgentMessage
from youtube_research import research_youtube_topic, predict_ctr, analyze_title_patterns
import json


class BaseAgent:
    """
    Base Agent class with LLM integration and A2A protocol support
    """
    
    def __init__(self, name: str, role: str, llm: ChatGroq):
        self.name = name
        self.role = role
        self.llm = llm
        self.inbox: List[AgentMessage] = []
        
        # Register with protocol
        protocol.register_agent(name, self)
    
    def receive_message(self, message: AgentMessage):
        """Receive message from another agent"""
        self.inbox.append(message)
        print(f"📨 {self.name} received message from {message.sender}")
    
    def send_message(
        self,
        conversation_id: str,
        receiver: str,
        message_type: str,
        data: Dict,
        parent_message_id: Optional[str] = None
    ) -> AgentMessage:
        """Send message via A2A protocol"""
        return protocol.send_message(
            conversation_id=conversation_id,
            sender=self.name,
            receiver=receiver,
            message_type=message_type,
            data=data,
            parent_message_id=parent_message_id
        )
    
    def think(self, context: str, output_schema: Optional[type] = None) -> Dict:
        """
        Use LLM to think and reason about a problem
        Returns JSON response
        """
        try:
            if output_schema:
                parser = JsonOutputParser(pydantic_object=output_schema)
                chain = self.llm | parser
            else:
                parser = JsonOutputParser()
                chain = self.llm | parser
            
            response = chain.invoke(context)
            return response
        except Exception as e:
            print(f"❌ {self.name} thinking error: {e}")
            return {"error": str(e)}


class ResearchAgent(BaseAgent):
    """
    Research Agent - Investigates topics and gathers YouTube data
    """
    
    def __init__(self, llm: ChatGroq):
        super().__init__(name="research", role="Topic Researcher", llm=llm)
    
    def research_topic(
        self,
        conversation_id: str,
        video_concept: str,
        niche: str,
        keywords: List[str]
    ) -> Dict:
        """
        Research the topic on YouTube and gather insights
        """
        print(f"\n🔍 {self.name.upper()}: Starting research on '{video_concept}'")
        
        # Build search query
        search_query = f"{keywords[0]} {video_concept}" if keywords else video_concept
        
        # Research YouTube
        research_data = research_youtube_topic(search_query, max_results=20)
        
        # Use LLM to analyze research findings
        analysis_prompt = f"""
        You are a YouTube research expert. Analyze the following research data and provide insights.
        
        VIDEO CONCEPT: {video_concept}
        TARGET NICHE: {niche}
        KEYWORDS: {', '.join(keywords)}
        
        RESEARCH DATA:
        - Videos Found: {research_data.get('videos_found', 0)}
        - Top Performing Titles: {json.dumps(research_data.get('top_performing_titles', []))}
        - Pattern Analysis: {json.dumps(research_data.get('patterns', {}))}
        - Recommended Keywords: {json.dumps(research_data.get('recommended_keywords', []))}
        
        Provide a JSON response with:
        {{
            "topic_analysis": {{
                "trend_score": <0-100>,
                "search_volume": "low/medium/high",
                "competition_level": "low/medium/high"
            }},
            "successful_patterns": [
                "pattern 1",
                "pattern 2"
            ],
            "recommended_keywords": ["keyword1", "keyword2"],
            "key_insights": [
                "insight 1",
                "insight 2"
            ],
            "confidence_score": <0.0-1.0>
        }}
        """
        
        llm_analysis = self.think(analysis_prompt)
        
        # Combine research data with LLM analysis
        result = {
            "raw_research": research_data,
            "llm_analysis": llm_analysis,
            "top_performing_titles": research_data.get('top_performing_titles', []),
            "patterns": research_data.get('patterns', {}),
            "recommended_keywords": llm_analysis.get('recommended_keywords', keywords)
        }
        
        # Send findings to other agents
        self.send_message(
            conversation_id=conversation_id,
            receiver="all",
            message_type="RESEARCH_COMPLETE",
            data=result
        )
        
        print(f"✅ {self.name.upper()}: Research complete. Found {research_data.get('videos_found', 0)} videos")
        
        return result


class CompetitorAgent(BaseAgent):
    """
    Competitor Agent - Analyzes titles and suggests improvements
    """
    
    def __init__(self, llm: ChatGroq):
        super().__init__(name="competitor", role="Title Critic & Improver", llm=llm)
    
    def analyze_titles(
        self,
        conversation_id: str,
        titles: List[str],
        research_data: Dict
    ) -> Dict:
        """
        Analyze proposed titles and suggest improvements
        """
        print(f"\n🏆 {self.name.upper()}: Analyzing {len(titles)} titles")
        
        # Get research insights
        patterns = research_data.get('patterns', {})
        top_performers = research_data.get('top_performing_titles', [])
        
        # Analyze each title
        title_analyses = []
        
        for title in titles:
            # Predict CTR
            predicted_ctr = predict_ctr(title, research_data.get('raw_research', {}))
            
            # Use LLM to critique
            critique_prompt = f"""
            You are a YouTube title expert. Critically analyze this title.
            
            TITLE: "{title}"
            
            TOP PERFORMING TITLES IN NICHE:
            {json.dumps(top_performers[:3], indent=2)}
            
            SUCCESSFUL PATTERNS:
            - {patterns.get('contains_number', 0)}% of top titles contain numbers
            - {patterns.get('contains_brackets', 0)}% use brackets/parentheses
            - {patterns.get('contains_question', 0)}% are questions
            - Average length: {patterns.get('average_length', 50)} characters
            
            Provide JSON analysis:
            {{
                "strengths": ["strength 1", "strength 2"],
                "weaknesses": ["weakness 1", "weakness 2"],
                "improvement_suggestions": ["suggestion 1", "suggestion 2"],
                "comparison_to_top_performers": "how it compares",
                "predicted_performance": "poor/fair/good/excellent"
            }}
            """
            
            critique = self.think(critique_prompt)
            
            title_analyses.append({
                "title": title,
                "predicted_ctr": round(predicted_ctr, 2),
                "strengths": critique.get('strengths', []),
                "weaknesses": critique.get('weaknesses', []),
                "improvement_suggestions": critique.get('improvement_suggestions', []),
                "performance_rating": critique.get('predicted_performance', 'fair')
            })
        
        # Generate alternative titles
        alternatives = self.generate_alternatives(conversation_id, title_analyses, research_data)
        
        result = {
            "title_analyses": title_analyses,
            "alternative_titles": alternatives,
            "recommendation": f"Consider alternatives for titles with CTR < {round(sum(t['predicted_ctr'] for t in title_analyses) / len(title_analyses), 1)}%"
        }
        
        # Send analysis to validator
        self.send_message(
            conversation_id=conversation_id,
            receiver="validator",
            message_type="ANALYSIS_COMPLETE",
            data=result
        )
        
        print(f"✅ {self.name.upper()}: Analysis complete. Generated {len(alternatives)} alternatives")
        
        return result
    
    def generate_alternatives(
        self,
        conversation_id: str,
        title_analyses: List[Dict],
        research_data: Dict
    ) -> List[Dict]:
        """Generate alternative improved titles"""
        
        # Find weakest titles
        weak_titles = [t for t in title_analyses if t['predicted_ctr'] < 6.0]
        
        if not weak_titles:
            return []
        
        alternatives = []
        
        for weak in weak_titles[:3]:  # Limit to top 3 weakest
            improvement_prompt = f"""
            Create an IMPROVED version of this YouTube title.
            
            ORIGINAL TITLE: "{weak['title']}"
            
            WEAKNESSES:
            {json.dumps(weak['weaknesses'], indent=2)}
            
            IMPROVEMENT SUGGESTIONS:
            {json.dumps(weak['improvement_suggestions'], indent=2)}
            
            TOP PERFORMING PATTERNS:
            {json.dumps(research_data.get('patterns', {}), indent=2)}
            
            Create 2 alternative titles that fix the weaknesses. Return JSON:
            {{
                "alternatives": [
                    "alternative title 1",
                    "alternative title 2"
                ],
                "reasoning": "why these are better"
            }}
            """
            
            result = self.think(improvement_prompt)
            
            for alt in result.get('alternatives', []):
                alternatives.append({
                    "original": weak['title'],
                    "improved": alt,
                    "reasoning": result.get('reasoning', ''),
                    "predicted_ctr": predict_ctr(alt, research_data.get('raw_research', {}))
                })
        
        return alternatives


class ValidatorAgent(BaseAgent):
    """
    Validator Agent - Final decision maker and quality assurance
    """
    
    def __init__(self, llm: ChatGroq):
        super().__init__(name="validator", role="Final Validator", llm=llm)
    
    def validate_titles(
        self,
        conversation_id: str,
        original_titles: List[str],
        research_data: Dict,
        competitor_analysis: Dict
    ) -> Dict:
        """
        Make final validation decisions on all titles
        """
        print(f"\n✅ {self.name.upper()}: Validating titles")
        
        # Combine original titles with alternatives
        all_titles = original_titles.copy()
        alternatives = competitor_analysis.get('alternative_titles', [])
        for alt in alternatives:
            all_titles.append(alt['improved'])
        
        # Validate each title
        validated_titles = []
        
        for title in all_titles:
            # Calculate confidence score
            confidence = self.calculate_confidence(
                title,
                research_data,
                competitor_analysis
            )
            
            # Get validation decision
            validation_prompt = f"""
            As the final validator, decide if this YouTube title should be APPROVED.
            
            TITLE: "{title}"
            
            RESEARCH INSIGHTS:
            {json.dumps(research_data.get('llm_analysis', {}), indent=2)}
            
            COMPETITOR ANALYSIS:
            {json.dumps(competitor_analysis.get('title_analyses', [])[:2], indent=2)}
            
            CONFIDENCE SCORE: {confidence}
            
            Return JSON decision:
            {{
                "validation_status": "APPROVED/REJECTED/NEEDS_IMPROVEMENT",
                "reasoning": ["reason 1", "reason 2"],
                "final_score": <0-100>,
                "recommendation_rank": <1-10>
            }}
            """
            
            decision = self.think(validation_prompt)
            
            if decision.get('validation_status') in ['APPROVED', 'NEEDS_IMPROVEMENT']:
                validated_titles.append({
                    "title": title,
                    "validation_status": decision.get('validation_status', 'APPROVED'),
                    "confidence_score": confidence,
                    "reasoning": decision.get('reasoning', []),
                    "final_score": decision.get('final_score', 70),
                    "predicted_ctr": predict_ctr(title, research_data.get('raw_research', {})),
                    "rank": decision.get('recommendation_rank', 5)
                })
        
        # Sort by rank and score
        validated_titles.sort(key=lambda x: (x['rank'], -x['final_score']))
        
        # Top recommendation
        top_title = validated_titles[0] if validated_titles else None
        
        result = {
            "validated_titles": validated_titles,
            "top_recommendation": top_title,
            "total_analyzed": len(all_titles),
            "approved_count": len([t for t in validated_titles if t['validation_status'] == 'APPROVED']),
            "final_recommendation": f"Use '{top_title['title']}' with {round(top_title['confidence_score'] * 100)}% confidence" if top_title else "No suitable titles found"
        }
        
        # Send final decision
        self.send_message(
            conversation_id=conversation_id,
            receiver="all",
            message_type="FINAL_DECISION",
            data=result
        )
        
        print(f"✅ {self.name.upper()}: Validation complete. {result['approved_count']} titles approved")
        
        return result
    
    def calculate_confidence(
        self,
        title: str,
        research_data: Dict,
        competitor_analysis: Dict
    ) -> float:
        """
        Calculate confidence score for a title based on all evidence
        Returns score between 0.0 and 1.0
        """
        score = 0.5  # Base confidence
        
        # Check against research patterns
        patterns = research_data.get('patterns', {})
        
        # Numbers boost confidence if common in niche
        if patterns.get('contains_number', 0) > 50 and any(c.isdigit() for c in title):
            score += 0.1
        
        # Brackets boost if common
        if patterns.get('contains_brackets', 0) > 30 and ('[' in title or '(' in title):
            score += 0.08
        
        # Length matches niche average
        avg_length = patterns.get('average_length', 50)
        if abs(len(title) - avg_length) < 10:
            score += 0.12
        
        # Contains recommended keywords
        rec_keywords = research_data.get('recommended_keywords', [])
        if any(keyword.lower() in title.lower() for keyword in rec_keywords[:3]):
            score += 0.15
        
        # High predicted CTR
        predicted_ctr = predict_ctr(title, research_data.get('raw_research', {}))
        if predicted_ctr > 7.0:
            score += 0.15
        elif predicted_ctr > 6.0:
            score += 0.08
        
        # Cap at 1.0
        return min(1.0, score)


from integrations.stability_ai import generate_image_stable_diffusion

class ThumbnailAgent(BaseAgent):
    """
    Thumbnail Agent - Designs and generates viral thumbnails
    """
    
    def __init__(self, llm: ChatGroq):
        super().__init__(name="thumbnail", role="Visual Strategist", llm=llm)
    
    def generate_thumbnails(
        self,
        conversation_id: str,
        title: str,
        video_concept: str,
        niche: str,
        research_data: Dict
    ) -> Dict:
        """
        Design and generate a thumbnail for the validated title
        """
        print(f"\n🎨 {self.name.upper()}: Designing thumbnail for '{title}'")
        
        # Design thumbnail concept using LLM
        design_prompt = f"""
        You are a world-class YouTube thumbnail designer (like MrBeast's team).
        Design a high-CTR thumbnail for this video.
        
        TITLE: "{title}"
        Use this title to guide the visual hook.
        
        CONCEPT: {video_concept}
        NICHE: {niche}
        
        REQUIREMENTS:
        - Aspect Ratio: 16:9 (YouTube Standard)
        - Text Overlay: MUST include specific, bold text on the image (max 3-5 words).
        - Style: High contrast, expressive faces (if applicable), vibrant colors.
        
        RESEARCH AND PATTERNS:
        {json.dumps(research_data.get('patterns', {}), indent=2)}
        
        Create a detailed visual concept.
        
        Return JSON ONLY:
        {{
            "visual_concept": "Description of the scene",
            "text_overlay": "Exact text to appear on image (e.g., 'INSANE RESULT!', 'DON'T DO THIS')",
            "colors": ["#color1", "#color2"],
            "elements": ["element1", "element2"],
            "image_prompt": "Detailed Stable Diffusion XL prompt. START WITH: 'YouTube thumbnail, 8k resolution, text overlay saying \"[TEXT_OVERLAY]\" in bold modern font'. Describe placement of text. High quality, realistic/illustrated, dramatic lighting.",
            "reasoning": "Why this will get clicks"
        }}
        """
        
        design = self.think(design_prompt)
        
        # Try to generate actual images
        image_paths = []
        image_urls = []
        
        try:
            # Generate images using Stability AI
            prompt = design.get('image_prompt', '')
            if prompt:
                print(f"🎨 {self.name.upper()}: Generating 3 variants with AI...")
                # Request 3 samples
                generated_paths = generate_image_stable_diffusion(prompt, samples=3)
                
                image_paths = generated_paths
                
                # Create URLs
                for path in image_paths:
                    filename = os.path.basename(path)
                    image_urls.append(f"/generated_images/{filename}")
                
        except Exception as e:
            print(f"⚠️ Image generation failed (likely no API key): {e}")
            # If generation fails, we still return the design
        
        result = {
            "title": title,
            "design": design,
            "image_paths": image_paths,
            "image_urls": image_urls,
            "status": "GENERATED" if image_paths else "DESIGN_ONLY"
        }
        
        # Share with group
        self.send_message(
            conversation_id=conversation_id,
            receiver="all",
            message_type="THUMBNAIL_COMPLETE",
            data=result
        )
        
        print(f"✅ {self.name.upper()}: Thumbnail task complete")
        return result


def create_agent_system() -> Dict[str, BaseAgent]:
    """
    Create and initialize the multi-agent system
    """
    # Initialize LLM (Groq)
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found")
    
    llm = ChatGroq(
        temperature=0.7,
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile"
    )
    
    # Create agents
    agents = {
        "research": ResearchAgent(llm),
        "competitor": CompetitorAgent(llm),
        "validator": ValidatorAgent(llm),
        "thumbnail": ThumbnailAgent(llm)
    }
    
    print("🤖 Multi-Agent System initialized")
    print("   - Research Agent ✓")
    print("   - Competitor Agent ✓")
    print("   - Validator Agent ✓")
    print("   - Thumbnail Agent ✓")
    
    return agents
