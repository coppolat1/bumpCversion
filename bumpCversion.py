import os
import re
import argparse
import configparser
from patterns import RegexDoxy, RegexPreProcessor
from exceptions import DoxyException
from typing import NamedTuple, Pattern

PART_TO_BUMP = ''

class ConfigStruct(NamedTuple):
    name: str
    path: str


def modify_revision(matchobj, action):
    """
    Caveats:
    Assumes the following named match groups exist: varName, nSpaces, val
    and name.
    """
    currentVer = int(matchobj.group('val'))
    retStr = ''
  
    if (action == 'zero'):
        change_bump_on_zero()
        newVer = 0
    elif (action == 'bump'):
        newVer = currentVer + 1
    else:
        raise ValueError("Invalid 'action' parameter " + str(action))


    try:
        retStr = "#define " + matchobj.group('varName') + matchobj.group('nSpaces') + \
        "(" + str(newVer) + matchobj.group('unsigned') + ")"
        return (str(retStr))
    except IndexError:
        print("WARNING: " + str(DoxyException(matchobj)))
        retStr = get_doxy_str(matchobj, newVer)
        pass

    return (str(retStr))


def change_bump_on_zero():
    global PART_TO_BUMP
    if PART_TO_BUMP == 'major':
        PART_TO_BUMP = 'minor'
    elif PART_TO_BUMP == 'minor':
        PART_TO_BUMP = 'patch'
    else:
        PART_TO_BUMP = 'patch'


def get_doxy_str(matchobj, newVer):
    doxyStr = matchobj.group(0)
    if PART_TO_BUMP == 'major':
        temp = '=' + str(newVer) + '.'
        reobj = re.compile(r'=\s*\d+\.', re.X)
        retStr = reobj.sub(temp, doxyStr)
    elif PART_TO_BUMP == 'minor':
        temp = '.' + str(newVer) + '.'
        reobj = re.compile(r'\.\d+\.', re.X)
        retStr = reobj.sub(temp, doxyStr)
    elif PART_TO_BUMP == 'patch':
        temp = '.' + str(newVer) 
        retStr = doxyStr.rpartition('.')[0] + temp #  GET THE PART OF A STRING BEFORE THE LAST OCCURRENCE OF '.'
    return str(retStr)


def bump_revision(matchobj):
    return modify_revision(matchobj, 'bump')


def zero_revision(matchobj):
    return modify_revision(matchobj, 'zero')


def get_major_minor_patch_str(string, Patterns):
    # get major
    matchMaj = re.search(Patterns.rMajor, string)
    # get minor
    matchMin = re.search(Patterns.rMinor, string)
    # get patch
    matchPat = re.search(Patterns.rPatch, string)
    
    try:
        majorVal = matchMaj.group('val')
        minorVal = matchMin.group('val')
        patchVal = matchPat.group('val')
    except AttributeError or UnboundLocalError:
        print("ERROR: No match for current version number, check convention: <major>.<minor>.<patch>")

    return str(majorVal + '.' + minorVal + '.' + patchVal)


def extant_file(x):
    """
    'Type' for argparse - checks that file exists but does not open.
    """
    if not os.path.exists(x):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(x))
    return x


def parse_args():
    """ Parse arguments and return them. """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config-file",
        required=False,
        help="Config file to read from. If this argument is not supplied \
              the program will check for the existence of a configuration \
              file with the name: \".bump.cfg\" in the current directory \
              and use it",
    )
    parser.add_argument(
        "version_file", metavar="version-file",
        nargs='?',
        type=extant_file,
        help="File that contains C library version information",
        default=None
        #help="File to change"
    )
    parser.add_argument(
        "part",
        choices=['major', 'minor', 'patch'],
        help="Part of the version to be bumped (major|minor|patch)"
    )
    parser.add_argument(
        "--dont-reset",
        action='store_true',
        help=("Don't reset the patch and/or minor to zero when bumping the"
              " major or minor versions")
    )
    parser.add_argument(
        "--component",
        required=False,
        help="A component, defined in the config file, of which to bump"
    )
    args = parser.parse_args()

    return args


