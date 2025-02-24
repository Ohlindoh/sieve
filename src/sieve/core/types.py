from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class Platform(str, Enum):
    TWITTER = "twitter"
    HACKERNEWS = "hackernews"
    GITHUB = "github"

class DiscussionType(str, Enum):
    TECHNICAL = "technical"
    ANNOUNCEMENT = "announcement"
    DEBATE = "debate"
    TREND = "trend"

class Discussion(BaseModel):
    """Represents a tracked discussion across platforms"""
    id: str
    platform: Platform
    type: DiscussionType
    title: str
    content: str
    url: str
    timestamp: datetime
    engagement_score: float
    importance_score: float
    participants: List[str]
    context: Optional[str] = None
    related_discussions: List[str] = Field(default_factory=list)

class AnalysisResult(BaseModel):
    """Results of agent analysis on discussions"""
    discussion_id: str
    key_insights: List[str]
    technical_validity: float
    community_sentiment: float
    expert_consensus: Optional[float] = None
    action_items: List[str] = Field(default_factory=list) 