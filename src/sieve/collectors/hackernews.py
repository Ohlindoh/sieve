import aiohttp
from datetime import datetime
from typing import AsyncIterator
import structlog
from pydantic import BaseModel

from sieve.core.types import Discussion, Platform, DiscussionType

logger = structlog.get_logger()

class HNCollector:
    """Simple HackerNews collector that fetches top stories"""
    
    def __init__(self):
        self.base_url = "https://hacker-news.firebaseio.com/v0"
        
    async def collect_discussions(self) -> AsyncIterator[Discussion]:
        """Collect top HN stories and convert them to discussions"""
        async with aiohttp.ClientSession() as session:
            try:
                # Get top story IDs
                async with session.get(f"{self.base_url}/topstories.json") as resp:
                    story_ids = await resp.json()
                
                # Process first 10 stories
                for story_id in story_ids[:10]:
                    async with session.get(f"{self.base_url}/item/{story_id}.json") as resp:
                        story = await resp.json()
                        if story and story.get('type') == 'story':
                            # Basic engagement score based on points and comments
                            engagement = (story.get('score', 0) + story.get('descendants', 0)) / 200
                            
                            yield Discussion(
                                id=f"hn_{story_id}",
                                platform=Platform.HACKERNEWS,
                                type=DiscussionType.TECHNICAL,  # We'll improve this later
                                title=story.get('title', ''),
                                content=story.get('text', ''),
                                url=story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                                timestamp=datetime.fromtimestamp(story.get('time', 0)),
                                engagement_score=min(engagement, 1.0),
                                importance_score=0.0,  # Will be set during analysis
                                participants=[story.get('by', 'unknown')]
                            )
            
            except Exception as e:
                logger.error("hn_collection_error", error=str(e)) 