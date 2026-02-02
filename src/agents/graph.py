"""
LangGraph Orchestration - The Refactoring Swarm Graph
"""
import os
import glob
from typing import Literal

try:
    from langgraph.graph import StateGraph, END
except Exception:  # pragma: no cover - fallback when langgraph deps are unavailable
    StateGraph = None
    END = None

from .state import SwarmState
from .auditor import auditor_node
from .fixer import fixer_node
from .judge import judge_node


def initialize_state(target_dir: str, max_retries: int = 3) -> SwarmState:
    """
    Initialize the swarm state with files from target directory.
    """
    # Find all Python files in target directory (excluding test files)
    pattern = os.path.join(target_dir, "**", "*.py")
    all_files = glob.glob(pattern, recursive=True)
    
    # Filter out test files
    source_files = [f for f in all_files if not os.path.basename(f).startswith("test_")]
    
    return SwarmState(
        target_dir=target_dir,
        files=source_files,
        current_file=None,
        original_code=None,
        audit_report=None,
        refactoring_plan=None,
        fixed_code=None,
        test_results=None,
        test_passed=False,
        error_logs=None,
        retry_count=0,
        max_retries=max_retries,
        completed_files=[],
        failed_files=[],
        messages=[]
    )


def select_next_file(state: SwarmState) -> SwarmState:
    """
    Select the next file to process from the queue.
    """
    if state["files"]:
        state["current_file"] = state["files"].pop(0)
        state["retry_count"] = 0
        state["test_passed"] = False
        state["error_logs"] = None
        print(f"\n📁 ORCHESTRATOR: Selected file {state['current_file']}")
    else:
        state["current_file"] = None
        print(f"\n📁 ORCHESTRATOR: No more files to process")
    
    return state


def handle_result(state: SwarmState) -> SwarmState:
    """
    Handle the result after Judge evaluation.
    """
    if state["test_passed"]:
        # Success - add to completed
        if state["current_file"]:
            state["completed_files"].append(state["current_file"])
        if state["current_file"]:
            print(f"✅ ORCHESTRATOR: {state['current_file']} completed successfully!")
    else:
        # Check if we should retry
        if state["retry_count"] < state["max_retries"]:
            state["retry_count"] += 1
            print(f"🔄 ORCHESTRATOR: Retry {state['retry_count']}/{state['max_retries']}")
        else:
            # Max retries reached - mark as failed
            if state["current_file"] and state["current_file"] not in state["failed_files"]:
                state["failed_files"].append(state["current_file"])
            if state["current_file"]:
                print(f"❌ ORCHESTRATOR: {state['current_file']} failed after {state['max_retries']} attempts")
    
    return state


def should_continue(state: SwarmState) -> Literal["select_file", "retry_fix", "end"]:
    """
    Routing function to determine next step after handling result.
    """
    if state["test_passed"]:
        # Tests passed - check if more files
        if state["files"]:
            return "select_file"
        else:
            return "end"
    else:
        # Tests failed - check if we can still retry
        # retry_count is incremented AFTER handle_result, so we check if it's still under max
        if state["retry_count"] < state["max_retries"]:
            return "retry_fix"
        else:
            # Max retries exhausted - add to failed and move on
            if state["current_file"] and state["current_file"] not in state["failed_files"]:
                state["failed_files"].append(state["current_file"])
                print(f"❌ ORCHESTRATOR: {state['current_file']} failed after {state['max_retries']} attempts")
            if state["files"]:
                return "select_file"
            else:
                return "end"


def has_file(state: SwarmState) -> Literal["process", "end"]:
    """
    Check if there's a file to process.
    """
    if state["current_file"]:
        return "process"
    else:
        return "end"


