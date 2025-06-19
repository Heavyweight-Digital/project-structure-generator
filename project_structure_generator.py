import os  # Import os module for interacting with the operating system.
import re  # Import re module for regular expressions.
import fnmatch  # Import fnmatch module for wildcard matching.

# Configuration settings
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))  # Root directory of the project (current directory of this file).
DOCUMENTATION_DIR = f"{PROJECT_DIR}/docs"  # Documentation directory (legacy).
OUTPUT_FILE = f"{DOCUMENTATION_DIR}/project_structure.txt"  # Output file path for project structure (legacy).
FUNCTIONS_FILE = f"{DOCUMENTATION_DIR}/functions.txt"  # Output file path for functions (legacy).
COMBINED_FILE = f"{DOCUMENTATION_DIR}/combined_structure.txt"  # Output file path for combined structure and functions (legacy).
EXPORT_STRUCTURE = False  # Whether to export the project structure file.
EXPORT_FUNCTIONS = False  # Whether to export the functions file.
EXPORT_COMBINED = True  # Whether to export the combined file.
RETURN_FOLDERS_ONLY = False  # If True, only include folder names in the output.
INCLUDE_ALL_FILES = False  # If True, include all files regardless of extensions.
MAX_DEPTH = 18  # Maximum depth for directory traversal.
IGNORE_DIRS = ['node_modules', 'lib', 'libs', 'DataTables', '.git', 'venv', 'chrome.app', '.vscode']  # Directory names or patterns to ignore.
IGNORE_FILES = ['README.md', 'CHANGELOG.md', '*.txt']  # File names or patterns to ignore.
EXTENSIONS_TO_INCLUDE = ('.js','.php', '.css')  # File extensions to include in the output.
PATTERNS = [r'links_(\d+)-(\d+)\.csv', r'part_\d+\.csv', r'links_\d+\.csv', r'(.*)_part_(\d+)\.csv']  # Patterns for identifying unique files.
SPECIAL_DIR_PATTERNS = [r'run_\d+']  # Patterns for special directories.
LANGUAGES = ['python', 'php', 'javascript']  # Languages to process for function and class extraction.

