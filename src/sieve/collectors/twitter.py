import tweepy
from typing import List, AsyncIterator
import structlog
from pydantic import BaseModel

from sieve.core.types import Discussion, Platform, DiscussionType

logger = structlog.get_logger()

class TwitterConfig(BaseModel):
    """Twitter API configuration"""
    api_key: str
    api_secret: str
    access_token: str
    access_token_secret: str
    list_ids: List[str]

class TwitterCollector:
    def __init__(self, config: TwitterConfig):
        auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
        auth.set_access_token(config.access_token, config.access_token_secret)
        self.api = tweepy.API(auth)
        self.config = config

    async def collect_discussions(self) -> AsyncIterator[Discussion]:
        """Collect discussions from configured Twitter lists"""
        for list_id in self.config.list_ids:
            try:
                tweets = self.api.list_timeline(
                    list_id=list_id,
                    count=100,
                    tweet_mode="extended"
                )
                
                for tweet in tweets:
                    # Basic engagement score based on likes and retweets
                    engagement = (tweet.favorite_count + tweet.retweet_count) / 100
                    
                    yield Discussion(
                        id=f"twitter_{tweet.id}",
                        platform=Platform.TWITTER,
                        type=DiscussionType.TECHNICAL,  # Simple default
                        title=tweet.full_text[:50],
                        content=tweet.full_text,
                        url=f"https://twitter.com/i/web/status/{tweet.id}",
                        timestamp=tweet.created_at,
                        engagement_score=min(engagement, 1.0),
                        importance_score=0.0,  # Will be set during analysis
                        participants=[tweet.user.screen_name]
                    )
            except Exception as e:
                logger.error("twitter_collection_error", 
                           list_id=list_id, error=str(e)) 