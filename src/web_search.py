from ddgs import DDGS
from base import Searcher
from typing import List, Dict, Any
from cache.cache import Cache

class WebSearcher(Searcher):
    def __init__(self):
        self.cache = Cache()

    def _rank_source(self, url: str) -> int:
        # Simple ranking: higher for reputable domains
        reputable = ['wikipedia.org', 'stackoverflow.com', 'github.com', 'arxiv.org', 'ieee.org']
        for domain in reputable:
            if domain in url:
                return 10
        if 'edu' in url or 'ac.' in url:
            return 8
        if 'org' in url:
            return 6
        return 5  # Default

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        # Check cache first
        cached = self.cache.get(query, {"region": "en-us", "max_results": max_results})
        if cached:
            return cached

        try:
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, region='en-us', max_results=max_results * 2):  # Fetch more for ranking
                    results.append({
                        'title': r['title'],
                        'link': r['href'],
                        'snippet': r['body'],
                        'rank': self._rank_source(r['href'])
                    })
            # Sort by rank and take top max_results
            results.sort(key=lambda x: x['rank'], reverse=True)
            top_results = results[:max_results]
            # Remove rank from output
            for r in top_results:
                del r['rank']
            # Cache the results
            self.cache.set(query, top_results, {"region": "en-us", "max_results": max_results})
            return top_results
        except Exception as e:
            print(f"Error in web search: {e}")
            return []