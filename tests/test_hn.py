import asyncio
from sieve.collectors.hackernews import HNCollector

async def main():
    collector = HNCollector()
    async for discussion in collector.collect_discussions():
        print(f"\nTitle: {discussion.title}")
        print(f"URL: {discussion.url}")
        print(f"Score: {discussion.engagement_score}")
        print("---")

if __name__ == "__main__":
    asyncio.run(main()) 