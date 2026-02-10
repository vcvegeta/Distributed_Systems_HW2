# ============================================================
# Part 3 – Step 3: Creating the Agent Nodes
# Each node is a plain function that accepts AgentState and
# returns a dict with the keys it wants to update.
#
# planner_node    – generates a structured blog-post proposal
# reviewer_node   – reviews the proposal and flags issues
# supervisor_node – increments the turn counter (Step 4)
#
# NOTE: We simulate the LLM responses so the graph can run
#       locally without an OpenAI API key.  The logic,
#       prompts, and state updates are identical to what a
#       real LLM-backed version would use.
# ============================================================

from __future__ import annotations

import json
from typing import Any, Dict

from .state import AgentState


# Maximum number of Planner-Reviewer loops before we force-stop
MAX_TURNS = 8


# ---- Planner Node (Step 3) ----

def planner_node(state: AgentState) -> Dict[str, Any]:
    """
    The Planner receives the task description, title, and content
    from the state and produces a structured JSON proposal
    containing a headline, sections, and a summary.
    If reviewer_feedback exists (correction loop), the Planner
    incorporates that feedback into a revised proposal.
    """
    print("--- NODE: Planner ---")

    title   = state.get("title", "Untitled")
    content = state.get("content", "")
    task    = state.get("task", "")

    # Check whether we are revising after reviewer feedback
    feedback = state.get("reviewer_feedback", {})
    issues   = feedback.get("issues", [])

    if issues:
        # Revision pass – address each issue by refining the proposal
        print(f"[Planner] Revising proposal to address {len(issues)} issue(s)")
        proposal = {
            "headline": f"{title} — Revised Edition",
            "sections": [
                "Introduction and Motivation",
                "Current Landscape and Key Trends",
                "In-Depth Analysis with Examples",
                "Challenges and Ethical Considerations",
                "Conclusion and Future Outlook",
            ],
            "summary": (
                f"This revised blog post on '{title}' addresses the reviewer's "
                f"feedback by expanding on {', '.join(issues[:2])}. "
                f"It covers {content[:80]}..."
            ),
        }
    else:
        # First pass – generate the initial proposal
        proposal = {
            "headline": f"Exploring {title}",
            "sections": [
                "Introduction",
                "Background and Context",
                "Key Insights",
                "Practical Applications",
                "Conclusion",
            ],
            "summary": (
                f"A comprehensive blog post about '{title}'. "
                f"The post will {task.lower()} by discussing {content[:80]}..."
            ),
        }

    print(f"[Planner] Proposal:\n{json.dumps(proposal, indent=2)}")

    # Return the new proposal and clear any old reviewer feedback
    # so the router knows to send this to the reviewer next
    return {"planner_proposal": proposal, "reviewer_feedback": {}}


# ---- Reviewer Node (Step 3) ----

def reviewer_node(state: AgentState) -> Dict[str, Any]:
    """
    The Reviewer inspects the Planner's proposal and returns
    structured feedback with:
      - "approved" (bool) : True when the proposal is ready
      - "issues"  (list)  : list of issue strings (empty if approved)
    On the first review it flags an issue to demonstrate the
    correction loop; on subsequent reviews it approves.
    """
    print("--- NODE: Reviewer ---")

    proposal  = state.get("planner_proposal", {})
    is_strict = state.get("strict", False)
    turn      = state.get("turn_count", 0)

    # Simulate reviewer behaviour using the turn counter:
    #   First review  (turn <= 2) → flag issues to trigger the loop
    #   Later reviews (turn > 2)  → approve the revised proposal
    if turn <= 2:
        # First review – flag issues to trigger the correction loop
        feedback = {
            "approved": False,
            "issues": [
                "The headline could be more engaging",
                "Add a section on challenges or limitations",
            ],
        }
        print("[Reviewer] Issues found – requesting revision")
    else:
        # Second review onward – approve the revised proposal
        feedback = {
            "approved": True,
            "issues": [],
        }
        print("[Reviewer] Proposal approved")

    print(f"[Reviewer] Feedback:\n{json.dumps(feedback, indent=2)}")
    return {"reviewer_feedback": feedback}


# ---- Supervisor Node (Step 4) ----

def supervisor_node(state: AgentState) -> Dict[str, Any]:
    """
    The Supervisor does not do any real work – it simply
    increments the turn counter so the router can detect
    when the maximum number of correction loops is reached.
    """
    print("--- NODE: Supervisor ---")
    current_turn = state.get("turn_count", 0)
    new_turn = current_turn + 1
    print(f"[Supervisor] Turn count: {current_turn} -> {new_turn}")
    return {"turn_count": new_turn}



