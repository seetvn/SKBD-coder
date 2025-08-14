from langgraph.graph import StateGraph, END
from .nodes.interpret import interpret_node
from .nodes.plan import plan_node
from .nodes.generate import generate_node
from .nodes.writeout import writeout_node
from .util.schema import BuildState, Settings

def build_graph(settings: Settings,debug: bool = False) -> StateGraph:
    g = StateGraph(BuildState)

    # Add nodes to the graph
    g.add_node("interpret", lambda s: interpret_node(s, settings))
    g.add_node("plan",      lambda s: plan_node(s, settings))
    g.add_node("generate",  lambda s: generate_node(s, settings))
    g.add_node("writeout",  lambda s: writeout_node(s, settings))

    # Create edges between nodes
    g.set_entry_point("interpret")
    g.add_edge("interpret", "plan")
    g.add_edge("plan", "generate")
    g.add_edge("generate", "writeout")
    g.add_edge("writeout", END)

    return g.compile()