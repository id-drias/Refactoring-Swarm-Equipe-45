import os
import subprocess

# had fonction bach t9ra w tkteb f les fichiers berk f sandbox (3la jal security)

SANDBOX_DIR = os.path.abspath("sandbox")

def _is_safe_path(file_path: str) -> bool:
    '''nhezou l chemin absolu w nverifyiw eli howa dakhel sandbox'''
    abs_path = os.path.abspath(file_path)
    return abs_path.startswith(SANDBOX_DIR)



def read_file(file_path: str) -> str:
    '''nvirifiw eda nkedrou n9raw'''
    if not _is_safe_path(file_path):
        return f" SECURITY ERROR: Access denied to {file_path}. Stay in the sandbox."
    
    if not os.path.exists(file_path):
        return f" Error: File {file_path} not found."

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f" Error reading file: {str(e)}"



def write_file(file_path: str, content: str) -> str:
    '''nvirifiw eda nkedrou nktebw'''
    if not _is_safe_path(file_path):
        return f" SECURITY ERROR: Cannot write to {file_path}. Stay in the sandbox."
    
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f" Successfully wrote to {file_path}"
    except Exception as e:
        return f" Error writing file: {str(e)}"
    

def run_pylint(file_path: str) -> str:
    '''hadi interface ta3 pylint tool'''
    if not _is_safe_path(file_path):
        return " SECURITY ERROR: Cannot analyze files outside sandbox."

    try:
        # nruniw pylint 3la l fichier m3a disable ta3 docstring warnings
        result = subprocess.run(
            ["pylint", file_path, "--disable=C0114,C0115,C0116"], 
            capture_output=True, 
            text=True
        )
        return result.stdout if result.stdout else result.stderr
    except FileNotFoundError:
        return " Error: Pylint is not installed. Please check requirements.txt."
    except Exception as e:
        return f" Error running Pylint: {str(e)}"



def run_pytest(test_file_path: str) -> str:
    '''hadi interface ta3 pytest tool'''
    if not _is_safe_path(test_file_path):
        return " SECURITY ERROR: Cannot run tests outside sandbox."

    try:
        # nruniw pytest 3la l fichier ta3 tests
        result = subprocess.run(
            ["pytest", test_file_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return f" ALL TESTS PASSED:\n{result.stdout}"
        else:
            return f" TESTS FAILED:\n{result.stdout}"
    except FileNotFoundError:
        return " Error: Pytest is not installed."
    except Exception as e:
        return f" Error running Pytest: {str(e)}"