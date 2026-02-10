# ============================================================
# Part 3 – Step 4: Building the Supervisor (Router Logic)
# The routing function reads the current state and decides
# where to go next by returning a string key.
#
# Flow:
#   1. If no proposal yet            → route to "planner"
#   2. If proposal but no feedback   → route to "reviewer"
#   3. If reviewer approved          → END
#   4. If reviewer has issues AND
#      turn_count < MAX_TURNS        → route back to "planner"
#   5. Otherwise (max turns reached) → END
# ============================================================

from __future__ import annotations

from typing import Literal

from .state import AgentState
from .nodes import MAX_TURNS


def router_logic(
    state: AgentState,
) -> Literal["planner", "reviewer", "END"]:
    """Decide the next node based on the current state."""

    proposal = state.get("planner_proposal", {})
    feedback = state.get("reviewer_feedback", {})
    turn     = state.get("turn_count", 0)

    # Step 1 – No proposal yet → ask the Planner to create one
    if not proposal:
        return "planner"

    # Step 2 – Proposal exists but no review yet → send to Reviewer
    if not feedback:
        return "reviewer"

    # Step 3 – Reviewer approved the proposal → we are done
    if feedback.get("approved", False):
        print("[Router] Proposal approved – ending workflow.")
        return "END"

    # Step 4 – Reviewer flagged issues; loop back if within budget
    if turn < MAX_TURNS:
        print(f"[Router] Issues found, sending back to Planner (turn {turn}/{MAX_TURNS}).")
        return "planner"

    # Step 5 – Maximum turns reached → stop to avoid infinite loop
    print(f"[Router] Max turns ({MAX_TURNS}) reached – ending workflow.")
    return "END"


