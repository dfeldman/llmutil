import os
import io
import pyperclip
import difflib
import subprocess
import argparse
from typing import List, Dict, Tuple

def read_clipboard() -> str:
    return pyperclip.paste()

def split_files(content: str, file_name: str = None) -> Tuple[Dict[str, List[str]], str]:
    files = {}
    current_file = None
    commit_message = None

    if file_name:
        files[file_name] = content.split('\n')
    else:
        for line in content.split('\n'):
            if line.startswith('Commit: '):
                commit_message = line[len('Commit: '):]
            elif line.startswith('File: '):
                current_file = line[len('File: '):]
                files[current_file] = []
            elif current_file:
                files[current_file].append(line)

    return files, commit_message

def display_diff(file_path: str, new_content: List[str]):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            old_content = f.read()
        diff = difflib.unified_diff(old_content.split('\n'), new_content, fromfile=file_path, tofile=file_path, lineterm='')
        print('\n'.join(diff))
    else:
        print('\n'.join(new_content))

def process_file(file_path: str, content: List[str], added_files: List[str]):
    while True:
        choice = input(f"File: {file_path}\nCommit/Overwrite/Skip (c/o/s): ").lower()
        if choice == 'c':
            if os.path.exists(file_path):
                if not subprocess.run(['git', 'ls-files', '--error-unmatch', file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                    input(f"File {file_path} is not committed in Git. Please commit the current contents and press Enter.")
            with open(file_path, 'w') as f:
                f.write('\n'.join(content))
            subprocess.run(['git', 'add', file_path])
            added_files.append(file_path)
            break
        elif choice == 'o':
            with open(file_path, 'w') as f:
                f.write('\n'.join(content))
            break
        elif choice == 's':
            break
        else:
            print("Invalid choice. Please enter 'c', 'o', or 's'.")

def commit_files(added_files: List[str], commit_message: str):
    if added_files:
        if not commit_message:
            commit_message = input("Enter a commit message: ")
        subprocess.run(['git', 'commit', '-m', commit_message, *added_files])

def main():
    parser = argparse.ArgumentParser(description='Process files from clipboard or command line.')
    parser.add_argument('file_name', nargs='?', help='File name to process (optional)')
    args = parser.parse_args()

    content: str = read_clipboard()
    total_words: int = len(content.split())
    files, commit_message = split_files(content, args.file_name)
    added_files: List[str] = []

    for file_path, file_content in files.items():
        display_diff(file_path, file_content)
        process_file(file_path, file_content, added_files)

    commit_files(added_files, commit_message)

    print("\nSummary:")
    print(f"- {len(added_files)} file(s) added to Git")
    print(f"- {len(files) - len(added_files)} file(s) skipped or overwritten without Git")
    print(f"- Total words in the original buffer: {total_words}")

if __name__ == '__main__':
    main()

