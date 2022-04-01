# bumpCversion

## Overview

Development of a CLI version bump utility. Given a file containing some version number `<major>.<minor>.<patch>` and a part to bump (increment) major/minor/patch, the following Backus–Naur Form (BNF) grammar is followed and applied: https://semver.org/spec/v2.0.0.html

## Usage
An exe is located in the `.\bin` folder.
```
$ python bumpCversion.py --help
Usage: bumpCversion.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  bump             Bump version numbers from files specified in config
  display-version  Print out all components respective versions
  dry-run          Print out current and expected versions (without...
```
Specify a `Command` followed by `--help` to see usage:
```
$ python bumpCversion.py bump --help
Usage: bumpCversion.py bump [OPTIONS] CONFIG COMPONENT PART

  Bump version numbers from files specified in config

Arguments:
  CONFIG     Configuration file to read from. If this argument is
             not supplied the program will check for the existence of a
             configuration file in the CWD  [required]
  COMPONENT  A component defined in the config file, of which to bump
             [required]
  PART       Part to bump: major, minor, patch  [required]

Options:
  --reset / --no-reset  Reset the patch and/or minor to zero when bumping the
                        higher parts  [default: no-reset]
  --help                Show this message and exit.
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
    - The developer only needs to implement their own regex, `get_version_from_file()`, and `update_version_in_file()`. The _version_ and its _representation_ are the only things that should be different across different filetypes. 
- `bumpCversion.py` should not have to be changed.
- `exceptions.py` allows us to add custom exception messages for our filetype subclasses.
- If a new executable is needed, create a new executable by running `.\build-exe.ps1` in Powershell. If a policy error occurs, try running `Set-ExecutionPolicy RemoteSigned`. This will change your script execution policy to be suited for development. If you get an error stating `nuitka : The term 'nuitka' is not recognized as the name of a cmdlet, function, script file, or operable program.`, go back to your bash terminal and run `pip install niutka`.

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
Note that (usually) `"LIBNAME" == args.component` 

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
