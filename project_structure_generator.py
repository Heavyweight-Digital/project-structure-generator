import os  # Import os module for interacting with the operating system.  
import re  # Import re module for regular expressions.  
import fnmatch  # Import fnmatch module for wildcard matching.  

def generate_project_structure(project_dir, ignore_dirs, extensions_to_include, patterns, special_dir_patterns, output_file='project_structure.txt', return_folders_only=False, max_depth=None):  
    tree = [os.path.basename(os.path.normpath(project_dir)) + "/"]  # Initialize the tree representation with the root directory.  

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
            # Add directory line  
            if relative_path != '.':  
                tree.append(f"{indent}├── {current_dir_name}/")  # Add the directory to the tree.  
            continue  # Skip the rest of the logic for files if we only want folders.  

        # Identify unique files based on the patterns.  
        pattern_dict = {}  # Dictionary to hold the first and last file matching each pattern.  
        files_of_interest = set()  # Set to hold files that match the patterns.  

        for file in filenames:  # Iterate through files in the current directory.  
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

    # Save the project structure to a file.  
    with open(output_file, 'w') as f:  
        f.write("\n".join(tree))  # Write the tree representation to the file.  
    print(f"Project structure has been saved to {output_file}")  # Print success message.  

# Entry point of the script.  
if __name__ == '__main__':  
    # Define the root directory of the project.  
    project_dir = '/Volumes/Other/'  # Define th root directory of the project.
    output_path = '/Volumes/Other/project_structure.txt'  # Define the output file path.  
    return_folders_only = False
    max_depth = 2
    # List of directory names to ignore.  
    ignore_dirs = ['node_modules', 'lib', 'libs', '.git', 'venv', 'chrome.app', '.vscode', '.*']  
    # Define the file extensions of interest.  
    extensions_to_include = ('.py', '.json', '.php', '.csv')  # Define the file extensions of interest.  
    patterns = [r'links_(\d+)-(\d+)\.csv', r'part_\d+\.csv', r'links_\d+\.csv', r'(.*)_part_(\d+)\.csv']  # Define the patterns for identifying unique files.  
    special_dir_patterns = [r'run_\d+']  # Define patterns for special directories.  

    generate_project_structure(project_dir, ignore_dirs, extensions_to_include, patterns, special_dir_patterns, output_path, return_folders_only, max_depth)  # Generate the project structure.