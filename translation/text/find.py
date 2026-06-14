from pathlib import Path

def search_files_for_substring(root_dir: str, substring: str):
    target_path = Path(root_dir)
    
    if not target_path.exists():
        print(f"Error: The directory '{root_dir}' does not exist.")
        return

    for file_path in target_path.rglob('*.txt'):
        if file_path.is_file():
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    for line_number, line in enumerate(file, start=1):
                        if substring in line:
                            print(f"{file_path} (Line {line_number})")
            except Exception as e:
                print(f"Skipping {file_path} due to an error: {e}")

if __name__ == "__main__":
    SEARCH_DIRECTORY = "."  # Use "." for current folder
    SEARCH_TEXT = "Quit the current que"         # The word/phrase you want to find
    
    print(f"Searching for '{SEARCH_TEXT}' in {SEARCH_DIRECTORY}...\n")
    search_files_for_substring(SEARCH_DIRECTORY, SEARCH_TEXT)