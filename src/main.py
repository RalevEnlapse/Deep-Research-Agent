import typer
from typing import Optional, List
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from base import Agent
from web_search import WebSearcher
from file_search import FileSearcher
from summarizer import TextSummarizer
from config import Config

app = typer.Typer(
    help="🔍 Deep Research Agent - Search web and local files for comprehensive insights.",
    add_completion=False,
)
console = Console()

@app.callback()
def callback(
    version: bool = typer.Option(False, "--version", "-v", help="Show version and exit.")
):
    """
    Deep Research Agent CLI.

    Perform deep research on topics by searching the web and local files.
    """
    if version:
        console.print("[bold blue]Deep Research Agent[/bold blue] v1.0.0")
        console.print("Built with ❤️ using Python and AI")
        raise typer.Exit()

    # Welcome message
    welcome_text = Text("🔍 Deep Research Agent", style="bold magenta")
    welcome_panel = Panel(
        "[bold green]Welcome![/bold green]\n\n"
        "Search the web and your local files for comprehensive insights.\n"
        "Use [bold cyan]research[/bold cyan] to start exploring topics interactively.",
        title=welcome_text,
        border_style="blue"
    )
    console.print(welcome_panel)

@app.command()
def research(
    web: bool = typer.Option(True, help="🌐 Enable web search."),
    local: bool = typer.Option(True, help="📁 Enable local file search."),
    paths: List[Path] = typer.Option([Path("./data")], help="📂 Paths to search locally."),
    max_results: int = typer.Option(5, help="🔢 Maximum results per source."),
    depth: str = typer.Option("standard", help="📊 Depth mode: light, standard, or deep."),
    format: str = typer.Option("md", help="📄 Output format: md or json."),
    output: Optional[Path] = typer.Option(None, help="💾 Output file path."),
    verbose: bool = typer.Option(False, help="📢 Enable verbose output."),
):
    """
    🔬 Perform deep research on queries interactively.

    Enter your research queries one by one. Type 'quit' to exit.
    """
    console.print("\n[bold cyan]🚀 Starting Interactive Research Mode[/bold cyan]")
    console.print("[dim]Type your queries below. Enter 'quit' to exit.[/dim]\n")
    
    while True:
        try:
            query = Prompt.ask("[bold green]Query[/bold green]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[red]👋 Exiting...[/red]")
            break
        
        if query.lower() == "quit":
            console.print("[yellow]👋 Goodbye![/yellow]")
            break
        
        if not query:
            console.print("[red]❌ Please enter a valid query.[/red]")
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
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console,
            disable=not verbose,
        ) as progress:
            init_task = progress.add_task("🔧 Initializing components...", total=None)
            
            # Initialize components
            web_searcher = WebSearcher() if web else None
            file_searcher = FileSearcher() if local else None
            summarizer = TextSummarizer(depth=depth)

            agent = Agent(web_searcher, file_searcher, summarizer)
            
            progress.update(init_task, description="✅ Components ready")
            progress.remove_task(init_task)

            search_task = progress.add_task("🔍 Searching sources...", total=100)
            
            # Perform research
            try:
                local_path = str(paths[0]) if paths else Config.LOCAL_SEARCH_PATH
                summary = agent.research(query, local_path, adjusted_max_results)
                progress.update(search_task, completed=100)
            except KeyboardInterrupt:
                console.print("\n[red]⏹️  Research interrupted by user.[/red]")
                continue

            progress.update(search_task, description="📝 Formatting results...")

            # Format output
            if format == "md":
                output_text = f"# 🔍 Research Summary: {query}\n\n{summary}"
                if output:
                    output.write_text(output_text)
                    console.print(f"💾 [green]Output saved to {output}[/green]")
                else:
                    console.print(Markdown(output_text))
            elif format == "json":
                import json
                data = {"query": query, "summary": summary}
                output_text = json.dumps(data, indent=2)
                if output:
                    output.write_text(output_text)
                    console.print(f"💾 [green]Output saved to {output}[/green]")
                else:
                    console.print(output_text)
            else:
                console.print("[red]❌ Unsupported format.[/red]")

            progress.remove_task(search_task)
        
        console.print("\n" + "═" * 60)
        console.print("[dim]Ready for next query...[/dim]\n")

@app.command()
def config(
    action: str = typer.Argument(..., help="📋 Action: get or set."),
    key: str = typer.Argument(..., help="🔑 Config key."),
    value: Optional[str] = typer.Argument(None, help="✏️  Value for set action."),
):
    """
    ⚙️  Manage configuration settings.

    Available keys: LOCAL_SEARCH_PATH, VELOCITY_API_KEY
    """
    env_file = Path(".env")
    
    if action == "get":
        console.print(f"\n[bold blue]📋 Configuration Status[/bold blue]\n")
        if key == "LOCAL_SEARCH_PATH":
            path = Config.LOCAL_SEARCH_PATH
            console.print(f"📂 [cyan]LOCAL_SEARCH_PATH:[/cyan] {path}")
            if Path(path).exists():
                console.print(f"   [green]✓ Path exists[/green]")
            else:
                console.print(f"   [yellow]⚠️  Path does not exist[/yellow]")
        elif key == "VELOCITY_API_KEY":
            api_key = Config.get_velocity_api_key()
            if api_key:
                masked = "*" * (len(api_key) - 4) + api_key[-4:] if len(api_key) > 4 else "*" * len(api_key)
                console.print(f"🔑 [cyan]VELOCITY_API_KEY:[/cyan] {masked}")
                console.print(f"   [green]✓ API key configured[/green]")
            else:
                console.print(f"🔑 [cyan]VELOCITY_API_KEY:[/cyan] [red]Not set[/red]")
                console.print(f"   [yellow]⚠️  AI summarization will use fallback[/yellow]")
        else:
            console.print(f"[red]❌ Unknown key: {key}[/red]")
            console.print("[dim]Available keys: LOCAL_SEARCH_PATH, VELOCITY_API_KEY[/dim]")
    
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
            console.print(f"[green]✅ Set {key} to {value}[/green]")
            
            if key == "LOCAL_SEARCH_PATH":
                console.print(f"[dim]Restart the application for changes to take effect.[/dim]")
        else:
            console.print(f"[red]❌ Unknown key: {key}[/red]")
            console.print("[dim]Available keys: LOCAL_SEARCH_PATH, VELOCITY_API_KEY[/dim]")
    else:
        console.print("[red]❌ Invalid action. Use 'get' or 'set'.[/red]")

@app.command()
def status():
    """
    📊 Show system status and configuration.
    """
    status_panel = Panel(
        f"[bold green]System Status[/bold green]\n\n"
        f"🔍 [cyan]Web Search:[/cyan] {'✅ Enabled' if True else '❌ Disabled'}\n"
        f"📁 [cyan]File Search:[/cyan] {'✅ Enabled' if True else '❌ Disabled'}\n"
        f"🤖 [cyan]AI Summarization:[/cyan] {'✅ Available' if Config.get_velocity_api_key() else '⚠️  Fallback mode'}\n\n"
        f"📂 [cyan]Local Search Path:[/cyan] {Config.LOCAL_SEARCH_PATH}\n"
        f"⚙️  [cyan]Cache Location:[/cyan] .deep_research/cache.db",
        title="📊 Deep Research Agent Status",
        border_style="green"
    )
    console.print(status_panel)

if __name__ == "__main__":
    app()