Python script that will parse through a Python source file, extract each top-level function, and save them into separate files. The script will then create a `main.py` file that imports all of these functions.

Here's a simple Python script that performs the described task. Please note that this script assumes that your functions are not nested within classes or other functions and that your source file is not doing anything unusual with source code encoding or manipulation.


1. This script will not necessarily capture and handle all complex refactoring cases, especially those involving class methods, nested functions, and decorators.
2. All functions will get the same set of imports from the original file, which might not be necessary and could lead to unused import warnings.
3. The use of the `ast` since parsing the file as text may not be robust enough to handle complex cases of code structuring or syntax.
4. The `main.py` simply imports all functions, but does not replicate any imperative code that existed in the original file; additional logic might be required for a complete refactor.