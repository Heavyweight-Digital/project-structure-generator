# Changelog  

## Version 1.4  

- Added new features:  
  - Support for ignoring specific files or file patterns using the `ignore_files` parameter.  
  - New `combined_structure.txt` output file that combines project structure and function/class information.  
  - Boolean flags (`export_structure`, `export_functions`, `export_combined`) to control which output files are generated.  
  - Language filtering to process only languages with extensions in `extensions_to_include`.  
  - Centralized configuration using constants for improved maintainability.  
  - Output files saved to a `docs` directory (marked as legacy).  

## Version 1.3  

- Added function and class extraction:  
  - Extracts functions and classes from Python (`.py`), PHP (`.php`), and JavaScript (`.js`) files.  
  - Captures function names, class names, methods, and associated comments.  
  - For PHP, extracts `/*** ... ***/` comments immediately following function opening braces.  
- Introduced new output file (`functions.txt`):  
  - Lists processed files with their language, total counts of classes, methods, and functions.  
  - Details classes (with methods) and standalone functions, including comments and line numbers.  
- Added language support:  
  - Supports Python, PHP, and JavaScript with language-specific regex patterns for function and class extraction.  
  - Validates specified languages and warns about unsupported ones.  
- Enhanced file processing:  
  - Processes files for function/class extraction if they match specified language extensions.  
  - Uses UTF-8 encoding for file reading with error handling for unreadable files.  
- Improved PHP handling:  
  - Distinguishes between standalone functions and class methods in PHP files.  
  - Extracts classes and their methods, associating comments correctly.  
- Added new parameters:  
  - `languages` parameter to specify languages for function/class extraction.  
  - `functions_file` parameter to set the output path for `functions.txt`.  
- Updated configuration:  
  - Default settings now include a broader `max_depth` (18) and focus on `.php` and `.js` extensions.  
  - Set `include_all_files` to `True` by default for broader file inclusion.  

## Version 1.2  

- Added new feature:  
  - `include_all_files` parameter, allowing the option to include all files regardless of extensions when set to `True`.  
  - If `include_all_files` is `False`, only files matching the specified extensions will be included.  
  - Updated file-matching logic to accommodate the new parameter, offering more flexibility in file selection.  

## Version 1.1  

- Added new functionalities:  
  - Option to output only folder names to simplify the directory view.  
  - Control over the depth level of the output, allowing users to specify how deep the directory structure can go.  
  - Updated the function signature to include `return_folders_only` and `max_depth` parameters.  
  - Changed the output format: Instead of using "project_root/" in the output file, the defined project directory is now used as the base in the output.  

## Version 1.0  

- Initial release with the following features:  
  - Ignores specified directories  
  - Groups files with similar naming patterns  
  - Lists directories before files within each directory  
  - Handles special directory naming patterns (e.g., `run_1`, `run_2`)  
  - Customizable file extensions and patterns  
  - Wildcard patterns supported for directory ignores.