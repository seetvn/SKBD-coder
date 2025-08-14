from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pathlib import Path

def _parse_bullets(text: str):

    """Parse bullet points from a text string into a structured list."""

    plans = []
    for line in text.splitlines():
        line = line.strip("-• ").strip()
        if " — " in line:
            path, desc = line.split(" — ", 1)
            if path and desc:
                plans.append({"path": path.strip(), "description": desc.strip()})
    return plans

def plan_node(state, settings,debug: bool = False):

    """
    Create a file plan based on the clarified requirements.
    """

    print(f"[DEBUG] Running plan_node with state: {state}") if debug else None
    reqs = state["clarified_requirements"]
    tmpl_text = Path(__file__).resolve().parents[1].joinpath("prompts/plan.md").read_text(encoding="utf-8")
    prompt = PromptTemplate.from_template(tmpl_text).format(requirements=reqs)
    llm = ChatOpenAI(model=settings.model, temperature=0.1)
    resp = llm.invoke(prompt)
    state["file_plan"] = _parse_bullets(resp.content)
    return state