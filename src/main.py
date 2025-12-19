import typer
from typing import Optional, List
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from base import Agent
from web_search import WebSearcher
from file_search import FileSearcher
from summarizer import TextSummarizer
from config import Config

app = typer.Typer(help="Deep Research Agent - Search web and local files for comprehensive insights.")
console = Console()

@app.callback()
def callback():
    """
    Deep Research Agent CLI.

    Perform deep research on topics by searching the web and local files.
    """
    pass

@app.command()
def research(
    web: bool = typer.Option(True, help="Enable web search."),
    local: bool = typer.Option(True, help="Enable local file search."),
    paths: List[Path] = typer.Option([Path("./data")], help="Paths to search locally."),
    max_results: int = typer.Option(5, help="Maximum results per source."),
    depth: str = typer.Option("standard", help="Depth mode: light, standard, or deep."),
    format: str = typer.Option("md", help="Output format: md or json."),
    output: Optional[Path] = typer.Option(None, help="Output file path."),
    verbose: bool = typer.Option(False, help="Enable verbose output."),
):
    """
    Perform deep research on queries interactively.
    """
    console.print("[bold green]Deep Research Agent[/bold green]")
    console.print("Enter your research query (or 'quit' to exit):")
    
    while True:
        try:
            query = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[red]Exiting...[/red]")
            break
        
        if query.lower() == "quit":
            console.print("[yellow]Goodbye![/yellow]")
            break
        
        if not query:
            console.print("[red]Please enter a valid query.[/red]")
            continue
        
        # Adjust max_results based on depth
        adjusted_max_results = max_results
        if depth == "light":
            adjusted_max_results = min(max_results, 3)
        elif depth == "deep":
            adjusted_max_results = max(max_results, 10)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            disable=not verbose,
        ) as progress:
            task = progress.add_task("Initializing...", total=None)

            # Initialize components
            web_searcher = WebSearcher() if web else None
            file_searcher = FileSearcher() if local else None
            summarizer = TextSummarizer(depth=depth)

            agent = Agent(web_searcher, file_searcher, summarizer)

            progress.update(task, description="Searching...")

            # Perform research
            try:
                local_path = str(paths[0]) if paths else Config.LOCAL_SEARCH_PATH
                summary = agent.research(query, local_path, adjusted_max_results)
            except KeyboardInterrupt:
                console.print("\n[red]Research interrupted by user.[/red]")
                continue

            progress.update(task, description="Formatting output...")

            # Format output
            if format == "md":
                output_text = f"# Research Summary: {query}\n\n{summary}"
                if output:
                    output.write_text(output_text)
                    console.print(f"Output saved to {output}")
                else:
                    console.print(Markdown(output_text))
            elif format == "json":
                import json
                data = {"query": query, "summary": summary}
                output_text = json.dumps(data, indent=2)
                if output:
                    output.write_text(output_text)
                    console.print(f"Output saved to {output}")
                else:
                    console.print(output_text)
            else:
                console.print("Unsupported format.")

            progress.update(task, description="Done.")
        
        console.print("\n" + "="*50)
        console.print("Enter another research query (or 'quit' to exit):")

@app.command()
def config(
    action: str = typer.Argument(..., help="Action: get or set."),
    key: str = typer.Argument(..., help="Config key."),
    value: Optional[str] = typer.Argument(None, help="Value for set action."),
):
    """
    Manage configuration.
    """
    env_file = Path(".env")
    if action == "get":
        if key == "LOCAL_SEARCH_PATH":
            console.print(f"LOCAL_SEARCH_PATH: {Config.LOCAL_SEARCH_PATH}")
        elif key == "VELOCITY_API_KEY":
            api_key = Config.get_velocity_api_key()
            console.print(f"VELOCITY_API_KEY: {'*' * len(api_key) if api_key else 'Not set'}")
        else:
            console.print(f"Unknown key: {key}")
    elif action == "set":
        if key in ["LOCAL_SEARCH_PATH", "VELOCITY_API_KEY"]:
            if env_file.exists():
                lines = env_file.read_text().splitlines()
            else:
                lines = []
            # Remove existing key
            lines = [line for line in lines if not line.startswith(f"{key}=")]
            lines.append(f"{key}={value}")
            env_file.write_text("\n".join(lines))
            console.print(f"Set {key} to {value}")
        else:
            console.print(f"Unknown key: {key}")
    else:
        console.print("Invalid action. Use 'get' or 'set'.")

if __name__ == "__main__":
    app()