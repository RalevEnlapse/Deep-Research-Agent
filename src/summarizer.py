from base import Summarizer
from config import Config
import re

def get_client():
    import openai
    api_key = Config.get_velocity_api_key()
    if not api_key:
        return None
    return openai.OpenAI(base_url="https://chat.velocity.online/api", api_key=api_key)

class TextSummarizer(Summarizer):
    def __init__(self, depth: str = "standard"):
        self.client = get_client()
        self.depth = depth

    def summarize(self, text: str, query: str = "") -> str:
        if self.client is None:
            # Fallback to simple summarization
            sentences = re.split(r'(?<=[.!?]) +', text)
            summary_sentences = sentences[:3]  # First 3 sentences
            return ' '.join(summary_sentences)
        if len(text) < 50:
            return text
        try:
            if self.depth == "light":
                prompt = f"Summarize the following research data briefly about '{query}': {text}"
                max_tokens = 100
            elif self.depth == "standard":
                prompt = f"Summarize the following research data with key findings about '{query}': {text}"
                max_tokens = 200
            elif self.depth == "deep":
                prompt = f"Provide a detailed analysis of the following research data about '{query}', including claims, evidence, and conclusions: {text}"
                max_tokens = 500
            else:
                prompt = f"Summarize the following research data about '{query}': {text}"
                max_tokens = 150

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes research data."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            # Try with gpt-4 if gpt-3.5 fails
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that summarizes research data."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content
            except Exception as e2:
                print(f"Error in summarization: {e}, {e2}")
                # Fallback to simple summarization
                sentences = re.split(r'(?<=[.!?]) +', text)
                query_words = query.lower().split()
                relevant_sentences = [s for s in sentences if any(word in s.lower() for word in query_words)]
                if not relevant_sentences:
                    relevant_sentences = sentences
                num_sentences = 5 if self.depth == "deep" else 3
                summary_sentences = relevant_sentences[:num_sentences]
                return ' '.join(summary_sentences)