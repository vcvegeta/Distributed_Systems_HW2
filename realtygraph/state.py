# ============================================================
# Part 3 – Step 2: Setting Up the AgentState
# This TypedDict acts as the shared "memory" for the entire
# graph.  Every node reads from and writes to this state.
# Fields:
#   - title, content, email, strict, task  → initial inputs
#   - llm                                  → LLM instance (optional)
#   - planner_proposal                     → Planner output
#   - reviewer_feedback                    → Reviewer output
#   - turn_count                           → loop counter
# ============================================================

from __future__ import annotations

from typing import Any, Dict, TypedDict


class AgentState(TypedDict, total=False):
    """Shared state dictionary passed between all graph nodes."""
    title: str               # blog-post title supplied by the user
    content: str             # raw content / topic for the blog post
    email: str               # author email for the metadata
    strict: bool             # whether the reviewer should be strict
    task: str                # high-level task description
    llm: Any                 # LLM instance (optional, not used with mock responses)
    planner_proposal: Dict[str, Any]   # JSON proposal from the Planner
    reviewer_feedback: Dict[str, Any]  # JSON feedback from the Reviewer
    turn_count: int          # tracks iterations to prevent infinite loops


def initialize_state(
    title: str,
    content: str,
    email: str,
    task: str,
    strict: bool = False,
    llm: Any = None,
) -> AgentState:
    """Create a fresh AgentState with sensible defaults."""
    return AgentState(
        title=title,
        content=content,
        email=email,
        strict=strict,
        task=task,
        llm=llm,
        planner_proposal={},
        reviewer_feedback={},
        turn_count=0,
    )



