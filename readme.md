# Deep Research Agent

A Python-based AI agent that performs deep research on topics by searching the web and local files, then summarizing the data.

## Features

- Web search using DuckDuckGo (free)
- Local file search in .txt and .md files
- AI-powered summarization (OpenAI-compatible API)
- Clean CLI with subcommands and formatting options
- Modular and abstract design
- Parallel search execution for faster results

## Installation

### From Source
1. Clone the repository
2. Install with pip: `pip install .`
3. (Optional) Set `VELOCITY_API_KEY` for AI summarization in `.env` file

### Direct Usage
```bash
pip install -r requirements.txt
cd src
python main.py research
# Then enter queries interactively
```

## Usage

### Basic Research
```bash
cd src
python main.py research
# Then enter queries interactively, type 'quit' to exit
```

### Advanced Options
```bash
# Disable web search, search specific paths
deep-research research --no-web --paths /path/to/docs --max-results 10

# Output to file in JSON format (applies to all queries in session)
deep-research research --format json --output results.json

# Verbose mode with progress
deep-research research --verbose

# Depth modes: light (brief), standard, deep (detailed)
deep-research research --depth deep --max-results 15
```

### Configuration
```bash
# Get config values
deep-research config get LOCAL_SEARCH_PATH

# Set config values
deep-research config set LOCAL_SEARCH_PATH ./my_docs
deep-research config set VELOCITY_API_KEY your_api_key
```

### Help
```bash
deep-research --help
deep-research research --help
```

## Configuration

- Set `LOCAL_SEARCH_PATH` in `src/config.py` or via `.env` file.
