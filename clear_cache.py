# clear_cache.py
import os
import shutil

def clear_pycache():
    for root, dirs, files in os.walk("."):
        for dir in dirs:
            if dir == "__pycache__":
                shutil.rmtree(os.path.join(root, dir))
                print(f"Deleted {os.path.join(root, dir)}")

def clear_pytest_cache():
    if os.path.exists(".pytest_cache"):
        shutil.rmtree(".pytest_cache")
        print("Deleted .pytest_cache")

def clear_mypy_cache():
    if os.path.exists(".mypy_cache"):
        shutil.rmtree(".mypy_cache")
        print("Deleted .mypy_cache")

if __name__ == "__main__":
    clear_pycache()
    clear_pytest_cache()
    clear_mypy_cache()
    print("Cache cleared successfully!")
