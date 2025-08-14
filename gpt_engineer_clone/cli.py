import os
from pathlib import Path
import typer
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv

from .graph import build_graph
from .util.schema import Settings

app = typer.Typer(add_completion=False)
console = Console()

@app.command("init")
def init_env():
    """Create a .env.example if missing."""
    p = Path(".env.example")
    if p.exists():
        console.print("[yellow].env.example already exists[/yellow]")
    else:
        p.write_text("OPENAI_API_KEY=\n", encoding="utf-8")
        console.print("[green]Wrote .env.example[/green]")

@app.command("run")
def run(
    prompt: str = typer.Option(..., "--prompt", "-p", help="Natural language brief"),
    out_dir: str = typer.Option("generated_project", "--out", "-o", help="Output folder"),
    model: str = typer.Option("gpt-4.1", "--model", help="LLM model"),
    temperature: float = typer.Option(0.2, "--temp", help="Sampling temperature"),
    show_steps: bool = typer.Option(True, "--show-steps/--no-show-steps"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode")
):
    """Generate a codebase from a prompt."""
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]OPENAI_API_KEY not set. Export it or create a .env[/red]")
        raise typer.Exit(1)

    settings = Settings(model=model, temperature=temperature)
    graph = build_graph(settings,debug=debug)

    state = {
        "user_prompt": prompt,
        "out_dir": out_dir,
        "meta": {"model": model}
    }

    with console.status("[bold]Running generation graph...[/bold]"):
        state = graph.invoke(state)

    if show_steps:
        console.rule("[bold cyan]Clarified Requirements")
        console.print(Panel(state.get("clarified_requirements","(none)")))

        console.rule("[bold cyan]File Plan")
        for f in state.get("file_plan", []):
            console.print(f'• [b]{f["path"]}[/b] — {f["description"]}')

        console.rule("[bold cyan]Output")
        console.print(f'Wrote {len(state.get("drafts", []))} files to [green]{Path(out_dir).resolve()}[/green]')

if __name__ == "__main__":
    app()