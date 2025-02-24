import httpx
from datetime import datetime
from typing import List, Dict, Any

class HNCollector:
    """Simple HackerNews collector for MVP."""
    
    BASE_URL = "https://hacker-news.firebaseio.com/v0"
    
    async def get_top_stories(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch top stories from HN."""
        async with httpx.AsyncClient() as client:
            # Get top story IDs
            response = await client.get(f"{self.BASE_URL}/topstories.json")
            story_ids = response.json()[:limit]
            
            # Fetch story details
            stories = []
            for story_id in story_ids:
                story_resp = await client.get(f"{self.BASE_URL}/item/{story_id}.json")
                story = story_resp.json()
                if story and story.get('type') == 'story':
                    stories.append({
                        'title': story.get('title'),
                        'url': story.get('url'),
                        'points': story.get('score'),
                        'num_comments': story.get('descendants', 0),
                        'external_id': str(story_id)
                    })
            
            return stories

    def filter_stories_by_topic(self, stories: List[Dict[str, Any]], topics: List[str]) -> List[Dict[str, Any]]:
        """Filter stories based on topic keywords."""
        filtered_stories = []
        for story in stories:
            title = story['title'].lower()
            if any(topic.lower() in title for topic in topics):
                filtered_stories.append(story)
        return filtered_stories 