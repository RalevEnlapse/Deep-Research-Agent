# Deep Research Agent

A Python-based AI agent that performs deep research on topics by searching the web and local files, then summarizing the data.

## Features

- 🌐 Web search using DuckDuckGo (free)
- 📁 Local file search in .txt and .md files
- 🤖 AI-powered summarization (OpenAI-compatible API)
- 🎨 Beautiful CLI with colors and progress indicators
- 📊 Parallel search execution for faster results
- ⚙️  Interactive configuration management
- 📈 System status monitoring

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
python main.py research --no-web --paths /path/to/docs --max-results 10

# Output to file in JSON format (applies to all queries in session)
python main.py research --format json --output results.json

# Verbose mode with detailed progress
python main.py research --verbose

# Depth modes: light (brief), standard, deep (detailed)
python main.py research --depth deep --max-results 15
```

### Configuration Management
```bash
# Get configuration values
python main.py config get LOCAL_SEARCH_PATH
python main.py config get VELOCITY_API_KEY

# Set configuration values
python main.py config set LOCAL_SEARCH_PATH ./my_docs
python main.py config set VELOCITY_API_KEY your_api_key
```

### System Status
```bash
# Check system status and configuration
python main.py status
```

### Version Information
```bash
python main.py --version
```

## CLI Features

- **🎨 Rich Interface**: Colorful output with panels, progress bars, and icons
- **📊 Progress Tracking**: Real-time progress with spinners, bars, and time estimates
- **🔄 Interactive Mode**: Enter multiple queries without restarting
- **⚙️  Smart Configuration**: Environment-based config with validation
- **🚦 Status Monitoring**: Comprehensive system health checks

## Configuration

- Set `LOCAL_SEARCH_PATH` in `src/config.py` or via `.env` file.
