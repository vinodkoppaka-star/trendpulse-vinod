
import requests
import time
import json
import os
from datetime import datetime

# Base URLs for HackerNews API
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header as required
HHEADERS = {"User-Agent": "TrendPulse/1.0"}

# Category keywords (case-insensitive matching)
CATEGORIES = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

# Max stories per category
MAX_PER_CATEGORY = 25


def get_top_story_ids(limit=500):
    """
    Fetch top story IDs from HackerNews API.
    Returns a list of IDs (max 'limit').
    """
    try:
        response = requests.get(TOP_STORIES_URL, headers=HEADERS)
        response.raise_for_status()
        return response.json()[:limit]
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return []


def get_story_details(story_id):
    """
    Fetch details for a single story.
    Returns JSON data or None if request fails.
    """
    try:
        url = ITEM_URL.format(story_id)
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to fetch story {story_id}: {e}")
        return None


def categorize_title(title):
    """
    Assign category based on keywords in title.
    Returns category name or None if no match.
    """
    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category

    return "entertainment"  # No category match


def main():
    # Get top story IDs
    story_ids = get_top_story_ids()

    # Store collected stories
    collected_data = []

    # Track counts per category
    category_counts = {cat: 0 for cat in CATEGORIES}

    # Loop through each category separately (for sleep control)
    for category in CATEGORIES:
        print(f"
Collecting category: {category}")

        for story_id in story_ids:
            # Stop if category limit reached
            if category_counts[category] >= MAX_PER_CATEGORY:
                break

            story = get_story_details(story_id)

            # Skip if request failed or no title
            if not story or "title" not in story:
                continue

            # Categorize story
            story_category = categorize_title(story["title"])

            # Only collect if it matches current category
            if story_category == category:
                data = {
                    "post_id": story.get("id"),
                    "title": story.get("title"),
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                collected_data.append(data)
                category_counts[category] += 1

        # Wait 2 seconds after finishing each category
        time.sleep(2)

    # Create data folder if not exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # Generate filename with current date
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    # Save to JSON file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_data, f, indent=4)

    # Print summary
    print(f"
Collected {len(collected_data)} stories.")
    print(f"Saved to {filename}")
    print(category_counts)


if __name__ == "__main__":
    main()
