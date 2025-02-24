"""HackerNews collector for fetching top stories."""

import aiohttp
import asyncio
from dataclasses import dataclass
from typing import AsyncIterator
import logging

logger = logging.getLogger(__name__)

@dataclass
class Discussion:
    """Represents a HackerNews discussion."""
    title: str
    url: str
    engagement_score: int

class HNCollector:
    """Collects discussions from HackerNews."""
    
    def __init__(self) -> None:
        self.base_url = "https://hacker-news.firebaseio.com/v0"
        
    async def fetch_item(self, session: aiohttp.ClientSession, item_id: int) -> dict:
        """Fetch a single HN item."""
        async with session.get(f"{self.base_url}/item/{item_id}.json") as response:
            return await response.json()
            
    async def collect_discussions(self) -> AsyncIterator[Discussion]:
        """Collect top stories from HackerNews."""
        async with aiohttp.ClientSession() as session:
            # Get top story IDs
            async with session.get(f"{self.base_url}/topstories.json") as response:
                story_ids = await response.json()
                
            # Process each story
            for story_id in story_ids:
                try:
                    story = await self.fetch_item(session, story_id)
                    if story and 'title' in story and 'url' in story:
                        yield Discussion(
                            title=story['title'],
                            url=story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                            engagement_score=story.get('score', 0)
                        )
                except Exception as e:
                    logger.error(f"Error processing story {story_id}: {str(e)}")
                    continue 