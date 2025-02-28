# ORIC-poc-01: Organized Repository Information Compiler (Proof of Concept)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Introduction and Use Cases

The Organized Repository Information Compiler (ORIC) is a Python tool designed to analyze a directory (typically a code repository or a collection of personal audit documents) and compile its structure and content into a well-formatted YAML file. This YAML file can then be easily processed by Large Language Models (LLMs) for various purposes, including:

*   **Code Understanding:**  LLMs can use the compiled YAML to understand a codebase's architecture, identify dependencies, generate documentation, answer questions about the code, and even suggest improvements.
*   **DevOps Automation:**  The structured information can be used to automate DevOps tasks like generating deployment scripts, analyzing infrastructure configurations, and identifying potential security vulnerabilities.
*   **Self-Audit and Personal Growth:**  ORIC can also process personal audit documents (e.g., meeting notes, project planning reflections, daily journals) written in a similar YAML or Markdown structure.  This allows LLMs to analyze personal behavior, identify patterns, suggest improvements, and correlate personal data with code contributions.
*   **Knowledge Base Creation:** The generated YAML can serve as a structured knowledge base about a project or a collection of personal insights, making it easier to search, analyze, and share information.
*   **Rapid Prototyping Support:** Analyze a new project's structure to support quicker decision-making.

This repository, `ORIC-poc-01`, contains a proof-of-concept implementation of ORIC.

## How to Use

**1. Installation:**

No installation is required beyond having Python 3 installed. Simply clone this repository:

```bash
git clone https://github.com/your_username/ORIC-poc-01.git  # Replace your_username with your actual GitHub username
cd ORIC-poc-01
```

**2. Usage:**

The script (`ORIC.py`) takes the repository path as a command-line argument and can output the YAML to the console or a file.

**Basic Syntax:**

```bash
python3 ORIC.py <repository_path> [-n <repository_name>] [-d <description>] [-o <output_file>]
```

**Arguments:**

| Argument           | Short | Description                                                                                               | Default Value                   |
| :----------------- | :---- | :-------------------------------------------------------------------------------------------------------- | :------------------------------ |
| `repository_path`  |       | **Required.** The path to the root directory of the repository you want to analyze.                             |                                 |
| `--name`           | `-n`  | Optional.  The name of the repository.                                                                  | The name of the root directory. |
| `--description`    | `-d`  | Optional. A description of the repository.                                                                | An empty string.                |
| `--output`         | `-o`  | Optional. The path to the output YAML file. If not provided, the output is printed to the standard output. | Standard output (console).    |

**Examples:**

*   **Process a code repository and print the YAML to the console:**

    ```bash
    python3 ORIC.py /path/to/your/code/repository
    ```

*   **Process a directory of self-audits and save the output to a file:**

    ```bash
    python3 ORIC.py /path/to/your/self_audits -o audits.yaml
    ```

*   **Specify a repository name and description:**

    ```bash
    python3 ORIC.py /path/to/MyProject -n MyProject -d "This is my awesome project." -o my_project.yaml
    ```
*   **Create Sample Directory (For test)**
    ```bash
    # Create a test directory structure
    mkdir -p TestRepo/src TestRepo/docs
    echo "# Test Repository" > TestRepo/README.md
    cat << EOF > TestRepo/src/app.py
    def hello():
        print('Hello, world!')
        print('This is a multi-line string.')
        print('''
        This is a triple-quoted
        multi-line string.
        ''')
    EOF

    echo "This is a text file.\nWith multiple lines." > TestRepo/docs/notes.txt
    echo '{"key": "value"}' > TestRepo/data.json  # Add a JSON file

    # Create an empty .ipynb file
    touch TestRepo/notebook.ipynb


    # Run the script and save the output
    python3 ORIC.py TestRepo -o TestRepo.yaml
    ```

**3.  Self-Audit Data Structure:**

ORIC can also process personal audit data if it follows the same YAML structure as the code repository output. See the examples in the script's documentation for details.  You can use either YAML or Markdown files for your self-audits.  Keep self-audits in a separate directory (e.g., `self_audits`).

## Code Structure

The `ORIC.py` script is organized into the following main functions:

| Function             | Description                                                                                                                                                                                  |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `guess_language(file_path)` | Determines the programming language of a file based on its MIME type and file extension.  Handles a wide variety of languages and defaults to the file extension if the language is unknown. |
| `process_directory(root_path, repository_name, description)` | Recursively processes a directory, extracting information about files and subfolders, and creating a nested dictionary representing the repository structure.                                   |
| `represent_scalar(dumper, data)` | A custom YAML representer that *forces* the use of block style (`|`) for multi-line strings, ensuring correct formatting of file content in the YAML output.                           |
| `main()`             | Parses command-line arguments, calls `process_directory` to generate the data, and then uses `yaml.dump` to output the YAML, using the custom representer.                                     |

**Key Features and Considerations:**

*   **Recursive Processing:**  Handles nested directories to any depth.
*   **Language Detection:**  Identifies the programming language of files.
*   **Error Handling:**  Gracefully handles file reading errors (e.g., encoding issues).
*   **`.ipynb` Handling:**  Sets the content of `.ipynb` (Jupyter Notebook) files to an empty string (configurable).
*   **Hidden File/Folder Skipping:** Ignores hidden files and folders (names starting with `.`).
*   **README.md Handling:** Includes the content of a `README.md` file (if present) in the `readme_content` field.
*   **Custom YAML Representer:**  Ensures correct formatting of multi-line strings in the YAML output, using the literal block style (`|`).
* **Root Level File Support**: It also includes files that exist in the root folder.

## YAML Output Structure

The generated YAML output follows a consistent structure:

```yaml
repository_name: <name>
description: <description>
readme_content: |
  <content_of_readme>
context:
  overall_architecture: ""
  deployment_process: ""
  key_technologies: []
folders:
  - path: <folder_path>
    description: <folder_description>
    files:
      - path: <file_path>
        language: <language>
        description: <file_description>
        content: |
          <file_content>
    folders:  # Nested folders
      - ...
files: # Files Exist in Root Folder
      - path: <file_path>
        language: <language>
        description: <file_description>
        content: |
          <file_content>

```

## Contributing

Contributions are welcome!  Please submit pull requests or open issues to discuss proposed changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The only change needed from the previous response is to replace  `https://github.com/<your_username>/ORIC-poc-01.git` with `https://github.com/your_username/ORIC-poc-01.git`, where *your\_username* is your actual GitHub username.  Since I don't know your username, I cannot fill that in. The rest of the README is complete and does not use any placeholders. It's ready to be used directly in your repository.
