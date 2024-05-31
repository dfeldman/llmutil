import os
import ast
import pyperclip
import re

def extract_comments(node):
    if not node.body:
        return ""
    first_node = node.body[0]
    if isinstance(first_node, ast.Expr) and isinstance(first_node.value, ast.Str):
        return first_node.value.s.strip()
    return ""

def process_python_file(file_path):
    with open(file_path, "r") as file:
        tree = ast.parse(file.read())

    outline = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            comment = extract_comments(node)
            outline.append(f"Function: {node.name}")
            if comment:
                outline.append(f"  Comment: {comment}")

        elif isinstance(node, ast.ClassDef):
            comment = extract_comments(node)
            outline.append(f"Class: {node.name}")
            if comment:
                outline.append(f"  Comment: {comment}")

            for subnode in node.body:
                if isinstance(subnode, ast.FunctionDef):
                    method_comment = extract_comments(subnode)
                    outline.append(f"  Method: {subnode.name}")
                    if method_comment:
                        outline.append(f"    Comment: {method_comment}")

        elif isinstance(node, ast.Assign):
            if isinstance(node.targets[0], ast.Name) and isinstance(node.value, (ast.Num, ast.Str, ast.NameConstant)):
                constant_name = node.targets[0].id
                constant_value = ast.literal_eval(node.value)
                outline.append(f"Constant: {constant_name} = {constant_value}")

    return outline

def process_js_ts_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    outline = []
    pattern = r"(?:\/\*\*(?P<comment>[\s\S]*?)\*\/\s*)?\s*(?:(?:export|const|let|var)\s+)?(?:function|class|interface|type)\s+(?P<name>\w+)"
    matches = re.finditer(pattern, content)

    for match in matches:
        name = match.group("name")
        comment = match.group("comment")
        if comment:
            comment = comment.strip()
        if "function" in match.group():
            outline.append(f"Function: {name}")
        elif "class" in match.group():
            outline.append(f"Class: {name}")
        elif "interface" in match.group():
            outline.append(f"Interface: {name}")
        elif "type" in match.group():
            outline.append(f"Type: {name}")
        if comment:
            outline.append(f"  Comment: {comment}")

    return outline

def process_go_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    outline = []
    pattern = r"(?:\/\/(?P<comment>.*?)\n)?\s*(?P<keyword>func|type|const|var)\s+(?P<name>\w+)"
    matches = re.finditer(pattern, content)

    for match in matches:
        name = match.group("name")
        comment = match.group("comment")
        if comment:
            comment = comment.strip()
        keyword = match.group("keyword")
        if keyword == "func":
            outline.append(f"Function: {name}")
        elif keyword == "type":
            outline.append(f"Type: {name}")
        elif keyword in ["const", "var"]:
            outline.append(f"Variable: {name}")
        if comment:
            outline.append(f"  Comment: {comment}")

    return outline

def process_html_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    outline = []
    pattern = r"<(?P<tag>\w+).*?(?:id|class)=[\"'](?P<class>[\w-]+)[\"'].*?>"
    matches = re.finditer(pattern, content)

    for match in matches:
        tag = match.group("tag")
        class_name = match.group("class")
        outline.append(f"{tag}: {class_name}")

    return outline

def process_css_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    outline = []
    pattern = r"\.(?P<class>[\w-]+)\s*\{"
    matches = re.finditer(pattern, content)

    for match in matches:
        class_name = match.group("class")
        outline.append(f"Class: {class_name}")

    return outline

def process_hugo_template(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    outline = []
    pattern = r"{{.*?partial\s+[\"'](?P<partial>[\w-]+)[\"'].*?}}"
    matches = re.finditer(pattern, content)

    for match in matches:
        partial = match.group("partial")
        outline.append(f"Partial: {partial}")

    return outline

def process_markdown_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    outline = []
    pattern = r"^#{1,6}\s+(?P<heading>.*?)$"
    matches = re.finditer(pattern, content, re.MULTILINE)

    for match in matches:
        heading = match.group("heading")
        outline.append(f"Heading: {heading}")

    return outline

def process_javascript_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    outline = []
    pattern = r"(?:\/\*\*(?P<comment>[\s\S]*?)\*\/\s*)?\s*(?:(?:export|const|let|var)\s+)?(?:function|class)\s+(?P<name>\w+)"
    matches = re.finditer(pattern, content)

    for match in matches:
        name = match.group("name")
        comment = match.group("comment")
        if comment:
            comment = comment.strip()
        if "function" in match.group():
            outline.append(f"Function: {name}")
        elif "class" in match.group():
            outline.append(f"Class: {name}")
        if comment:
            outline.append(f"  Comment: {comment}")

    return outline

def process_data_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    outline = []
    outline.append(f"Data: {content}")

    return outline

def create_code_index(directory):
    code_index = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            # ... (previous code for Python, JavaScript/TypeScript, and Go remains the same)
            elif file.endswith(".html"):
                file_path = os.path.join(root, file)
                module_name = os.path.relpath(file_path, directory)
                code_index.append(f"HTML File: {module_name}")
                code_index.extend(process_html_file(file_path))
                code_index.append("")  # Add a blank line for separation
            elif file.endswith(".css"):
                file_path = os.path.join(root, file)
                module_name = os.path.relpath(file_path, directory)
                code_index.append(f"CSS File: {module_name}")
                code_index.extend(process_css_file(file_path))
                code_index.append("")  # Add a blank line for separation
            elif file.endswith(".md"):
                file_path = os.path.join(root, file)
                module_name = os.path.relpath(file_path, directory)
                code_index.append(f"Markdown File: {module_name}")
                code_index.extend(process_markdown_file(file_path))
                code_index.append("")  # Add a blank line for separation
            elif file.endswith(".js"):
                file_path = os.path.join(root, file)
                module_name = os.path.relpath(file_path, directory)
                code_index.append(f"JavaScript File: {module_name}")
                code_index.extend(process_javascript_file(file_path))
                code_index.append("")  # Add a blank line for separation
            elif file.endswith((".json", ".yaml", ".yml", ".toml")):
                file_path = os.path.join(root, file)
                module_name = os.path.relpath(file_path, directory)
                code_index.append(f"Data File: {module_name}")
                code_index.extend(process_data_file(file_path))
                code_index.append("")  # Add a blank line for separation
            elif file.endswith((".jpg", ".png", ".gif")):
                file_path = os.path.join(root, file)
                module_name = os.path.relpath(file_path, directory)
                code_index.append(f"Image File: {module_name}")
                code_index.append("")  # Add a blank line for separation

    return "\n".join(code_index)

# Example usage
directory = "."  # Current directory
code_index = create_code_index(directory)
print(code_index)

# Copy the code index to the clipboard
pyperclip.copy(code_index)
print("Code index copied to clipboard.")
