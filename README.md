# GPT‑Engineer Clone (CLI)

A minimal, real implementation of a CLI that turns a natural‑language brief into a runnable codebase.
Built with **LangChain + LangGraph** for orchestration, **Typer** for the CLI, and standard library
(`pathlib`, `os`) for filesystem output.

## Features
- Interpret user prompt → clarify requirements
- Plan files and folder structure
- Generate per‑file code
- Write to disk in a project‑ready folder
- Show intermediate steps with Rich

## Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e .
```

Or without editable install:

```bash
pip install .
```

## Environment

Put your key in `.env` or export it:

```bash
cp .env.example .env
# edit .env to add your key
export OPENAI_API_KEY=sk-...
```

## Usage

```bash
gptx run -p "An api for a TODO list in Flask in Python" -o hn_cli
```

Options:

- `--prompt`/`-p`: the natural language brief (required)
- `--out`/`-o`: output folder (default: `generated_project`)
- `--model`: OpenAI model (default: `gpt-4o-mini`)
- `--temp`: sampling temperature (default: `0.2`)
- `--show-steps/--no-show-steps`: toggle printing intermediate results
- `--debug`: for debugging/still being implemented

## Development notes

- Uses `langchain_openai.ChatOpenAI`. Any model string supported by your account can be passed.
- Graph steps: `interpret → plan → generate → writeout`.
- Extend by adding nodes (e.g., tests/validate) and edges in `graph.py`.
- Add retries/guardrails if a file comes back empty.