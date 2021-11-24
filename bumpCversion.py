import os
import re
import argparse
import configparser

rAnyPreprocessorDefine = r"""
\#define\s              # Match '#define '
(?P<varName>[A-Z_]*)    # Capture group for pre-processor name
(?P<nSpaces>\s*)\(      # Capture group for spaces between name and '('
(?P<val>\d+)            # Capture group for any number of digits
(?P<unsigned>[uU]?)\)   # Capture group to capture 'U' (zero or one times) and ')'
"""
rPreprocessorMajor = r"""
\#define\s                  # Match '#define '
(?P<varName>[A-Z_]*MAJOR)   # Capture group for pre-processor name + 'MAJOR'
(?P<nSpaces>\s*)\(          # Capture group for spaces between name and '('
(?P<val>\d+)                # Capture group for any number of digits
(?P<unsigned>[uU]?)\)       # Capture group to capture 'U' (zero or one times) and ')'
"""
rPreprocessorMinor = r"""
\#define\s              # Match '#define '
(?P<varName>[A-Z_]*MINOR)    # Capture group for pre-processor name + 'MINOR'
(?P<nSpaces>\s*)\(      # Capture group for spaces between name and '('
(?P<val>\d+)            # Capture group for any number of digits
(?P<unsigned>[uU]?)\)   # Capture group to capture 'U' (zero or one times) and ')'
"""
rPreprocessorPatch = r"""
\#define\s              # Match '#define '
(?P<varName>[A-Z_]*PATCH)    # Capture group for pre-processor name + 'PATCH'
(?P<nSpaces>\s*)\(      # Capture group for spaces between name and '('
(?P<val>\d+)            # Capture group for any number of digits
(?P<unsigned>[uU]?)\)   # Capture group to capture 'U' (zero or one times) and ')'
"""


def modify_revision(matchobj, action):
    """
    Caveats:
    Assumes the following named match groups exist: varName, nSpaces, val
    and name.
    """
    currentVer = int(matchobj.group('val'))

    if (action == 'zero'):
        newVer = 0
    elif (action == 'bump'):
        newVer = currentVer + 1
    else:
        raise ValueError("Invalid 'action' parameter " + str(action))

    retStr = "#define " + matchobj.group('varName') + matchobj.group('nSpaces') + \
        "(" + str(newVer) + matchobj.group('unsigned') + ")"

    return (str(retStr))


def bump_revision(matchobj):
    return modify_revision(matchobj, 'bump')


def zero_revision(matchobj):
    return modify_revision(matchobj, 'zero')


def get_major_minor_patch_str(string):
    # get major
    reMajor = re.compile(rPreprocessorMajor, re.X)
    matchMaj = reMajor.search(string)
    majorVal = matchMaj.group('val')
    # get minor
    reMinor = re.compile(rPreprocessorMinor, re.X)
    matchMin = reMinor.search(string)
    minorVal = matchMin.group('val')
    # get patch
    rePatch = re.compile(rPreprocessorPatch, re.X)
    matchPat = rePatch.search(string)
    patchVal = matchPat.group('val')

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
        help="Config file to read from (default: .bump.cfg)",
    )
    parser.add_argument(
        "version_file", metavar="version-file",
        nargs='*',
        type=extant_file,
        help="File that contains C library version information",
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
    args = parser.parse_args()

    return args


def get_config(config_file):
    components = []  # [0] component name, [1] path to file to bump
    config = configparser.ConfigParser()

    if config_file is None:
        return False, []

    config_file_exists = os.path.exists(config_file)
    if not config_file_exists:
        print("Configuration does not exist!")
        return config_file_exists, []

    config.read(config_file)
    for section in config.sections():
        if config.has_option(section, 'filetobump'):
            components.append((section, config.get(section, 'filetobump')))
    return config_file_exists, components

def replace_version_single_file(args):
    version_file = args.version_file
    partToBump = args.part

    # Open file for reading
    with open(version_file, 'r', errors='ignore', encoding='utf-8') as f:
        content = f.read()

    # Print version, before we bump it
    print("Pre-bump string:  ", get_major_minor_patch_str(content))

    # Bump the revision based on the 'part' command line arg
    if partToBump == 'major':
        # Bump major
        reobj = re.compile(rPreprocessorMajor, re.X)
        content = reobj.sub(bump_revision, content)
        if not (args.dont_reset):
            # Zero minor
            reobj = re.compile(rPreprocessorMinor, re.X)
            content = reobj.sub(zero_revision, content)
            # Zero patch
            reobj = re.compile(rPreprocessorPatch, re.X)
            content = reobj.sub(zero_revision, content)
    elif partToBump == 'minor':
        # Bump minor
        reobj = re.compile(rPreprocessorMinor, re.X)
        content = reobj.sub(bump_revision, content)
        if not (args.dont_reset):
            # Zero patch
            reobj = re.compile(rPreprocessorPatch, re.X)
            content = reobj.sub(zero_revision, content)
    elif partToBump == 'patch':
        reobj = re.compile(rPreprocessorPatch, re.X)
        content = reobj.sub(bump_revision, content)
    else:
        print('Skipping update')

    # Write back to file with replaced contents
    with open(version_file, 'w', errors='ignore', encoding='utf-8') as f:
        f.write(content)

    # Print version, after we bump it
    print("Post-bump string:  ", get_major_minor_patch_str(content))



def main():

    # Parse command line arguments
    args = parse_args()

    '''
    If we have a single version file, passed in as an arg, there is no config
    file. Therefore, we'll call the 'single_file' variety of this function.
    TODO: Consolidate these into the same function.
    '''
    if args.version_file is not None:
        replace_version_single_file(args)
    else:
        config_file_exists, cfg_component_list = get_config(args.config_file)


if __name__ == '__main__':
    main()
