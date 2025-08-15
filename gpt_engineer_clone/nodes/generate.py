from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pathlib import Path


def generate_node(state, settings, debug: bool = False):
    """
    Generate drafts based on the clarified requirements and file plan.
    """

    print(
        f"[DEBUG] Running generate_node with state: {state}") if debug else None
    reqs = state["clarified_requirements"]
    file_plan_lines = [
        f'{f["path"]} — {f["description"]}' for f in state["file_plan"]]
    file_plan_text = "\n".join(file_plan_lines)

    drafts = []
    llm = ChatOpenAI(model=settings.model, temperature=settings.temperature)

    template_text = Path(__file__).resolve().parents[1].joinpath(
        "prompts/generate.md").read_text(encoding="utf-8")
    for item in state["file_plan"]:
        path = item["path"]
        prompt = PromptTemplate.from_template(template_text).format(
            requirements=reqs, file_plan=file_plan_text, path=path
        )
        resp = llm.invoke(prompt)
        # TODO: do the path handling here instead
        drafts.append({"path": path, "content": resp.content})
    state["drafts"] = drafts
    return state

if __name__ == "__main__":
    # For testing purposes
    test_state = {
        "clarified_requirements": "Create a simple Python script that prints 'Hello, World!'",
        "file_plan": [
            {"path": "src/main.py", "description": "Main script"},
            {"path": "README.md", "description": "Project description"}
        ]
    }
    settings = type('Settings', (object,), {'model': 'gpt-3.5-turbo', 'temperature': 0.7})
    generate_node(test_state, settings, debug=True)
    print("Generate node executed successfully.")
