# ============================================================
# Part 3 – Step 6: Running and Testing the Agent Graph
# This script builds the compiled graph, creates the initial
# state, and uses .stream() to print the output from each
# step so you can observe the Supervisor → Planner → Reviewer
# correction loop in action.
#
# No API key is required – agent responses are simulated
# to demonstrate the graph structure and routing logic.
#
# Usage:
#   python run_graph.py
# ============================================================

import json

from realtygraph.workflow import build_workflow
from realtygraph.state import initialize_state


def main():
    # ---- Step 5: Build the compiled graph ----
    graph = build_workflow()

    # ---- Step 2: Create the initial state ----
    state = initialize_state(
        title="The Future of AI in Education",
        content="Explore how artificial intelligence is transforming classrooms, personalized learning, and student outcomes.",
        email="author@example.com",
        task="Write a well-structured blog post about AI in education.",
        strict=False,       # set to True to force stricter reviews
    )

    # ---- Step 6: Stream the graph execution step by step ----
    print("=" * 60)
    print("  AGENT GRAPH – Streaming Execution")
    print("=" * 60)

    for step_output in graph.stream(state):
        # step_output is a dict like {"node_name": {state_updates}}
        for node_name, updates in step_output.items():
            print(f"\n{'─' * 50}")
            print(f"  Completed node: {node_name}")
            print(f"{'─' * 50}")

            # Display planner proposal if produced in this step
            if "planner_proposal" in updates:
                print("  Planner Proposal:")
                print(json.dumps(updates["planner_proposal"], indent=4))

            # Display reviewer feedback if produced in this step
            if "reviewer_feedback" in updates:
                print("  Reviewer Feedback:")
                print(json.dumps(updates["reviewer_feedback"], indent=4))

            # Display turn count if updated
            if "turn_count" in updates:
                print(f"  Turn count: {updates['turn_count']}")

    # ---- Print the final state summary ----
    print("\n" + "=" * 60)
    print("  FINAL STATE SUMMARY")
    print("=" * 60)

    # Re-invoke to get the final state dict
    final_state = graph.invoke(state)
    print(f"  Title   : {final_state.get('title')}")
    print(f"  Task    : {final_state.get('task')}")
    print(f"  Turns   : {final_state.get('turn_count')}")
    print(f"  Approved: {final_state.get('reviewer_feedback', {}).get('approved', 'N/A')}")
    print("\n  Final Proposal:")
    print(json.dumps(final_state.get("planner_proposal", {}), indent=4))
    print("\n  Final Feedback:")
    print(json.dumps(final_state.get("reviewer_feedback", {}), indent=4))


if __name__ == "__main__":
    main()

