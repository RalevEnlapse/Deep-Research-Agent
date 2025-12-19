from .base import Agent
from .web_search import WebSearcher
from .file_search import FileSearcher
from .summarizer import TextSummarizer
from .config import Config

def main():
    web_searcher = WebSearcher()
    file_searcher = FileSearcher()
    summarizer = TextSummarizer()
    agent = Agent(web_searcher, file_searcher, summarizer)

    topic = input("Enter research topic: ")
    summary = agent.research(topic, Config.LOCAL_SEARCH_PATH)
    print("Research Summary:")
    print(summary)

if __name__ == "__main__":
    main()