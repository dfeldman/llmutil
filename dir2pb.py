import os
import io
import pyperclip
import argparse

def get_file_extensions():
    return ['.py', '.go']  # Add more file extensions as needed

def copy_files_to_clipboard(directory):
    extensions = get_file_extensions()
    buffer = io.StringIO()
    copied_files = []
    total_words = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                copied_files.append(file_path)

                with open(file_path, 'r') as f:
                    content = f.read()
                    total_words += len(content.split())
                    buffer.write(f"File: {file_path}\n")
                    buffer.write(content)
                    buffer.write("\n\n")

    pyperclip.copy(buffer.getvalue())
    buffer.close()

    print("Copied files:")
    for file in copied_files:
        print(file)
    print(f"\nTotal words: {total_words}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Copy files to clipboard.')
    parser.add_argument('directory', nargs='?', default=os.getcwd(),
                        help='Directory path (default: current directory)')
    args = parser.parse_args()

    copy_files_to_clipboard(args.directory)