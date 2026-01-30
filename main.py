import argparse
import sys
import os
from dotenv import load_dotenv
from src.agents import run_swarm

load_dotenv()

def main():
    parser = argparse.ArgumentParser(
        description="🐝 Refactoring Swarm - Multi-Agent AI Code Refactoring System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --target_dir sandbox/buggy_code
  python main.py --target_dir sandbox/project --max_retries 5

The swarm will:
  1. 🔍 Auditor: Analyze code and create refactoring plan
  2. 🔧 Fixer: Apply fixes based on the plan
  3. ⚖️ Judge: Run tests and validate (self-healing loop)
        """
    )
    parser.add_argument(
        "--target_dir", 
        type=str, 
        required=True, 
        help="Directory containing Python code to refactor (must be inside sandbox/)"
    )
    parser.add_argument(
        "--max_retries",
        type=int,
        default=3,
        help="Maximum retry attempts per file if tests fail (default: 3)"
    )
    args = parser.parse_args()

    # Validate target directory exists
    if not os.path.exists(args.target_dir):
        print(f"❌ Directory '{args.target_dir}' not found.")
        sys.exit(1)
    
    # Security check: ensure target is inside sandbox
    abs_target = os.path.abspath(args.target_dir)
    sandbox_dir = os.path.abspath("sandbox")
    
    if not abs_target.startswith(sandbox_dir):
        print(f"❌ Security Error: Target directory must be inside 'sandbox/'")
        print(f"   Got: {abs_target}")
        print(f"   Expected prefix: {sandbox_dir}")
        sys.exit(1)

    print(f"🚀 STARTING REFACTORING SWARM")
    print(f"   Target: {args.target_dir}")
    print(f"   Max Retries: {args.max_retries}")
    
    # Run the swarm
    result = run_swarm(args.target_dir, max_retries=args.max_retries)
    
    # Exit with appropriate code
    if result["failed_files"]:
        print("\n⚠️ Some files failed to refactor completely.")
        sys.exit(1)
    else:
        print("\n✅ MISSION_COMPLETE - All files refactored successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()