def get_config(config_file):
    components = []  # [0] component name, [1] path to file to bump
    config = configparser.ConfigParser()

    # Check for config_file argument. If it doesn't exist, check
    # for a default configuration file in the CWD.
    if config_file is None:
        if os.path.exists('.bump.cfg'):
            config_file = '.bump.cfg'
        else:
            return False, []

    config_file_exists = os.path.exists(config_file)
    if not config_file_exists:
        print("Configuration does not exist!")
        return config_file_exists, []

    config.read(config_file)
    for section in config.sections():
        if config.has_option(section, 'filetobump'):
            components.append(ConfigStruct(section,
                                           config.get(section, 'filetobump')))
    return config_file_exists, components


# If a version file was specified on the CLI, use it. Otherwise,
# look for a configuration file.
def get_target_file(args):
    target_file = ""
    if args.version_file:
        target_file = args.version_file
        return target_file
    else:
        config_file_exists, cfg_components = get_config(args.config_file)

        if not config_file_exists:
            print("Nothing to do!")
            return

        for comp in cfg_components:
            if args.component == comp.name:
                print("Using component:", comp.name)
                # This will obviously only grab the first file.
                # TODO: Add ability for multiple files to be handled.
                target_file = comp.path
                break    
    return target_file


def get_component_patterns(args):
    print("Checking component for file type...")
    if args.component == "doxy": 
        print("Using Doxyfile...")
        Patterns = RegexDoxy()
        return Patterns
    else:
        print("Using '.h' file...")
        Patterns = RegexPreProcessor()
        return Patterns


def check_bump(args, content, Patterns, part_to_bump):
    if part_to_bump == 'major':
        # Bump major
        reobj = re.compile(Patterns.rMajor, re.X)
        content = reobj.sub(bump_revision, content)
        if not (args.dont_reset):
            # Zero minor
            reobj = re.compile(Patterns.rMinor, re.X)
            content = reobj.sub(zero_revision, content)
            # Zero patch
            reobj = re.compile(Patterns.rPatch, re.X)
            content = reobj.sub(zero_revision, content)
    elif part_to_bump == 'minor':
        # Bump minor
        reobj = re.compile(Patterns.rMinor, re.X)
        content = reobj.sub(bump_revision, content)
        if not (args.dont_reset):
            # Zero patch
            reobj = re.compile(Patterns.rPatch, re.X)
            content = reobj.sub(zero_revision, content)
    elif part_to_bump == 'patch':
        reobj = re.compile(Patterns.rPatch, re.X)
        content = reobj.sub(bump_revision, content)
    else:
        print('Skipping update')   
    return content 


def main():

    # Parse command line arguments
    args = parse_args()

    # gives us scope for part_to_bump when calling bump_revision and zero_revision
    part_to_bump = args.part # = major, minor, or patch
    global PART_TO_BUMP 
    PART_TO_BUMP = part_to_bump

    # get file we're interested in
    target_file = get_target_file(args)

    # Open file for reading
    with open(target_file, 'r', errors='ignore', encoding='utf-8') as f:
        content = f.read()

        # Check whether C or Doxy, returns Patterns for either C or Doxy file.
        Patterns = get_component_patterns(args)

        # Print version, before we bump it
        print("Pre-bump string:  ", get_major_minor_patch_str(content, Patterns))

        # Bump the revision based on the 'part' command line arg
        content = check_bump(args, content, Patterns, part_to_bump)

    # Write back to file with replaced contents
    print("Target file: " + target_file)
    with open(target_file, 'w', errors='ignore', encoding='utf-8') as f:
        f.write(content)

    # Print version, after we bump it
    print("Post-bump string:  ", get_major_minor_patch_str(content, Patterns))


if __name__ == '__main__':
    main()
