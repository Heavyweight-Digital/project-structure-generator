# Project Structure Generator

Automatically generate a clean and organized project directory structure for documentation and analysis. Perfect for developers needing a clear overview of large codebases.

## Purpose

The purpose of this script is to generate a structured and formatted representation of a project's directory and file hierarchy. This script is particularly useful for developers who need to document and understand the layout of a large project. It ensures that:

- Directories and files are presented in a readable and organized manner.
- Special handling is provided to ignore specific directories and files.
- Users can define which files to include in the output.
- Files with similar naming patterns are grouped together.
- Function and class information, including file descriptions, is extracted and documented.

### Pattern Logic

The pattern logic allows listing only one of each of the values defined as a pattern. For example, if you have 10 CSV files in a folder that increment in value, instead of listing all of them (which would make the output very long), it will list just one for each folder. The output will not repeat or output folders that have the same depth and final folder name.

### Wildcard Patterns

Directories and files in the ignore lists can have wildcard patterns which will be correctly interpreted and matched. For example:

- `*.cache` will ignore any directory or file ending with `.cache`.
- `.*` will ignore all hidden directories or files starting with a `.`.

## Features

- Ignores specified directories and files using wildcard patterns.
- Groups files with similar naming patterns for concise output.
- Lists directories before files within each directory for clarity.
- Handles special directory naming patterns (e.g., `run_1`, `run_2`).
- Customizable file extensions, file patterns, and languages for processing.
- Option to output only folder names for a simplified directory view.
- Control over the depth level of the output to limit directory structure representation.
- Uses the defined project directory name as the base in the output structure.
- Extracts functions and classes from Python (`.py`), PHP (`.php`), and JavaScript (`.js`) files.
- Captures function names, class names, methods, associated comments, and line numbers.
- Extracts file descriptions for PHP and JavaScript files using predefined regex patterns.
- Generates multiple output files:
  - `project_structure.txt`: Directory and file hierarchy.
  - `functions.txt`: Function, class, and file description details.
  - `combined_structure.txt`: Combined structure with function, class, and file description data.
- Selective output generation using boolean flags (`EXPORT_STRUCTURE`, `EXPORT_FUNCTIONS`, `EXPORT_COMBINED`).
- Dynamic project directory configuration based on the script's location.
- Automatically creates the documentation directory if it does not exist.
- Supports additional file extensions (e.g., `.php`, `.css`) for inclusion.
- Language-specific regex patterns for accurate function and class extraction.
- Validates specified languages and warns about unsupported ones.
- Processes files with UTF-8 encoding and handles unreadable files gracefully.
- Improved PHP handling to distinguish between standalone functions and class methods.

## Configuration

1. Define the project directory automatically using `PROJECT_DIR` (set to the script's directory).
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
   - `EXTENSIONS_TO_INCLUDE`: File extensions to include (e.g., `.js`, `.php`, `.css`).
   - `PATTERNS`: Patterns for grouping similar files.
   - `SPECIAL_DIR_PATTERNS`: Patterns for special directories.
   - `LANGUAGES`: Languages to process for function/class extraction (e.g., `python`, `php`, `javascript`).
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
File Description: Script for fetching and parsing external API data  
  Function: fetch_data (Line 10)  
  - Function Description: Fetches data from external API  
  Function: parse_response (Line 25)  
  - Function Description: Parses API response into JSON  

File: woopoint/woopoint.php (php)  
Total Classes: 1  
Total Methods: 3  
File Description: Main class for WooCommerce point management  
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
  File Description: Script for fetching and parsing external API data  
    Function: fetch_data (Line 10)  
    - Function Description: Fetches data from external API  
    Function: parse_response (Line 25)  
    - Function Description: Parses API response into JSON  

  File: woopoint/woopoint.php (php)  
  Total Classes: 1  
  Total Methods: 3  
  File Description: Main class for WooCommerce point management  
    Class: WooPoint  
      Function: __construct  
      - Function Description: Initializes the WooPoint class  
      Function: process_order  
      - Function Description: Processes customer orders  
      Function: update_stock  
      - Function Description: Updates inventory stock levels  
```