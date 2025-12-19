from abc import ABC, abstractmethod
from typing import List, Dict, Any
import os
import concurrent.futures

class Searcher(ABC):
    @abstractmethod
    def search(self, query: str) -> List[Dict[str, Any]]:
        pass

class Summarizer(ABC):
    @abstractmethod
    def summarize(self, text: str, query: str = "") -> str:
        pass

class Agent:
    def __init__(self, web_searcher: Searcher, file_searcher: Searcher, summarizer: Summarizer):
        self.web_searcher = web_searcher
        self.file_searcher = file_searcher
        self.summarizer = summarizer

    def research(self, topic: str, local_path: str = ".", max_results: int = 5) -> str:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            web_future = executor.submit(self.web_searcher.search, topic, max_results) if self.web_searcher else None
            file_future = executor.submit(self.file_searcher.search, topic, local_path, max_results) if self.file_searcher else None
            
            web_results = web_future.result() if web_future else []
            file_results = file_future.result() if file_future else []
            
            print(f"Web search completed: {len(web_results)} results")
            print(f"File search completed: {len(file_results)} results")
        
        combined_text = self._combine_results(web_results, file_results)
        summary = self.summarizer.summarize(combined_text, topic)
        return summary

    def _combine_results(self, web: List[Dict], files: List[Dict]) -> str:
        text = "Web Results:\n"
        for res in web:
            text += f"- {res.get('title', '')}: {res.get('snippet', '')}\n"
        text += "\nFile Results:\n"
        for res in files:
            text += f"- {res.get('file', '')}: {res.get('content', '')}\n"
        return text