def generate_project_structure(project_dir,ignore_dirs,ignore_files,extensions_to_include,patterns,special_dir_patterns,languages,output_file,functions_file,combined_file,export_structure,export_functions,export_combined,return_folders_only,max_depth,include_all_files):
    ### Generate the project structure, extract functions/classes, and save to specified output files.
    tree = [os.path.basename(os.path.normpath(project_dir)) + "/"]  # Initialize the tree representation with the root directory.
    functions_data = []  # List to store function and class information for functions.txt

    # Compile all patterns from the provided list.
    compiled_patterns = [re.compile(pattern_str) for pattern_str in patterns]
    compiled_special_patterns = [re.compile(pattern) for pattern in special_dir_patterns]
    compiled_ignore_dir_patterns = [re.compile(fnmatch.translate(ignore)) for ignore in ignore_dirs]  # Compile ignore directory patterns.
    compiled_ignore_file_patterns = [re.compile(fnmatch.translate(ignore)) for ignore in ignore_files]  # Compile ignore file patterns.

    # Language-specific regex patterns for function and class extraction
    language_patterns = {
        'python': {
            'extensions': ('.py',),
            'function_regex': r'(?:^|\n)(?:[ \t]*#.*\n)*[ \t]*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*:',
            'comment_regex': r'((?:^[ \t]*#.*\n)*)[ \t]*def\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\)\s*:',
        },
        'php': {
            'extensions': ('.php',),
            'class_regex': r'(?:^|\n)(?:[ \t]*\/\*\*.*?\*\/[ \t]*\n)?[ \t]*(?:abstract\s+)?class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:extends\s+[a-zA-Z_][a-zA-Z0-9_]*\s*)?(?:implements\s+[a-zA-Z_][a-zA-Z0-9_]*(?:\s*,\s*[a-zA-Z_][a-zA-Z0-9_]*)*\s*)?{',
            'function_regex': r'(?:^|\n)[ \t]*(?:public|private|protected)?\s*(?:static\s+)?function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*(?::\s*[a-zA-Z_][a-zA-Z0-9_]*(?:\|\s*[a-zA-Z_][a-zA-Z0-9_]*)*\s*)?{\s*(?:[ \t]*\/\*\*\*[\s\S]*?\*\*\*[ \t]*\n)?',
            'comment_regex': r'function\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\)\s*\{\s*(\/\*\*\*[\s\S]*?\*\*\*\/)',
            'file_description_regex': r'<\?php\s*\n\/\*\*\s*\n\s*\*\s*Description:\s*(.*?)\s*\n\s*\*\s*File:.*?\*\/',
        },
        'javascript': {
            'extensions': ('.js',),
            'function_regex': r'(?:^|\n)(?:[ \t]*//.*\n|[ \t]*\/\*[^*]*\*\/[ \t]*\n)*[ \t]*(?:function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)|([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*function\s*\([^)]*\)|([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*\([^)]*\)\s*=>)\s*{',
            'comment_regex': r'function\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\)\s*\{\s*(\/\*\*\*[\s\S]*?\*\*\*\/)',
            'file_description_regex': r'\/\*\*\s*\n\s*\*[^\n]*\n\s*\*\s*File:.*?\n\s*\*\s*@version.*?\n\s*\*\s*@description\s*(.*?)\s*\n\s*\*\/',
        }
    }

    # Validate provided languages and filter based on extensions_to_include
    valid_languages = language_patterns.keys()
    processed_languages = []
    for lang in languages:
        if lang not in valid_languages:
            print(f"Warning: Language '{lang}' is not supported. Supported languages: {', '.join(valid_languages)}")
        elif any(ext in extensions_to_include for ext in language_patterns[lang]['extensions']):
            processed_languages.append(lang)
        else:
            print(f"Warning: Language '{lang}' skipped as its extensions are not in extensions_to_include")

    # Helper function to check if a directory matches any special pattern.
    def is_special_directory(directory):
        ### Check if the directory matches any special pattern.
        return any(re.match(pattern, directory) for pattern in compiled_special_patterns)

    # Helper function to check if a directory should be ignored based on ignore_patterns.
    def should_ignore_directory(directory):
        ### Check if the directory should be ignored based on patterns.
        return any(pattern.match(directory) for pattern in compiled_ignore_dir_patterns)

    # Helper function to check if a file should be ignored based on ignore_file_patterns.
    def should_ignore_file(file):
        ### Check if the file should be ignored based on patterns.
        return any(pattern.match(file) for pattern in compiled_ignore_file_patterns)

    # Helper function to find the end of a class (matching braces)
    def find_class_end(content, start_pos):
        ### Find the end of a class by matching braces.
        brace_count = 1
        pos = start_pos
        while pos < len(content) and brace_count > 0:
            if content[pos] == '{':
                brace_count += 1
            elif content[pos] == '}':
                brace_count -= 1
            pos += 1
        return pos if brace_count == 0 else len(content)

    # Helper function to extract functions and classes from a file
    def extract_functions(file_path, language):
        ### Extract functions, classes, and file descriptions from a file based on the specified language.
        if language not in language_patterns:
            return {'functions': [], 'classes': [], 'file_description': ''}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (IOError, UnicodeDecodeError):
            print(f"Warning: Could not read file '{file_path}'")
            return {'functions': [], 'classes': [], 'file_description': ''}

        functions = []
        classes = []
        file_description = ''
        patterns = language_patterns[language]

        # Extract file description for PHP or JavaScript files
        if language in ['php', 'javascript']:
            description_match = re.search(patterns['file_description_regex'], content, re.DOTALL)
            if description_match:
                file_description = description_match.group(1).strip()

        if language == 'php':
            # Extract classes
            class_matches = re.finditer(patterns['class_regex'], content)
            class_ranges = []
            for match in class_matches:
                class_name = match.group(1)
                class_start = match.start()
                class_end = find_class_end(content, match.end())
                class_content = content[match.start():class_end]
                class_ranges.append((class_start, class_end))
                
                # Extract methods within this class
                class_functions = []
                function_matches = re.finditer(patterns['function_regex'], class_content)
                comment_matches = re.finditer(patterns['comment_regex'], class_content)
                
                # Collect comments and functions
                comment_list = [(m.group(1).strip() if m.group(1) else '', m.start()) for m in comment_matches]
                function_list = [(m.group(1), m.start()) for m in function_matches]
                
                # Match comments to functions (comments after function start)
                for func_name, func_start in function_list:
                    closest_comment = ''
                    for comment, comment_start in comment_list:
                        if comment_start > func_start and (not closest_comment or comment_start < closest_comment[1]):
                            closest_comment = (comment, comment_start)
                    line_number = content[:func_start].count('\n') + 1
                    class_functions.append({
                        'name': func_name,
                        'comment': closest_comment[0] if closest_comment else '',
                        'line': line_number
                    })
                
                classes.append({
                    'name': class_name,
                    'functions': class_functions,
                    'comment': ''  # Class comments not currently extracted
                })

            # Extract all functions (standalone and methods)
            function_matches = re.finditer(patterns['function_regex'], content)
            comment_matches = re.finditer(patterns['comment_regex'], content)
            
            comment_list = [(m.group(1).strip() if m.group(1) else '', m.start()) for m in comment_matches]
            function_list = [(m.group(1), m.start()) for m in function_matches]
            
            for func_name, func_start in function_list:
                # Check if function is within a class
                is_class_method = False
                for class_start, class_end in class_ranges:
                    if class_start <= func_start < class_end:
                        is_class_method = True
                        break
                if not is_class_method:
                    closest_comment = ''
                    for comment, comment_start in comment_list:
                        if comment_start > func_start and (not closest_comment or comment_start < closest_comment[1]):
                            closest_comment = (comment, comment_start)
                    line_number = content[:func_start].count('\n') + 1
                    functions.append({
                        'name': func_name,
                        'comment': closest_comment[0] if closest_comment else '',
                        'line': line_number
                    })

        else:
            # Non-PHP languages (Python, JavaScript)
            function_matches = re.finditer(patterns['function_regex'], content)
            comment_matches = re.finditer(patterns['comment_regex'], content)

            comment_list = [(m.group(1).strip(), m.start()) for m in comment_matches]
            function_list = []
            for match in function_matches:
                func_name = next((g for g in match.groups() if g), None)
                if func_name:
                    function_list.append((func_name, match.start()))

            for func_name, func_start in function_list:
                closest_comment = ''
                for comment, comment_start in comment_list:
                    if comment_start < func_start and (not closest_comment or comment_start > closest_comment[1]):
                        closest_comment = (comment, comment_start)
                line_number = content[:func_start].count('\n') + 1
                functions.append({
                    'name': func_name,
                    'comment': closest_comment[0] if closest_comment else '',
                    'line': line_number
                })

        return {'functions': functions, 'classes': classes, 'file_description': file_description}

    # Walk through the directory tree.
    for dirpath, dirnames, filenames in os.walk(project_dir, topdown=True):
        depth = os.path.relpath(dirpath, project_dir).count(os.sep)  # Calculate the directory depth.
        if max_depth is not None and depth >= max_depth:
            continue  # Skip processing if the current depth exceeds the maximum allowed.

        dirnames[:] = [d for d in dirnames if not should_ignore_directory(d) and not is_special_directory(d)]
        dirnames.sort()  # Sort the directory names.

        relative_path = os.path.relpath(dirpath, project_dir)  # Get the relative path from the root directory.
        current_dir_name = os.path.basename(dirpath)  # Get the current directory name.

        if should_ignore_directory(current_dir_name):
            continue

        indent = '│   ' * depth  # Create the indent for the current depth.
        subindent = '│   ' * (depth + 1)  # Create the subindent for subdirectories.

        if return_folders_only:  # Check if only folder names should be returned.
            if relative_path != '.':
                tree.append(f"{indent}├── {current_dir_name}/")  # Add the directory to the tree.
            continue  # Skip the rest of the logic for files if we only want folders.

        # Identify unique files based on the patterns.
        pattern_dict = {}  # Dictionary to hold the first and last file matching each pattern.
        files_of_interest = set()  # Set to hold files that match the patterns.

        for file in filenames:  # Iterate through files in the current directory.
            if not file.startswith('.') and not should_ignore_file(file):  # Exclude hidden and ignored files.
                if include_all_files or any(file.endswith(ext) for ext in extensions_to_include):  # Include files based on extensions.
                    unique_found = False
                    for pattern in compiled_patterns:
                        match = pattern.match(file)
                        if match:
                            key = pattern.pattern
                            if key not in pattern_dict:
                                pattern_dict[key] = {"first": file, "last": file}
                            else:
                                pattern_dict[key]["last"] = file
                            unique_found = True
                            break
                    if not unique_found:
                        files_of_interest.add(file)

                    # Extract functions and classes from the file if it matches a language's extension
                    file_path = os.path.join(dirpath, file)
                    for lang in processed_languages:
                        if any(file.endswith(ext) for ext in language_patterns[lang]['extensions']):
                            data = extract_functions(file_path, lang)
                            relative_file_path = os.path.join(relative_path, file) if relative_path != '.' else file
                            functions_data.append({
                                'file': relative_file_path,
                                'language': lang,
                                'functions': data['functions'],
                                'classes': data['classes'],
                                'file_description': data['file_description']
                            })

        for files in pattern_dict.values():  # Add identified files to interest set.
            files_of_interest.add(files["first"])
            files_of_interest.add(files["last"])

        # Add directory line for folder to tree.
        if relative_path != '.':
            tree.append(f"{indent}├── {current_dir_name}/")

        # Append files of interest with correct connector
        sorted_files_of_interest = sorted(files_of_interest)  # Sort files of interest.
        for i, filename in enumerate(sorted_files_of_interest):  # Add files to tree.
            is_last_file = (i == len(sorted_files_of_interest) - 1)  # Check if last file.
            has_subdirectories = bool(dirnames)  # Check for subdirectories.
            connector = "└──" if is_last_file and not has_subdirectories else "├──"
            tree.append(f"{subindent}{connector} {filename}")

        # Add break line if necessary.
        if not dirnames and sorted_files_of_interest and sorted_files_of_interest[-1].endswith('.py'):
            tree.append(indent + '│')  # Add break line.

    # Clean up trailing connector lines.
    while tree and (tree[-1].strip() == "│" or tree[-1].strip() == ""):
        tree.pop()  # Remove trailing connector lines.

    # Save the project structure to a file if requested.
    if export_structure:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(tree))  # Write the tree representation to the file.
        print(f"Project structure has been saved to {output_file}")  # Print success message.

    # Save the functions and classes to functions.txt if requested
    if export_functions:
        with open(functions_file, 'w', encoding='utf-8') as f:
            for entry in functions_data:
                language = entry['language']

                if entry['language'] == 'php':
                    language = 'php'
                elif entry['language'] == 'python':
                    language = 'python'
                elif entry['language'] == 'javascript':
                    language = 'javascript'

                f.write(f"File: {entry['file']} ({language})\n")
                total_classes = len(entry['classes'])
                total_methods = sum(len(cls['functions']) for cls in entry['classes'])
                total_functions = len(entry['functions'])

                if total_classes == 0 and total_methods == 0 and total_functions == 0 and not entry['file_description']:
                    f.write("No functions, classes, or file description found\n")
                    continue

                if total_classes > 0:
                    f.write(f" Total Classes: {total_classes}")
                if total_methods > 0:
                    f.write(f" Total Methods: {total_methods}")
                if total_functions > 0:
                    f.write(f" Total Functions: {total_functions}")
                if entry['file_description']:
                    f.write(f"\n File Description: {entry['file_description']}")
                if total_classes > 0 or total_methods > 0 or total_functions > 0 or total_classes == 0 and total_methods == 0 and total_functions == 0 and entry['file_description']:
                    f.write("\n")

                # Write classes
                for cls in entry['classes']:
                    f.write(f"  Class: {cls['name']}\n")
                    for func in cls['functions']:
                        f.write(f"    Function: {func['name']}")
                        if func['comment']:
                            cleaned_comment = re.sub(r'^\/\*\*\*|\*\*\*\/$', '', func['comment'].strip()).strip()
                            f.write(f"\n    - Function Description: {cleaned_comment}")
                        f.write("\n")
                        
                # Write standalone functions
                for func in entry['functions']:
                    f.write(f"  Function: {func['name']} (Line {func['line']})")
                    if func['comment']:
                        cleaned_comment = re.sub(r'^\/\*\*\*|\*\*\*\/$', '', func['comment'].strip()).strip()
                        f.write(f"\n  - Function Description: {cleaned_comment}")
                    f.write("\n")
                f.write("\n")
        print(f"Function and class information has been saved to {functions_file}")  # Print success message.

    # Save combined structure and functions to combined file if requested
    if export_combined:
        if not os.path.exists(DOCUMENTATION_DIR):
            os.makedirs(DOCUMENTATION_DIR)
        with open(combined_file, 'w', encoding='utf-8') as f:
            f.write("Project Structure:\n")
            for line in tree:
                f.write(f"  {line}\n")
            f.write("\nFile Structure:\n")
            for entry in functions_data:
                language = entry['language']
                f.write(f"  File: {entry['file']} ({language})")
                total_classes = len(entry['classes'])
                total_methods = sum(len(cls['functions']) for cls in entry['classes'])
                total_functions = len(entry['functions'])

                if total_classes == 0 and total_methods == 0 and total_functions == 0 and not entry['file_description']:
                    f.write(" No functions or classes found\n")
                    continue

                if total_classes > 0:
                    f.write(f" Total Classes: {total_classes}")
                if total_methods > 0:
                    f.write(f" Total Methods: {total_methods}")
                if total_functions > 0:
                    f.write(f" Total Functions: {total_functions}")
                if entry['file_description']:
                    f.write(f"\n  - File Description: {entry['file_description']}")
                if total_classes > 0 or total_methods > 0 or total_functions > 0 or total_classes == 0 and total_methods == 0 and total_functions == 0 and entry['file_description']:
                    f.write("\n")

                # Write classes
                for cls in entry['classes']:
                    f.write(f"    Class: {cls['name']}\n")
                    for func in cls['functions']:
                        f.write(f"      Function: {func['name']}")
                        if func['comment']:
                            cleaned_comment = re.sub(r'^\/\*\*\*|\*\*\*\/$', '', func['comment'].strip()).strip()
                            f.write(f"\n      - Function Description: {cleaned_comment}")
                        f.write("\n")
                        
                # Write standalone functions
                for func in entry['functions']:
                    f.write(f"    Function: {func['name']} (Line {func['line']})")
                    if func['comment']:
                        cleaned_comment = re.sub(r'^\/\*\*\*|\*\*\*\/$', '', func['comment'].strip()).strip()
                        f.write(f"\n    - Function Description: {cleaned_comment}")
                    f.write("\n")
                f.write("\n")
        print(f"Combined structure and function information has been saved to {combined_file}")

# Entry point of the script.
if __name__ == '__main__':
    generate_project_structure(
        project_dir=PROJECT_DIR,
        ignore_dirs=IGNORE_DIRS,
        ignore_files=IGNORE_FILES,
        extensions_to_include=EXTENSIONS_TO_INCLUDE,
        patterns=PATTERNS,
        special_dir_patterns=SPECIAL_DIR_PATTERNS,
        languages=LANGUAGES,
        output_file=OUTPUT_FILE,
        functions_file=FUNCTIONS_FILE,
        combined_file=COMBINED_FILE,
        export_structure=EXPORT_STRUCTURE,
        export_functions=EXPORT_FUNCTIONS,
        export_combined=EXPORT_COMBINED,
        return_folders_only=RETURN_FOLDERS_ONLY,
        max_depth=MAX_DEPTH,
        include_all_files=INCLUDE_ALL_FILES
    )  # Generate the project structure.