import wikipediaapi
from text_processing import get_word_frequency
from collections import Counter
import asyncio

fetched_articles_cache = {}

wiki_wiki = wikipediaapi.Wikipedia(
    user_agent='wikipedia_word_frequency_dictionary (ainur@gmail.com) Python/3.9.6 wikipediaapi/0.5.4',
    language='en'
)

SEM = asyncio.Semaphore(5)

async def fetch_wikipedia_article(title: str):
    """Asynchronously fetch Wikipedia article content, respecting rate limits."""
    async with SEM:
        await asyncio.sleep(1)
        page = wiki_wiki.page(title)
        if not page.exists():
            print(f"Article '{title}' does not exist.")
            return {"error": f"Article '{title}' does not exist on Wikipedia."}
        links = list(page.links.keys())  # Get all linked articles
        print(f"Found {len(links)} links in article: {title}")
        return {
            "title": page.title,
            "content": page.text,
            "links": links,
        }

async def fetch_wikipedia_article_with_depth(title: str, depth: int, visited: set):
    """
    Recursively fetch Wikipedia articles and count words up to the given depth.
    - depth = 0 → Fetch only the original article
    - depth = 1 → Fetch original + its direct links
    - depth = 2 → Fetch original + its links + links of links
    """
    if title in visited or depth < 0:
        return Counter()  # Skip already visited articles
    visited.add(title)
    if title in fetched_articles_cache:
        return fetched_articles_cache[title]
    article_data = await fetch_wikipedia_article(title)
    if "error" in article_data:
        return Counter()
    word_counts = get_word_frequency(article_data["content"])
    all_word_counts = Counter(word_counts)
    total_words = sum(all_word_counts.values())
    print(f"Total words in article '{title}': {total_words}")
    if depth > 0:
        links_to_traverse = article_data["links"][:5]
        tasks = [fetch_wikipedia_article_with_depth(link, depth - 1, visited) for link in links_to_traverse]
        sub_results = await asyncio.gather(*tasks)
        for result in sub_results:
            all_word_counts.update(result)
    total_words_after = sum(all_word_counts.values())
    fetched_articles_cache[title] = all_word_counts
    return all_word_counts