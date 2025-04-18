# Project Structure Generator 1.3

Automatically generate a clean and organized project directory structure and code element documentation for developers managing large codebases. Ideal for creating clear overviews of project layouts and code components.  

## Purpose  

This script generates a structured representation of a project's directory and file hierarchy, along with detailed documentation of code elements such as functions and classes. It is designed for developers who need to document and understand the layout and codebase of large projects. The script ensures:  

- Directories and files are presented in a readable, tree-like format.  
- Specific directories can be ignored to focus on relevant project components.  
- Users can customize which files to include in the output.  
- Files with similar naming patterns are grouped to reduce clutter.  
- Functions and classes are extracted and documented for supported programming languages.  

### Pattern Logic  

The script uses pattern matching to list only the first and last files for each defined pattern within a folder. For example, if a folder contains multiple CSV files with incremental names (e.g., `links_1.csv`, `links_2.csv`), only the first and last are included to keep the output concise. The script also avoids repeating folders with the same depth and name.  

### Wildcard Patterns  

Directories in the ignore list support wildcard patterns for flexible matching. For example:  

- `*.cache` ignores any directory ending with `.cache`.  
- `.*` ignores all hidden directories starting with a `.`.  

## Features  

- **Directory Structure Generation**:  
  - Creates a tree-like representation of the project directory in a text file (`project_structure.txt`).  
  - Lists directories before files, sorted alphabetically.  
  - Uses ASCII characters for visual hierarchy.  
- **Directory Filtering**:  
  - Ignores specified directories using wildcard patterns (e.g., `node_modules`, `.git`).  
  - Excludes special directories matching defined patterns (e.g., `run_1`, `run_2`).  
- **File Filtering and Grouping**:  
  - Includes files with specified extensions or all files, based on configuration.  
  - Groups files with similar naming patterns, listing only the first and last matches per pattern.  
- **Function and Class Extraction**:  
  - Extracts functions and classes from Python (`.py`), PHP (`.php`), and JavaScript (`.js`) files.  
  - Captures function names, class names, methods, and associated comments.  
  - For PHP, extracts `/*** ... ***/` comments following function declarations.  
- **Code Documentation**:  
  - Generates a `functions.txt` file listing processed files, their language, and details of classes (with methods) and standalone functions.  
  - Includes total counts of classes, methods, and functions, along with comments and line numbers.  
- **Customization Options**:  
  - Option to output only folder names for a simplified view.  
  - Control over traversal depth to limit the directory structure output.  
  - Support for specifying languages to process for code extraction.  
- **Robust Handling**:  
  - Uses UTF-8 encoding for file reading with error handling for unreadable files.  
  - Validates specified languages and warns about unsupported ones.  

## Configuration  

1. Define the project directory by setting `project_dir`.  
2. Specify the output file paths for the directory structure (`project_structure.txt`) and code documentation (`functions.txt`).  
3. Customize the `ignore_dirs`, `extensions_to_include`, `patterns`, `special_dir_patterns`, and `languages` variables as needed.  
4. Use the `return_folders_only` parameter to output only folder names.  
5. Set the `max_depth` parameter to control the depth of the directory structure.  
6. Enable `include_all_files` to include all files or restrict to specific extensions.  

## Example Output  

### Directory Structure (`project_structure.txt`)  

```
project_root/
│   ├── project_structure_generator.py
├── config/
│   ├── update_files.py
│   ├── initial_setup/
│   │   └── structure.py
├── data/
│   ├── processed_files/
│   │   ├── Categories.json
│   │   ├── Combined_File.json
├── src/
│   ├── data_fetch/
│   │   └── fetch_feeds.py
│   ├── data_processing/
│   │   ├── combine_feeds.py
│   │   └── populate_reference_files.py
├── tests/
│   ├── test_combine_feeds.py
│   └── test_integration.py
├── woopoint/
│   └── woopoint.php
```

### Code Documentation (`functions.txt`)  

```
File: src/data_fetch/fetch_feeds.py (Language: Python)
  Total Functions: 2

  Function: fetch_data (Line 10)
  Function: parse_feed (Line 25)

File: woopoint/woopoint.php (Language: Php)
  Total Classes: 1
  Total Methods: 3
  Total Functions: 1

  Class: WooPoint
    Method: calculate_points
      *** Calculates customer points based on order total ***
    Method: save_points
      *** Saves points to the database ***
    Method: retrieve_points

  Function: initialize_woopoint (Line 15)
  Function Description: Initializes the WooPoint system
```