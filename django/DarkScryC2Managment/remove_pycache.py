import os
import shutil
import argparse

def remove_pycaches(path):
    """Remove all __pycache__ directories from the specified path."""
    if not os.path.exists(path):
        print(f"The path '{path}' does not exist.")
        return

    # Walk through the directory
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                dir_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(dir_path)  # Remove the __pycache__ directory and its contents
                    print(f"Removed: {dir_path}")
                except Exception as e:
                    print(f"Error removing {dir_path}: {e}")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Remove all __pycache__ directories from the specified path.")
    parser.add_argument(
        'path', 
        nargs='?', 
        default='.', 
        help="The path to search for __pycache__ directories (default: current directory)."
    )
    
    args = parser.parse_args()
    
    # Call the function to remove __pycache__ directories
    remove_pycaches(args.path)

if __name__ == "__main__":
    main()