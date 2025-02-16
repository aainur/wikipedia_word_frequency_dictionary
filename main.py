from fastapi import FastAPI
from pydantic import BaseModel
from wikipedia_scraper import fetch_wikipedia_article
from text_processing import get_word_frequency
from wikipedia_scraper import fetch_wikipedia_article_with_depth
from collections import Counter

app = FastAPI(
    title="Wikipedia Word-Frequency API",
    description="An API that generates word-frequency dictionaries.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

class KeywordRequest(BaseModel):
    article: str
    depth: int
    ignore_list: list[str]
    percentile: int

@app.get("/", summary="Root Endpoint")
def root():
    return {"message": "Welcome to Wikipedia Word-Frequency API! Go to /docs for API documentation."}

def filter_words_by_percentile(word_counts: Counter, percentile: int):
    """
    Filters words that fall below the given percentile threshold.
    """
    total_words = sum(word_counts.values())
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    cumulative_count = 0
    threshold_count = total_words * (percentile / 100)
    filtered_counts = Counter()
    for word, count in sorted_words:
        cumulative_count += count
        if cumulative_count >= threshold_count:
            break
        filtered_counts[word] = count
    return filtered_counts

@app.get("/word-frequency", summary="Fetch word frequency from a Wikipedia article")
async def get_word_frequency_api(article: str, depth: int = 0):
    """
    Retrieves the word frequency dictionary for a given Wikipedia article up to the specified depth.
    """
    visited = set()
    word_counts = await fetch_wikipedia_article_with_depth(article, depth, visited)
    if not word_counts:
        return {"error": f"Article '{article}' does not exist on Wikipedia."}
    total_words = sum(word_counts.values())
    word_percentages = {word: round((count / total_words) * 100, 2) for word, count in word_counts.items()}
    return {
        "title": article,
        "word_counts": dict(word_counts),
        "word_percentages": word_percentages
    }

@app.post("/keywords", summary="Fetch filtered word frequency from a Wikipedia article")
async def get_filtered_word_frequency(request: KeywordRequest):
    """
    Retrieves the word frequency dictionary with filtering based on an ignore list and percentile threshold.
    """
    visited = set()
    word_counts = await fetch_wikipedia_article_with_depth(request.article, request.depth, visited)
    for word in request.ignore_list:
        word_counts.pop(word, None)
    filtered_counts = filter_words_by_percentile(word_counts, request.percentile)
    total_words = sum(filtered_counts.values())
    word_percentages = {word: (count / total_words) * 100 for word, count in filtered_counts.items()}
    return {
        "title": request.article,
        "filtered_word_counts": dict(filtered_counts),
        "word_percentages": word_percentages
    }
