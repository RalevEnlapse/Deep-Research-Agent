# Deep Research Agent

A Python-based AI agent that performs deep research on topics by searching the web and local files, then summarizing the data.

## Features

- Web search using Google Custom Search API (free tier available)
- Local file search in .txt and .md files
- Simple text summarization
- Modular and abstract design

## Installation

1. Install dependencies: `pip install -r requirements.txt`
2. Set up Google Custom Search API:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Enable Custom Search API
   - Create credentials (API key)
   - Create a Custom Search Engine at [CSE](https://cse.google.com/)
   - Set environment variables: `GOOGLE_API_KEY` and `GOOGLE_CSE_ID` in a `.env` file
3. Run the agent: `python -m src.main`

## Usage

Enter a research topic when prompted. The agent will search the web and local files, then provide a summary.

## Configuration

- Set `LOCAL_SEARCH_PATH` in `src/config.py` or via `.env` file.
