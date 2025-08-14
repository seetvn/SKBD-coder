from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pathlib import Path


def interpret_node(state, settings):
    """
    Interpret the user's prompt to clarify requirements.
    """

    brief = state["user_prompt"]
    tmpl_text = Path(__file__).resolve().parents[1].joinpath(
        "prompts/interpret.md").read_text(encoding="utf-8")
    prompt = PromptTemplate.from_template(tmpl_text).format(brief=brief)
    llm = ChatOpenAI(model=settings.model, temperature=settings.temperature)
    resp = llm.invoke(prompt)
    state["clarified_requirements"] = resp.content.strip()
    return state
