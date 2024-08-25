```markdown
# Changelog  

## Version 1.0  

- Initial release with the following features:  
  - Ignores specified directories  
  - Groups files with similar naming patterns  
  - Lists directories before files within each directory  
  - Handles special directory naming patterns (e.g., `run_1`, `run_2`)  
  - Customizable file extensions and patterns  
  - Wildcard patterns supported for directory ignores.  

## Version 1.1  

- Added new functionalities:  
  - Option to output only folder names to simplify the directory view.  
  - Control over the depth level of the output, allowing users to specify how deep the directory structure can go.  
  - Updated the function signature to include `return_folders_only` and `max_depth` parameters.  
  - Changed the output format: Instead of using "project_root/" in the output file, the defined project directory is now used as the base in the output.  
```
