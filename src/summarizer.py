from .base import Summarizer, get_client
import re

class TextSummarizer(Summarizer):
    def __init__(self):
        self.client = get_client()

    def summarize(self, text: str) -> str:
        if self.client is None:
            # Fallback to simple summarization
            sentences = re.split(r'(?<=[.!?]) +', text)
            summary_sentences = sentences[:3]  # First 3 sentences
            return ' '.join(summary_sentences)
        if len(text) < 50:
            return text
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes research data."},
                    {"role": "user", "content": f"Summarize the following research data: {text}"}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in summarization: {e}")
            return text[:200] + "..."