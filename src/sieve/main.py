import asyncio
from sieve.services.collector import HNCollector
from sieve.services.emailer import EmailDigest

async def run_digest(dry_run: bool = True):
    collector = HNCollector()
    emailer = EmailDigest()
    
    # Simple MVP - just AI/ML topics
    topics = ["AI", "LLM", "GPT", "Machine Learning"]
    
    try:
        print("Fetching stories...")
        stories = await collector.get_top_stories(limit=100)
        print(f"Found {len(stories)} total stories")
        
        relevant_stories = collector.filter_stories_by_topic(stories, topics)
        print(f"\nFound {len(relevant_stories)} relevant stories about {', '.join(topics)}")
        
        if relevant_stories:
            print("\nHere's what would be in the digest:")
            print("-" * 50)
            for story in relevant_stories:
                print(f"\nTitle: {story['title']}")
                print(f"URL: {story['url']}")
                print(f"Points: {story['points']} | Comments: {story['num_comments']}")
            print("-" * 50)
            
            if not dry_run:
                emailer.send_digest("your@email.com", relevant_stories)
                print("\nEmail sent!")
            else:
                print("\nDry run - no email sent")
        else:
            print("\nNo relevant stories found")
            
    except Exception as e:
        print(f"Error running digest: {e}")

if __name__ == "__main__":
    asyncio.run(run_digest(dry_run=True)) 