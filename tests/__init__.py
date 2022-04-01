# file empty but required
'''
    Sometimes tests placed in subfolders aren't 
    discovered because such test files cannot be imported.
    To make them importable, 
    create an empty file named init.py in that folder.
    https://stackoverflow.com/questions/67164367/pytest-fails-due-to-modulenotfounderror-but-works-when-using-python-m-pytest
'''
