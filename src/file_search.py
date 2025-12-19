import os
import glob
from .base import Searcher
from typing import List, Dict, Any

class FileSearcher(Searcher):
    def search(self, query: str, path: str = "./data") -> List[Dict[str, Any]]:
        results = []
        txt_files = glob.glob(os.path.join(path, "**", "*.txt"), recursive=True)
        md_files = glob.glob(os.path.join(path, "**", "*.md"), recursive=True)
        all_files = txt_files + md_files
        for file_path in all_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if any(word in content.lower() for word in query.lower().split()):
                        results.append({
                            'file': file_path,
                            'content': content[:500]  # First 500 chars
                        })
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        return results