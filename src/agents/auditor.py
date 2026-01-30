"""
Auditor Agent - Analyzes code and creates refactoring plan.
"""
import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from src.tools import read_file, run_pylint
from src.utils.logger import log_experiment, ActionType
from .state import SwarmState


def load_prompt(prompt_file: str) -> str:
    """Load a prompt template from file."""
    prompt_path = os.path.join("src", "prompts", "auditor", prompt_file)
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


def auditor_node(state: SwarmState) -> SwarmState:
    """
    The Auditor agent (OPTIMIZED - 1 LLM call):
    1. Reads the current file
    2. Runs pylint for static analysis
    3. Generates audit report AND refactoring plan in ONE call
    """
    print(f"\n🔍 AUDITOR: Analyzing {state['current_file']}...")
    
    # Initialize the LLM
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.2  # Low temperature for consistent analysis
    )
    
    # Step 1: Read the file
    file_content = read_file(state["current_file"])
    if file_content.startswith(" Error") or file_content.startswith(" SECURITY"):
        print(f"❌ AUDITOR: Could not read file - {file_content}")
        state["audit_report"] = f"ERROR: {file_content}"
        return state
    
    state["original_code"] = file_content
    
    # Step 2: Run pylint
    pylint_output = run_pylint(state["current_file"])
    print(f"📋 Pylint analysis complete")
    
    # Step 3: Generate BOTH audit report AND plan in ONE call
    input_prompt = f"""You are a Python code auditor and refactoring planner.

TASK 1 - ANALYZE: Review the code and pylint output. List issues with severity (LOW/MEDIUM/HIGH).
TASK 2 - PLAN: Based on the issues, create a numbered refactoring plan.

=== PYLINT OUTPUT ===
{pylint_output}

=== CODE TO ANALYZE ===
```python
{file_content}
```

Respond in this EXACT format:

## AUDIT REPORT
[List issues here with severity]

## REFACTORING PLAN
[Numbered list of fixes]"""

    messages = [
        SystemMessage(content="You are a Python code auditor. Be concise and actionable."),
        HumanMessage(content=input_prompt)
    ]
    
    response = llm.invoke(messages)
    combined_response = response.content
    
    # Split the response into audit report and plan
    if "## REFACTORING PLAN" in combined_response:
        parts = combined_response.split("## REFACTORING PLAN")
        audit_report = parts[0].replace("## AUDIT REPORT", "").strip()
        refactoring_plan = parts[1].strip()
    else:
        # Fallback if format not followed
        audit_report = combined_response
        refactoring_plan = combined_response
    
    # Log the interaction
    log_experiment(
        agent_name="Auditor",
        model_used="llama-3.1-8b-instant",
        action=ActionType.ANALYSIS,
        details={
            "input_prompt": input_prompt,
            "output_response": combined_response,
            "file": state["current_file"],
            "pylint_output": pylint_output
        },
        status="SUCCESS"
    )
    
    print(f"✅ AUDITOR: Analysis and plan ready (1 API call)")
    
    # Update state
    state["audit_report"] = audit_report
    state["refactoring_plan"] = refactoring_plan
    
    return state
