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

if __name__ == "__main__":
    # For testing purposes
    test_state = {
        "user_prompt": "I want to create a simple Python script that prints 'Hello, World!'"
    }
    settings = type('Settings', (object,), {'model': 'gpt-3.5-turbo', 'temperature': 0.7})
    interpret_node(test_state, settings)
    print("Interpret node executed successfully.")
    print(f"Clarified requirements: {test_state['clarified_requirements']}")

    