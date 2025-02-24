import asyncio
import logging
from sieve.collectors.hackernews import HNCollector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Test the HackerNews collector."""
    collector = HNCollector()
    count = 0
    
    logger.info("Starting to collect HackerNews stories...")
    
    async for discussion in collector.collect_discussions():
        logger.info("\n=== Story %d ===", count + 1)
        logger.info("Title: %s", discussion.title)
        logger.info("URL: %s", discussion.url)
        logger.info("Score: %d", discussion.engagement_score)
        
        count += 1
        if count >= 5:  # Just get 5 stories for testing
            break
    
    logger.info("\nDone! Collected %d stories.", count)

if __name__ == "__main__":
    asyncio.run(main()) 