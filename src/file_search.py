import os
import glob
from base import Searcher
from typing import List, Dict, Any
from cache.cache import Cache
import hashlib

class FileSearcher(Searcher):
    def __init__(self):
        self.cache = Cache(".deep_research/file_index.db")

    def _get_file_hash(self, file_path: str) -> str:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    def search(self, query: str, path: str = "./data", max_results: int = 5) -> List[Dict[str, Any]]:
        results = []
        txt_files = glob.glob(os.path.join(path, "**", "*.txt"), recursive=True)
        md_files = glob.glob(os.path.join(path, "**", "*.md"), recursive=True)
        all_files = txt_files + md_files
        for file_path in all_files:
            try:
                mtime = os.path.getmtime(file_path)
                file_hash = self._get_file_hash(file_path)
                cache_key = f"file:{file_path}"
                cached = self.cache.get(cache_key)
                if cached and cached.get('hash') == file_hash:
                    content = cached['content']
                else:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.cache.set(cache_key, {'content': content, 'hash': file_hash})
                if any(word in content.lower() for word in query.lower().split()):
                    results.append({
                        'file': file_path,
                        'content': content[:500]  # First 500 chars
                    })
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        return results[:max_results]