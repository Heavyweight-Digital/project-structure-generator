# Project Structure Generator

Automatically generate a clean and organized project directory structure for documentation and analysis. Perfect for developers needing a clear overview of large codebases.

## Purpose

The purpose of this script is to generate a structured and formatted representation of a project's directory and file hierarchy. This script is particularly useful for developers who need to document and understand the layout of a large project. It ensures that:

- Directories and files are presented in a readable and organized manner.
- Special handling is provided to ignore specific directories and files.
- Users can define which files to include in the output.
- Files with similar naming patterns are grouped together.
- Function and class information is extracted and documented.

### Pattern Logic

The pattern logic allows listing only one of each of the values defined as a pattern. For example, if you have 10 CSV files in a folder that increment in value, instead of listing all of them (which would make the output very long), it will list just one for each folder. The output will not repeat or output folders that have the same depth and final folder name.

### Wildcard Patterns

Directories and files in the ignore lists can have wildcard patterns which will be correctly interpreted and matched. For example:

- `*.cache` will ignore any directory or file ending with `.cache`.
- `.*` will ignore all hidden directories or files starting with a `.`.

## Features

- Ignores specified directories and files.
- Groups files with similar naming patterns.
- Lists directories before files within each directory.
- Handles special directory naming patterns (e.g., `run_1`, `run_2`).
- Customizable file extensions, file patterns, and languages for processing.
- Wildcard patterns for directories and files.
- Option to output only folder names for a simplified view.
- Control over the depth level of the output to limit how deep the directory structure is represented.
- Uses the defined project directory name as the base in the output structure.
- Extracts functions and classes from Python, PHP, and JavaScript files, with detailed output.
- Generates multiple output files: project structure, function/class details, and a combined structure with functions.
- Selective output generation for structure, functions, or combined files.

## Configuration

1. Define the project directory by updating `PROJECT_DIR`.
2. Specify the documentation directory with `DOCUMENTATION_DIR` (used for output files).
3. Set output file paths:
   - `OUTPUT_FILE` for the project structure (`project_structure.txt`).
   - `FUNCTIONS_FILE` for function and class details (`functions.txt`).
   - `COMBINED_FILE` for combined structure and function data (`combined_structure.txt`).
4. Configure export options:
   - `EXPORT_STRUCTURE`: Enable/disable project structure output.
   - `EXPORT_FUNCTIONS`: Enable/disable function/class output.
   - `EXPORT_COMBINED`: Enable/disable combined output.
5. Customize the following variables:
   - `IGNORE_DIRS`: List of directories or patterns to ignore.
   - `IGNORE_FILES`: List of files or patterns to ignore.
   - `EXTENSIONS_TO_INCLUDE`: File extensions to include.
   - `PATTERNS`: Patterns for grouping similar files.
   - `SPECIAL_DIR_PATTERNS`: Patterns for special directories.
   - `LANGUAGES`: Languages to process for function/class extraction.
6. Use the `RETURN_FOLDERS_ONLY` parameter to output only folder names.
7. Set `MAX_DEPTH` to control how deep the output structure should go.
8. Set `INCLUDE_ALL_FILES` to include all files or only those matching specified extensions.

## Example Output

The script generates text files with the following formats:

### project_structure.txt

```
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

### functions.txt

```
File: src/data_fetch/fetch_feeds.py (python)  
Total Functions: 2  
  Function: fetch_data (Line 10)  
  - Function Description: Fetches data from external API  
  Function: parse_response (Line 25)  
  - Function Description: Parses API response into JSON  

File: woopoint/woopoint.php (php)  
Total Classes: 1  
Total Methods: 3  
  Class: WooPoint  
    Function: __construct  
    - Function Description: Initializes the WooPoint class  
    Function: process_order  
    - Function Description: Processes customer orders  
    Function: update_stock  
    - Function Description: Updates inventory stock levels  
```

### combined_structure.txt

```
Project Structure:  
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

File Structure:  
  File: src/data_fetch/fetch_feeds.py (python)  
  Total Functions: 2  
    Function: fetch_data (Line 10)  
    - Function Description: Fetches data from external API  
    Function: parse_response (Line 25)  
    - Function Description: Parses API response into JSON  

  File: woopoint/woopoint.php (php)  
  Total Classes: 1  
  Total Methods: 3  
    Class: WooPoint  
      Function: __construct  
      - Function Description: Initializes the WooPoint class  
      Function: process_order  
      - Function Description: Processes customer orders  
      Function: update_stock  
      - Function Description: Updates inventory stock levels  
```