from abc import ABC, abstractmethod
from typing import List, Dict, Any
import os
from .config import Config

class Searcher(ABC):
    @abstractmethod
    def search(self, query: str) -> List[Dict[str, Any]]:
        pass

class Summarizer(ABC):
    @abstractmethod
    def summarize(self, text: str) -> str:
        pass

def get_client():
    import openai
    api_key = Config.get_velocity_api_key()
    if not api_key:
        return None
    return openai.OpenAI(base_url="https://chat.velocity.online/api", api_key=api_key)

class Agent:
    def __init__(self, web_searcher: Searcher, file_searcher: Searcher, summarizer: Summarizer):
        self.web_searcher = web_searcher
        self.file_searcher = file_searcher
        self.summarizer = summarizer

    def research(self, topic: str, local_path: str = ".") -> str:
        web_results = self.web_searcher.search(topic)
        file_results = self.file_searcher.search(topic, local_path)
        combined_text = self._combine_results(web_results, file_results)
        summary = self.summarizer.summarize(combined_text)
        return summary

    def _combine_results(self, web: List[Dict], files: List[Dict]) -> str:
        text = "Web Results:\n"
        for res in web:
            text += f"- {res.get('title', '')}: {res.get('snippet', '')}\n"
        text += "\nFile Results:\n"
        for res in files:
            text += f"- {res.get('file', '')}: {res.get('content', '')}\n"
        return text