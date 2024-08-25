```markdown
# Project Structure Generator  

Automatically generate a clean and organized project directory structure for documentation and analysis. Perfect for developers needing a clear overview of large codebases.  

## Purpose  

The purpose of this script is to generate a structured and formatted representation of a project's directory and file hierarchy. This script is particularly useful for developers who need to document and understand the layout of a large project. It ensures that:  

- Directories and files are presented in a readable and organized manner.  
- Special handling is provided to ignore specific directories.  
- Users can define which files to include in the output.  
- Files with similar naming patterns are grouped together.  

### Pattern Logic  

The pattern logic allows listing only one of each of the values defined as a pattern. For example, if you have 10 CSV files in a folder that increment in value, instead of listing all of them (which would make the output very long), it will list just one for each folder. The output will not repeat or output folders that have the same depth and final folder name.  

### Wildcard Patterns  

Directories in the ignore list can have wildcard patterns which will be correctly interpreted and matched. For example:  

- `*.cache` will ignore any directory ending with `.cache`.  
- `.*` will ignore all hidden directories starting with a `.`.  

## Features  

- Ignores specified directories  
- Groups files with similar naming patterns  
- Lists directories before files within each directory  
- Handles special directory naming patterns (e.g., `run_1`, `run_2`)  
- Customizable file extensions and patterns  
- Wildcard patterns  
- Option to output only folder names for a simplified view.  
- Control over the depth level of the output to limit how deep the directory structure is represented.  
- Uses the defined project directory name as the base in the output structure.  

## Configuration  

1. Define the project directory of the project by updating `project_dir`.  
2. Define the output file path by updating `output_path`.  
3. Customize the `ignore_dirs`, `extensions_to_include`, and `patterns` variables in the script as needed.  
4. Use the parameter `return_folders_only` in the `generate_project_structure` function to output only folder names.  
5. Set a `max_depth` parameter to control how deep the output structure should go.  

## Example Output  

The script generates a text file (`project_structure.txt`) with the following format:  

project_root/  
│   ├── project_structure_generator.py  
├── config/  
│   ├── update_files.py  
│   ├── initial_setup/  
│   │   └── structure.py  
│   │  
├── data/  
│   ├── processed_files/  
│   │   ├── Categories.json  
│   │   ├── Combined_File.json  
├── src/  
│   ├── data_fetch/  
│   │   └── fetch_feeds.py  
│   │  
│   ├── data_processing/  
│   │   ├── combine_feeds.py  
│   │   └── populate_reference_files.py  
├── tests/  
│   ├── test_combine_feeds.py  
│   └── test_integration.py  
│  
├── woopoint/  
│   └── woopoint.php
```
