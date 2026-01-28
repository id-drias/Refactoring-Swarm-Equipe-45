import argparse
import sys
import os
from dotenv import load_dotenv
from src.utils.logger import log_experiment, ActionType

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Refactoring Swarm - AI Agent System")
    parser.add_argument("--target_dir", type=str, required=True, help="Directory containing code to analyze")
    args = parser.parse_args()

    if not os.path.exists(args.target_dir):
        print(f"❌ Dossier {args.target_dir} introuvable.")
        sys.exit(1)

    print(f"🚀 DEMARRAGE SUR : {args.target_dir}")
    
    # TODO: Add your swarm agents here
    # Example workflow:
    # 1. Analyze code in target_dir
    # 2. Generate fixes/improvements
    # 3. Apply corrections
    # 4. Log each LLM interaction
    
    print("✅ MISSION_COMPLETE")

if __name__ == "__main__":
    main()
    
    # test merge 