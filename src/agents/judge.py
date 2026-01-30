"""
Judge Agent - Validates fixes by running tests.
No LLM calls - uses raw pytest output to save API quota.
"""
import os

from src.tools import run_pytest
from src.utils.logger import log_experiment, ActionType
from .state import SwarmState


def find_test_file(source_file: str) -> str:
    """
    Find the corresponding test file for a source file.
    Convention: test_<filename>.py in the same directory or tests/ folder.
    """
    dir_name = os.path.dirname(source_file)
    base_name = os.path.basename(source_file)
    
    # Try same directory: test_<filename>.py
    test_file = os.path.join(dir_name, f"test_{base_name}")
    if os.path.exists(test_file):
        return test_file
    
    # Try tests/ subdirectory
    test_file = os.path.join(dir_name, "tests", f"test_{base_name}")
    if os.path.exists(test_file):
        return test_file
    
    # Try parent tests/ directory
    parent_dir = os.path.dirname(dir_name)
    test_file = os.path.join(parent_dir, "tests", f"test_{base_name}")
    if os.path.exists(test_file):
        return test_file
    
    # Return the expected location even if not found
    return os.path.join(dir_name, f"test_{base_name}")


def judge_node(state: SwarmState) -> SwarmState:
    """
    The Judge agent:
    1. Runs pytest on the test file
    2. Analyzes the results (NO LLM - uses raw output to save quota)
    3. Decides if tests pass or if retry is needed
    """
    print(f"\n⚖️ JUDGE: Evaluating {state['current_file']}...")
    
    # Find the test file
    test_file = find_test_file(state["current_file"])
    
    # Run tests
    test_output = run_pytest(test_file)
    state["test_results"] = test_output
    
    # Determine if tests passed
    if "ALL TESTS PASSED" in test_output:
        state["test_passed"] = True
        state["error_logs"] = None
        print(f"✅ JUDGE: All tests passed!")
        
        # Log success
        log_experiment(
            agent_name="Judge",
            model_used="none",
            action=ActionType.DEBUG,
            details={
                "input_prompt": f"Run tests for {state['current_file']}",
                "output_response": "All tests passed",
                "test_file": test_file,
                "test_output": test_output
            },
            status="SUCCESS"
        )
    else:
        state["test_passed"] = False
        print(f"❌ JUDGE: Tests failed!")
        
        # NO LLM CALL - Just use raw pytest output to save API quota
        # The Fixer can interpret pytest errors directly
        state["error_logs"] = f"TEST FAILED - RAW OUTPUT:\n{test_output}"
        
        # Log failure
        log_experiment(
            agent_name="Judge",
            model_used="none",
            action=ActionType.DEBUG,
            details={
                "input_prompt": f"Run tests for {state['current_file']}",
                "output_response": f"Tests failed. Raw output provided to Fixer.",
                "test_file": test_file,
                "test_output": test_output
            },
            status="FAILURE"
        )
        
        print(f"📋 JUDGE: Passed raw test output to Fixer (no LLM used)")
    
    return state
