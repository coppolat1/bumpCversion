import os
import re
import argparse

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


def bump_revision_general(matchobj):
    """
    Caveats:
    Assumes the following named match groups exist: varName, nSpaces, val
    and name.
    """
    currentVer = int(matchobj.group('val'))
    retStr = "#define " + matchobj.group('varName') + matchobj.group('nSpaces') + "(" + \
        str(currentVer + 1) + matchobj.group('unsigned') + ")"

    return (str(retStr))


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
        "version_file", metavar="version-file",
        type=extant_file,
        help="File that contains C library version information."
    )
    parser.add_argument(
        "part",
        choices=['major', 'minor', 'patch'],
        help="Part of the version to be bumped (major|minor|patch)"
    )
    args = parser.parse_args()

    return args


def main():

    # Parse command line arguments
    args = parse_args()
    version_file = args.version_file
    partToBump = args.part

    # Open file for reading
    with open(version_file, 'r', errors='ignore', encoding='utf-8') as f:
        content = f.read()

    # Print version, before we bump it
    print("Pre-bump string:  ", get_major_minor_patch_str(content))

    # Bump the revision based on the 'part' command line arg
    if partToBump == 'major':
        reobj = re.compile(rPreprocessorMajor, re.X)
        content = reobj.sub(bump_revision_general, content)
    elif partToBump == 'minor':
        reobj = re.compile(rPreprocessorMinor, re.X)
        content = reobj.sub(bump_revision_general, content)
    elif partToBump == 'patch':
        reobj = re.compile(rPreprocessorPatch, re.X)
        content = reobj.sub(bump_revision_general, content)
    else:
        print('Skipping update')

    # Write back to file with replaced contents
    with open(version_file, 'w', errors='ignore', encoding='utf-8') as f:
        f.write(content)

    # Print version, after we bump it
    print("Post-bump string:  ", get_major_minor_patch_str(content))


if __name__ == '__main__':
    main()