def build_graph() -> StateGraph:
    """
    Build the LangGraph workflow for the Refactoring Swarm.
    
    Graph Structure:
    
    START
      │
      ▼
    select_file ──────────────────────┐
      │                               │
      ▼ (has file)                    │ (no file)
    auditor                           │
      │                               │
      ▼                               │
    fixer ◄───────────────────┐       │
      │                       │       │
      ▼                       │       │
    judge                     │       │
      │                       │       │
      ▼                       │       │
    handle_result             │       │
      │                       │       │
      ├─── (retry) ───────────┘       │
      │                               │
      ├─── (next file) ───► select_file
      │                               │
      └─── (done) ────────────────────┴──► END
    """
    
    if StateGraph is None:
        raise RuntimeError("LangGraph is unavailable. Use the fallback runner.")

    # Create the graph
    workflow = StateGraph(SwarmState)
    
    # Add nodes
    workflow.add_node("select_file", select_next_file)
    workflow.add_node("auditor", auditor_node)
    workflow.add_node("fixer", fixer_node)
    workflow.add_node("judge", judge_node)
    workflow.add_node("handle_result", handle_result)
    
    # Set entry point
    workflow.set_entry_point("select_file")
    
    # Add edges
    workflow.add_conditional_edges(
        "select_file",
        has_file,
        {
            "process": "auditor",
            "end": END
        }
    )
    
    workflow.add_edge("auditor", "fixer")
    workflow.add_edge("fixer", "judge")
    workflow.add_edge("judge", "handle_result")
    
    workflow.add_conditional_edges(
        "handle_result",
        should_continue,
        {
            "select_file": "select_file",
            "retry_fix": "fixer",
            "end": END
        }
    )
    
    return workflow


def run_swarm_without_langgraph(target_dir: str, max_retries: int = 3) -> dict:
    """
    Run the Refactoring Swarm without LangGraph.
    This avoids dependency issues when langgraph cannot be imported.
    """
    print("=" * 60)
    print("🐝 REFACTORING SWARM - MISSION START")
    print("=" * 60)
    print("⚠️  LangGraph unavailable. Running in fallback mode.")

    state = initialize_state(target_dir, max_retries)

    print(f"\n📂 Target: {target_dir}")
    print(f"📄 Files to process: {len(state['files'])}")
    for f in state["files"]:
        print(f"   - {f}")
    print()

    while True:
        state = select_next_file(state)
        if not state["current_file"]:
            break

        while True:
            state = auditor_node(state)
            state = fixer_node(state)
            state = judge_node(state)
            state = handle_result(state)

            if state["test_passed"]:
                break
            if state["retry_count"] >= state["max_retries"]:
                break

    print("\n" + "=" * 60)
    print("🐝 REFACTORING SWARM - MISSION COMPLETE")
    print("=" * 60)
    print(f"\n✅ Completed: {len(state['completed_files'])} files")
    for f in state["completed_files"]:
        print(f"   - {f}")

    print(f"\n❌ Failed: {len(state['failed_files'])} files")
    for f in state["failed_files"]:
        print(f"   - {f}")

    return state


def run_swarm(target_dir: str, max_retries: int = 3) -> dict:
    """
    Run the Refactoring Swarm on a target directory.
    
    Args:
        target_dir: Directory containing code to refactor
        max_retries: Maximum fix attempts per file
        
    Returns:
        Final state with results
    """
    print("=" * 60)
    print("🐝 REFACTORING SWARM - MISSION START")
    print("=" * 60)
    
    if StateGraph is None:
        return run_swarm_without_langgraph(target_dir, max_retries)

    # Build and compile the graph
    workflow = build_graph()
    app = workflow.compile()
    
    # Initialize state
    initial_state = initialize_state(target_dir, max_retries)
    
    # Calculate recursion limit more accurately
    # Per file: select_file (1) + auditor (1) + (fixer + judge + handle) × (1 + retries) = 2 + 3(1+retries)
    # Total: files × (2 + 3×(1+retries)) + generous buffer to avoid hitting the limit
    steps_per_file = 2 + 3 * (1 + max_retries)
    calculated_limit = max(100, len(initial_state["files"]) * steps_per_file + 100)
    
    print(f"\n📂 Target: {target_dir}")
    print(f"📄 Files to process: {len(initial_state['files'])}")
    for f in initial_state['files']:
        print(f"   - {f}")
    print()
    
    # Run the graph with calculated recursion limit
    final_state = app.invoke(initial_state, {"recursion_limit": calculated_limit})
    
    # Print summary
    print("\n" + "=" * 60)
    print("🐝 REFACTORING SWARM - MISSION COMPLETE")
    print("=" * 60)
    print(f"\n✅ Completed: {len(final_state['completed_files'])} files")
    for f in final_state['completed_files']:
        print(f"   - {f}")
    
    print(f"\n❌ Failed: {len(final_state['failed_files'])} files")
    for f in final_state['failed_files']:
        print(f"   - {f}")
    
    return final_state
