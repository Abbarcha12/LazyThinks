from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class UGCRequest(BaseModel):
    idea: str = Field(description="Product/concept to promote", min_length=5)
    niche: str = Field(description="Target audience/niche", min_length=3)
    tone: str = Field(description="Video tone: casual, professional, humorous, energetic")
    platform: str = Field(description="Platform: instagram, tiktok, youtube_shorts")
    length: int = Field(description="Duration in seconds", ge=15, le=60)
    language: str = Field(default="english", description="Language for script generation")


class Shot(BaseModel):
    shot_number: int
    type: str  # hook, problem, solution, proof, cta, b-roll
    duration: int
    scene: str
    script: str
    emotion: str
    camera: str
    image_prompt: str
    video_prompt: str


class VideoConcept(BaseModel):
    hook: str
    problem: str
    solution: str
    proof: str
    cta: str


class ProductionNotes(BaseModel):
    character_description: str
    setting: str
    total_estimated_duration: int
    tips: List[str]


class VoiceScript(BaseModel):
    full_text: str
    suggested_voice: str
    estimated_duration: int


class UGCScriptResponse(BaseModel):
    video_concept: VideoConcept
    shots: List[Shot]
    production_notes: ProductionNotes
    voice_script: VoiceScript


# YouTube Title Generator Models
class YouTubeTitleRequest(BaseModel):
    video_concept: str = Field(description="Main topic/concept for the video", min_length=3)
    niche: str = Field(description="Target audience", min_length=2)
    keywords: List[str] = Field(description="Primary keywords for SEO (1-5 keywords)", min_items=1, max_items=5)
    tone: str = Field(default="engaging", description="Title tone: engaging, professional, casual, exciting")
    num_variations: int = Field(default=7, ge=3, le=10, description="Number of title variations to generate")


class TitleVariation(BaseModel):
    title: str
    formula_used: str
    character_count: int
    length_status: str  # "optimal", "good", "too_short", "too_long", "acceptable"
    seo_score: float
    ctr_potential: str  # "high", "medium", "low"
    includes_power_words: List[str]
    includes_brackets: bool


class YouTubeTitleResponse(BaseModel):
    titles: List[TitleVariation]
    recommended_title: str
    seo_tips: List[str]


# Multi-Agent Validation Models
class TitleValidationRequest(BaseModel):
    video_concept: str = Field(description="Main topic/concept", min_length=3)
    niche: str = Field(description="Target audience", min_length=2)
    keywords: List[str] = Field(description="SEO keywords", min_items=1, max_items=5)
    titles_to_validate: List[str] = Field(description="Titles to validate (from initial generation)")
    max_research_depth: int = Field(default=20, ge=10, le=50, description="Number of videos to analyze")


class ValidatedTitleData(BaseModel):
    title: str
    validation_status: str  # "APPROVED", "REJECTED", "NEEDS_IMPROVEMENT"
    confidence_score: float
    reasoning: List[str]
    final_score: float
    predicted_ctr: float
    rank: int


class AgentMessageData(BaseModel):
    id: str
    sender: str
    receiver: str
    type: str
    content: Dict
    timestamp: str
    parent_id: Optional[str] = None


class MultiAgentValidationResponse(BaseModel):
    validated_titles: List[ValidatedTitleData]
    top_recommendation: Optional[ValidatedTitleData]
    conversation_log: List[AgentMessageData]
    research_summary: Dict
    competitor_analysis: Dict
    final_recommendation: str
    total_confidence: float
    processing_time: float
    approved_count: int
    thumbnail_data: Optional[Dict] = None

