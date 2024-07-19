```markdown
# Project Structure Generator

Automatically generate a clean and organized project directory structure for documentation and analysis. Perfect for developers needing a clear overview of large codebases.

## Features

- Ignores specified directories
- Groups files with similar naming patterns
- Lists directories before files within each directory
- Handles special directory naming patterns (e.g., `run_1`, `run_2`)
- Customizable file extensions and patterns
- Wildcard Patterns


## Wildcard Patterns  

- Directories in the ignore list can have wildcard patterns which will be correctly interpreted and matched.  
- For example, `*.cache` will ignore any directory ending with `.cache`.  
- Another example, `.*` will ignore all hidden directories starting with a `.`.  

## Configuration

1. Define the project directory of the project by updating `project_dir`.
2. Define the output file path by updating `output_path`.
3. Customize the `ignore_dirs`, `extensions_to_include`, and `patterns` variables in the script as needed.

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