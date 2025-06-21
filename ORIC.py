import os
import sys
import yaml
import mimetypes
import argparse

# --- Configuration for ignored items ---
# Set of directory names to ignore during traversal.
IGNORED_DIRS = {
    'node_modules', '.terraform', '.git', '__pycache__', '.vscode', '.idea',
    'dist', 'build', 'env', '.gitattributes', 'venv', '.vscode-test', '.cache',
    ,'.venv', 'target', '.mypy_cache', '.pytest_cache',
    '.tox', 'eggs', '.eggs', 'lib', 'lib64', 'bin', 'include', 'share'
}

# Set of file names to ignore.
IGNORED_FILES = {
    '.DS_Store', 'package-lock.json', 'yarn.lock', 'poetry.lock', 'Pipfile.lock'
}
# ----------------------------------------

def guess_language(file_path):
    """Guesses the programming language based on file extension."""
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        if mime_type == 'text/x-python':
            return 'python'
        elif mime_type == 'text/javascript':
            return 'javascript'
        elif mime_type == 'application/x-sh':
            return 'shell'
        elif mime_type == 'text/x-c':
            return 'c'
        elif mime_type == 'text/x-c++':
            return 'cpp'
        elif mime_type == 'text/x-java':
            return 'java'
        elif mime_type == 'text/x-go':
            return 'go'
        elif mime_type == 'text/x-ruby':
            return 'ruby'
        elif mime_type == 'text/x-php':
            return 'php'
        elif mime_type == 'text/x-csharp':
            return 'csharp'
        elif mime_type == 'text/x-swift':
             return 'swift'
        elif mime_type == 'application/json':
            return 'json'
        elif mime_type == 'text/html':
            return 'html'
        elif mime_type == 'text/css':
            return 'css'
        elif mime_type == 'text/markdown':
            return 'markdown'
        elif mime_type == 'application/x-yaml':
            return 'yaml'

    extension = os.path.splitext(file_path)[1].lower()
    if extension == '.tf':
        return 'terraform'
    elif extension == '.yaml' or extension == '.yml':
        return 'yaml'
    elif extension == '.py':
        return 'python'
    elif extension == '.js':
        return 'javascript'
    elif extension == '.go':
        return 'go'
    elif extension == '.md':
        return 'markdown'
    elif extension == '.ipynb':
        return 'ipynb'

    return extension[1:] if extension else 'unknown'

def process_directory(root_path, repository_name, description=""):
    """Processes a directory recursively for nested YAML."""

    data = {
        'repository_name': repository_name,
        'description': description,
        'readme_content': '',
        'context': {
            'overall_architecture': '',
            'deployment_process': '',
            'key_technologies': []
        },
        'folders': []
    }

    readme_path = os.path.join(root_path, 'README.md')
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                data['readme_content'] = f.read()
        except Exception as e:
            print(f"Error reading README.md: {e}", file=sys.stderr)

    def process_folder(folder_path, relative_path):
        folder_data = {
            'path': relative_path,
            'description': f"Folder: {relative_path}",
            'files': [],
            'folders': []
        }

        for item_name in sorted(os.listdir(folder_path)):
            item_path = os.path.join(folder_path, item_name)
            relative_item_path = os.path.join(relative_path, item_name)

            if os.path.isdir(item_path):
                if item_name in IGNORED_DIRS:
                    continue  # Skip ignored directories
                subfolder_data = process_folder(item_path, relative_item_path)
                # Only add the folder if it contains any files or subfolders
                if subfolder_data['files'] or subfolder_data['folders']:
                    folder_data['folders'].append(subfolder_data)

            elif os.path.isfile(item_path):
                if item_name in IGNORED_FILES:
                    continue # Skip ignored files

                try:
                    with open(item_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                except UnicodeDecodeError:
                    try:
                        with open(item_path, 'r', encoding='latin-1') as f:
                            file_content = f.read()
                    except Exception:
                        file_content = "" # Mark as unreadable
                except Exception:
                    file_content = "" # Mark as unreadable

                language = guess_language(item_path)
                if language == 'ipynb':
                    file_content = ""

                file_data = {
                    'path': relative_item_path,
                    'language': language,
                    'description': f"File: {item_name}",
                    'content': file_content
                }
                folder_data['files'].append(file_data)

        return folder_data

    for item_name in sorted(os.listdir(root_path)):
        item_path = os.path.join(root_path, item_name)
        
        # Skip README as it's handled separately
        if item_name == 'README.md':
            continue

        if os.path.isdir(item_path):
            if item_name in IGNORED_DIRS:
                continue # Skip ignored directories
            relative_item_path = os.path.join(os.path.relpath(root_path, root_path), item_name)
            subfolder_data = process_folder(item_path, relative_item_path)
            # Only add the folder if it contains any files or subfolders
            if subfolder_data['files'] or subfolder_data['folders']:
                data['folders'].append(subfolder_data)

        elif os.path.isfile(item_path):
            if item_name in IGNORED_FILES:
                continue # Skip ignored files

            relative_item_path = os.path.join(os.path.relpath(root_path, root_path), item_name)
            try:
                with open(item_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
            except UnicodeDecodeError:
                try:
                    with open(item_path, 'r', encoding='latin-1') as f:
                        file_content = f.read()
                except Exception:
                    file_content = ""
            except Exception:
                file_content = ""

            language = guess_language(item_path)
            if language == 'ipynb':
                file_content = ""
            file_data = {
                'path': relative_item_path,
                'language': language,
                'description': f"File: {item_name}",
                'content': file_content
            }
            if 'files' not in data:
                data['files'] = []
            data['files'].append(file_data)

    return data

def main():
    parser = argparse.ArgumentParser(description="Compile repository info to YAML.")
    parser.add_argument("repository_path", help="Path to the repository root.")
    parser.add_argument("-n", "--name", help="Repository name (defaults to folder name).")
    parser.add_argument("-d", "--description", help="Repository description.", default="")
    parser.add_argument("-o", "--output", help="Output file name (defaults to stdout).")
    args = parser.parse_args()

    repository_path = args.repository_path
    repository_name = args.name if args.name else os.path.basename(os.path.abspath(repository_path))
    description = args.description

    if not os.path.isdir(repository_path):
        print(f"Error: '{repository_path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    yaml_data = process_directory(repository_path, repository_name, description)

    # --- Custom YAML Representer (Force Block Style) ---
    def represent_scalar(dumper, data):
        if isinstance(data, str):
            if '\n' in data:  # Force block style for multi-line strings
                return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)

    yaml.add_representer(str, represent_scalar)
    # ----------------------------------------------------

    if args.output:
        with open(args.output, "w", encoding='utf-8') as outfile:
            yaml.dump(yaml_data, outfile, indent=2, sort_keys=False)
    else:
        print(yaml.dump(yaml_data, indent=2, sort_keys=False))

if __name__ == "__main__":
    main()
