# bumpCversion

## Overview

Development of a CLI version bump utility. Given a file containing some version number `<major>.<minor>.<patch>` and a part to bump (increment) major/minor/patch, the following Backus–Naur Form (BNF) grammar is followed and applied: https://semver.org/spec/v2.0.0.html

## Usage
```
usage: bumpCversion.exe [-h] [--config-file CONFIG_FILE] [--dont-reset] [--component COMPONENT] [version-file] {major,minor,patch}

positional arguments:
  version-file          File that contains C library version information
  {major,minor,patch}   Part of the version to be bumped (major|minor|patch)

optional arguments:
  -h, --help            show this help message and exit
  --config-file CONFIG_FILE
                        Config file to read from. If this argument is not supplied the program will check for the existence of a configuration file with the name: ".bump.cfg" in the
                        current directory and use it
  --dont-reset          Don't reset the patch and/or minor to zero when bumping the major or minor versions
  --component COMPONENT
                        A component, defined in the config file, of which to bump
```
Example config file :
```
# Component name
[naibrd]
# Path to files to replace version number in. ()
filesToBump = ./tests/sample-input-file.h, ./tests/Doxyfile

[naibsp]
filesToBump = ./tests/sample-input-file1.h
```
_Notice `filesToBump` is a comma delimited list of paths._


## Development
- `filetypes.py` contains a `Filetype` parent class and its subclasses. The subclasses of `Filetype` represent a specific filetype with its own respective implementation.
    - The developer only needs to implement their own regex, `init_version(self)`, and `overwrite_version(self)`. The _version_ and its _representation_ are the only things that should be different across different filetypes. 
- `bumpCversion.py` should not have to be changed.
- `exceptions.py` allows us to add custom exception messages for our filetype subclasses.

## Support & Representations

### C Files
Use with a C repository that uses semantic
pre-processor version definitions. Where a version `1.2.0` is represented in a
header file as:
```
...
#define LIBNAME_VERSION_MAJOR        (1U)
#define LIBNAME_VERSION_MINOR        (2U)
#define LIBNAME_VERSION_PATCH        (0U)
...
```

### Doxyfile
Use with a set of Doxy files where version `18.0.0` is represented in Doxyfile as:
```
...
# The PROJECT_NUMBER tag can be used to enter a project or revision number. This
# could be handy for archiving the generated documentation or if some version
# control system is used.
PROJECT_NUMBER =18.0.0
...
```
