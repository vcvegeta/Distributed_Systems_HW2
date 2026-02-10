# ============================================================
# Part 3 – Step 5: Assembling the Graph
# Wire the three nodes (supervisor, planner, reviewer)
# together using LangGraph's StateGraph.
#
# Graph structure:
#   ENTRY → supervisor → (router decides) → planner / reviewer / END
#   planner  → supervisor  (goes back so router can re-evaluate)
#   reviewer → supervisor  (goes back so router can re-evaluate)
# ============================================================

from __future__ import annotations

from langgraph.graph import StateGraph, END

from .state import AgentState
from .nodes import planner_node, reviewer_node, supervisor_node
from .router import router_logic


def build_workflow():
    """Construct and compile the Planner↔Reviewer agent graph."""

    workflow = StateGraph(AgentState)

    # Register the three nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("reviewer", reviewer_node)

    # The graph always starts at the supervisor
    workflow.set_entry_point("supervisor")

    # After the supervisor increments the turn counter, the
    # router decides what to do next
    workflow.add_conditional_edges(
        "supervisor",
        router_logic,
        {
            "planner":  "planner",
            "reviewer": "reviewer",
            "END":      END,
        },
    )

    # After the planner finishes, go back to the supervisor
    # so the router can decide whether to review or end
    workflow.add_edge("planner", "supervisor")

    # After the reviewer finishes, go back to the supervisor
    # so the router can decide whether to loop or end
    workflow.add_edge("reviewer", "supervisor")

    return workflow.compile()


