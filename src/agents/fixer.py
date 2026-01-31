"""
Fixer Agent - Applies corrections based on the refactoring plan.
"""
import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from src.tools import write_file, read_file
from src.utils.logger import log_experiment, ActionType
from .state import SwarmState


def load_prompt(prompt_file: str) -> str:
    """Load a prompt template from file."""
    prompt_path = os.path.join("src", "prompts", "fixer", prompt_file)
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


def find_test_file(source_file: str) -> str:
    """Find the corresponding test file for a source file."""
    dir_name = os.path.dirname(source_file)
    base_name = os.path.basename(source_file)
    
    # Try same directory: test_<filename>.py
    test_file = os.path.join(dir_name, f"test_{base_name}")
    if os.path.exists(test_file):
        return test_file
    
    return None


def fixer_node(state: SwarmState) -> SwarmState:
    """
    The Fixer agent:
    1. Reads the audit report, refactoring plan, AND test file
    2. Applies fixes to the code
    3. Writes the corrected code back to the file
    """
    is_retry = state["retry_count"] > 0
    
    if is_retry:
        print(f"\n🔧 FIXER: Retry #{state['retry_count']} for {state['current_file']}...")
    else:
        print(f"\n🔧 FIXER: Applying fixes to {state['current_file']}...")
    
    # Initialize the LLM
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.1  # Very low temperature for precise code generation
    )
    
    # Read the test file to understand expected behavior
    test_file = find_test_file(state["current_file"])
    test_content = ""
    if test_file:
        test_content = read_file(test_file)
        if test_content.startswith(" Error") or test_content.startswith(" SECURITY"):
            test_content = ""
    
    test_section = ""
    if test_content:
        test_section = f"""
=== TEST FILE (YOUR CODE MUST PASS THESE TESTS) ===
```python
{test_content}
```

CRITICAL: Read the tests carefully! Your code MUST:
- Raise the EXACT exception types the tests expect (ValueError, not ZeroDivisionError, etc.)
- Return values when tests check return values (don't just print)
- Match the exact behavior the tests are checking for
"""
    
    # Choose prompt based on whether this is a retry
    if is_retry:
        prompt_template = load_prompt("retry_fix.txt")
        input_prompt = f"""{prompt_template}

=== ORIGINAL CODE ===
```python
{state['original_code']}
```

=== PREVIOUS FIX ATTEMPT ===
```python
{state['fixed_code']}
```

=== TEST ERROR LOGS ===
{state['error_logs']}
{test_section}
=== REFACTORING PLAN ===
{state['refactoring_plan']}

Provide the corrected code:"""
    else:
        prompt_template = load_prompt("fix_code.txt")
        input_prompt = f"""{prompt_template}

=== AUDIT REPORT ===
{state['audit_report']}

=== REFACTORING PLAN ===
{state['refactoring_plan']}

=== CODE TO FIX ===
```python
{state['original_code']}
```
{test_section}
Provide the corrected code:"""

    messages = [
        SystemMessage(content="You are a Python code fixer. Return ONLY the corrected code, no explanations. CRITICAL: Your code must pass all the provided tests - match exact exception types and return values!"),
        HumanMessage(content=input_prompt)
    ]
    
    response = llm.invoke(messages)
    raw_response = response.content
    fixed_code = raw_response
    
    # Clean up the response (remove markdown code blocks if present)
    fixed_code = fixed_code.strip()
    if fixed_code.startswith("```python"):
        fixed_code = fixed_code[9:]
    if fixed_code.startswith("```"):
        fixed_code = fixed_code[3:]
    if fixed_code.endswith("```"):
        fixed_code = fixed_code[:-3]
    fixed_code = fixed_code.strip()
    
    # Log the interaction
    log_experiment(
        agent_name="Fixer",
        model_used="llama-3.1-8b-instant",
        action=ActionType.FIX,
        details={
            "input_prompt": input_prompt,
            "output_response": raw_response,
            "file": state["current_file"],
            "is_retry": is_retry,
            "retry_count": state["retry_count"]
        },
        status="SUCCESS"
    )
    
    # Write the fixed code
    write_result = write_file(state["current_file"], fixed_code)
    
    if "Successfully" in write_result:
        print(f"✅ FIXER: Code corrected and saved")
    else:
        print(f"❌ FIXER: Failed to write file - {write_result}")
    
    # Update state
    state["fixed_code"] = fixed_code
    
    return state
