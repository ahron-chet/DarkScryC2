import os
import shutil
import argparse

def remove_pycache_dirs(start_path):
    """
    Recursively finds and removes all __pycache__ directories starting from the given path.
    
    :param start_path: Path to start the search.
    """
    for root, dirs, files in os.walk(start_path):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                pycache_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(pycache_path)
                    print(f"Removed: {pycache_path}")
                except Exception as e:
                    print(f"Error removing {pycache_path}: {e}")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Remove all __pycache__ directories recursively.")
    parser.add_argument(
        "--path",
        type=str,
        default=os.getcwd(),
        help="Path to start searching for __pycache__ directories. Defaults to current directory.",
    )
    args = parser.parse_args()

    # Call the function to remove __pycache__ directories
    remove_pycache_dirs(args.path)

if __name__ == "__main__":
    main()
