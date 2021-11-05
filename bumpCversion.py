import re

test_str = """
#define LIBNAME_VERSION_MAJOR        (2)
#define LIBNAME_VERSION_MINOR        (4U)
#define LIBNAME_VERSION_PATCH        (0u)
"""
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


print("Pre-bump string:  ", test_str)
val = input("Bump major, minor or patch? ")

if (val == 'major'):
    reobj = re.compile(rPreprocessorMajor, re.X)
    rep = reobj.sub(bump_revision_general, test_str)
elif (val == 'minor'):
    reobj = re.compile(rPreprocessorMinor, re.X)
    rep = reobj.sub(bump_revision_general, test_str)
elif (val == 'patch'):
    reobj = re.compile(rPreprocessorPatch, re.X)
    rep = reobj.sub(bump_revision_general, test_str)
else:
    print('bad input')

print(rep)
