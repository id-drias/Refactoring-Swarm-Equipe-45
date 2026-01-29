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
    

