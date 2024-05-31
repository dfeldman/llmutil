import os
import io
import pyperclip
import difflib
import subprocess

def read_clipboard():
    return pyperclip.paste()

def split_files(content):
    files = {}
    current_file = None
    commit_message = None

    for line in content.split('\n'):
        if line.startswith('Commit: '):
            commit_message = line[len('Commit: '):]
        elif line.startswith('File: '):
            current_file = line[len('File: '):]
            files[current_file] = []
        elif current_file:
            files[current_file].append(line)

    return files, commit_message

def display_diff(file_path, new_content):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            old_content = f.read()
        diff = difflib.unified_diff(old_content.split('\n'), new_content, fromfile=file_path, tofile=file_path, lineterm='')
        print('\n'.join(diff))
    else:
        print('\n'.join(new_content))

def process_file(file_path, content, added_files):
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

def commit_files(added_files, commit_message):
    if added_files:
        if not commit_message:
            commit_message = input("Enter a commit message: ")
        subprocess.run(['git', 'commit', '-m', commit_message] + added_files)

def main():
    content = read_clipboard()
    files, commit_message = split_files(content)
    added_files = []

    for file_path, content in files.items():
        display_diff(file_path, content)
        process_file(file_path, content, added_files)

    commit_files(added_files, commit_message)

    print("\nSummary:")
    print(f"- {len(added_files)} file(s) added to Git")
    print(f"- {len(files) - len(added_files)} file(s) skipped or overwritten without Git")
    print(f"- Total words in the original buffer: {len(content.split())}")

if __name__ == '__main__':
    main()