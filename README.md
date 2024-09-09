## Overview ##
A really simple python program to visualize dependencies with .asmdef files, especially useful for 
resolving circular dependencies.<br>

## Arguments ##
Command line arguments are required to point the script to your project directory, optional
arguments are provided to refine your search.

<root_path>: The root directory where .asmdef files are searched for.
--ns_whitelist <namespace1,namespace2,...> (optional): A comma-separated list of namespaces to whitelist. All other namespaces will be ignored.