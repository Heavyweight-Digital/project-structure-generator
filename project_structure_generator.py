import os  # Import os module for interacting with the operating system.  
import re  # Import re module for regular expressions.  
import fnmatch  # Import fnmatch module for wildcard matching.  

# The purpose of this script is to generate a structured and formatted representation of a project's directory and file hierarchy.  
# This script is particularly useful for developers who need to document and understand the layout of a large project. It ensures that  
# directories and files are presented in a readable and organized manner, with special handling to ignore specific directories,  
# define which files to include in the output, and group files with similar naming patterns.  
#   
# The pattern logic allows listing only one of each of the values defined as a pattern. For example, if you have 10 CSV files in a folder  
# that increment in value, instead of listing all of them (which would make the output very long), it will list just one for each folder.  
# The output will not repeat or output folders that have the same depth and final folder name.  
#  
# Directories in ignore_dirs can have wildcard patterns which will be correctly interpreted and matched.  
# For example, '*.cache' will ignore any directory ending with '.cache'.  
# Another example, '.*' will ignore all hidden directories starting with a '.'.  

# Function: generate_project_structure; Generates and saves a structured representation of the project directory.  
def generate_project_structure(project_dir, ignore_dirs, extensions_to_include, patterns, special_dir_patterns, output_file='project_structure.txt'):  
    tree = ["project_root/"]  # Initialize the tree representation with the root directory.  

    # Compile all patterns from the provided list.  
    compiled_patterns = [re.compile(pattern_str) for pattern_str in patterns]  
    compiled_special_patterns = [re.compile(pattern) for pattern in special_dir_patterns]  
    compiled_ignore_patterns = [re.compile(fnmatch.translate(ignore)) for ignore in ignore_dirs]  # Compile ignore patterns.  
    
    # Helper function to check if a directory matches any special pattern.  
    def is_special_directory(directory):  
        return any(re.match(pattern, directory) for pattern in compiled_special_patterns)  

    # Helper function to check if a directory should be ignored based on ignore_patterns.  
    def should_ignore_directory(directory):  
        return any(pattern.match(directory) for pattern in compiled_ignore_patterns)  

    # Walk through the directory tree.  
    for dirpath, dirnames, filenames in os.walk(project_dir, topdown=True):  
        dirnames[:] = [d for d in dirnames if not should_ignore_directory(d) and not is_special_directory(d)]  
        dirnames.sort()  # Sort the directory names.  

        relative_path = os.path.relpath(dirpath, project_dir)  # Get the relative path from the root directory.  
        current_dir_name = os.path.basename(dirpath)  # Get the current directory name.  
        
        if should_ignore_directory(current_dir_name):  
            continue  

        depth = relative_path.count(os.sep)  # Calculate the directory depth.  
        indent = '│   ' * depth  # Create the indent for the current depth.  
        subindent = '│   ' * (depth + 1)  # Create the subindent for subdirectories.  

        # Identify unique files based on the patterns.  
        pattern_dict = {}  # Dictionary to hold the first and last file matching each pattern.  
        files_of_interest = set()  

        for file in filenames:  
            if file.endswith(extensions_to_include) and not file.startswith('.'):  
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

        for files in pattern_dict.values():  
            files_of_interest.add(files["first"])  
            files_of_interest.add(files["last"])  

        # Add directory line  
        if relative_path != '.':  
            tree.append(f"{indent}├── {current_dir_name}/")  # Add the directory to the tree.  

        # Append files of interest with correct connector  
        sorted_files_of_interest = sorted(files_of_interest)  
        for i, filename in enumerate(sorted_files_of_interest):  # Iterate and sort files of interest.  
            is_last_file = (i == len(sorted_files_of_interest) - 1)  # Check if this is the last file.  
            has_subdirectories = bool(dirnames)  # Check if there are subdirectories.  
            connector = "└──" if is_last_file and not has_subdirectories else "├──"  # Determine the connector.  
            tree.append(f"{subindent}{connector} {filename}")  # Add the file to the tree.  

        # Add break line only if there are no subdirectories and the last file is a Python file.  
        if not dirnames and sorted_files_of_interest and sorted_files_of_interest[-1].endswith('.py'):  
            tree.append(indent + '│')  # Add the break line.  

    # Remove the trailing connector lines if they are at the end of the tree.  
    while tree and (tree[-1].strip() == "│" or tree[-1].strip() == ""):  
        tree.pop()  # Remove trailing connector lines.  

    # Save the project structure to a file.  
    with open(output_file, 'w') as f:  
        f.write("\n".join(tree))  # Write the tree representation to the file.  
    print(f"Project structure has been saved to {output_file}")  # Print success message.  

# Entry point of the script.  
if __name__ == '__main__':  
    project_dir = '/Volumes/Other/'  # Define th root directory of the project.
    output_path = 'project_structure.txt'  # Define the output file path.  

    # List of directory names to ignore.  
    ignore_dirs = ['node_modules', 'lib', 'libs', '.git', 'venv', 'chrome.app', '.vscode', '.*']  
    extensions_to_include = ('.py', '.json', '.php', '.csv')  # Define the file extensions of interest.  
    patterns = [r'links_(\d+)-(\d+)\.csv', r'part_\d+\.csv', r'links_\d+\.csv', r'(.*)_part_(\d+)\.csv']  # Define the patterns for identifying unique files.  
    special_dir_patterns = [r'run_\d+']  # Define patterns for special directories.  

    generate_project_structure(project_dir, ignore_dirs, extensions_to_include, patterns, special_dir_patterns, output_path)  # Generate the project structure.