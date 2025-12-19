from ddgs import DDGS
from .base import Searcher
from typing import List, Dict, Any

class WebSearcher(Searcher):
    def search(self, query: str) -> List[Dict[str, Any]]:
        try:
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, region='en-us', max_results=5):
                    results.append({
                        'title': r['title'],
                        'link': r['href'],
                        'snippet': r['body']
                    })
            return results
        except Exception as e:
            print(f"Error in web search: {e}")
            return []