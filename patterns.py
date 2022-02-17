class RegexPreProcessor:
    rDefine = r"""
    \#define\s              # Match '#define '
    (?P<varName>[A-Z_]*)    # Capture group for pre-processor name
    (?P<nSpaces>\s*)\(      # Capture group for spaces between name and '('
    (?P<val>\d+)            # Capture group for any number of digits
    (?P<unsigned>[uU]?)\)   # Capture group to capture 'U' (zero or one times) and ')'
    """
    rMajor = r"""
    \#define\s                  # Match '#define '
    (?P<varName>[A-Z_]*MAJOR)   # Capture group for pre-processor name + 'MAJOR'
    (?P<nSpaces>\s*)\(          # Capture group for spaces between name and '('
    (?P<val>\d+)                # Capture group for any number of digits
    (?P<unsigned>[uU]?)\)       # Capture group to capture 'U' (zero or one times) and ')'
    """
    rMinor = r"""
    \#define\s              # Match '#define '
    (?P<varName>[A-Z_]*MINOR)    # Capture group for pre-processor name + 'MINOR'
    (?P<nSpaces>\s*)\(      # Capture group for spaces between name and '('
    (?P<val>\d+)            # Capture group for any number of digits
    (?P<unsigned>[uU]?)\)   # Capture group to capture 'U' (zero or one times) and ')'
    """
    rPatch = r"""
    \#define\s              # Match '#define '
    (?P<varName>[A-Z_]*PATCH)    # Capture group for pre-processor name + 'PATCH'
    (?P<nSpaces>\s*)\(      # Capture group for spaces between name and '('
    (?P<val>\d+)            # Capture group for any number of digits
    (?P<unsigned>[uU]?)\)   # Capture group to capture 'U' (zero or one times) and ')'
    """

class RegexDoxy:
    rMajor = r"PROJECT_NUMBER\s*=\s*(?P<val>\d+)\.(?:\d+)?\.(?:\*|\d+)"
    rMinor = r"PROJECT_NUMBER\s*=\s*(?:\d+\.)(?P<val>\d+)?\.(?:\*|\d+)"
    rPatch = r"PROJECT_NUMBER\s*=\s*(?:\d+)\.(?:\d+)?\.(?P<val>\*|\d+)"
    # rMajor = r"""
    # ^PROJECT_NUMBER\s*=\s*  # Match 'PROJECT_NUMBER'
    # (?P<val>\d+)\.                 # Capture group for major 1.xx.xx
    # (?:\d+)?\.              # Ignore capture group for minor xx.1.xx
    # (?:\*|\d+)$             # Ignore capture group for patch xx.xx.1
    # """
    # rMinor = r"""
    # ^PROJECT_NUMBER\s*=\s*  # Match 'PROJECT_NUMBER'
    # (?:\d+\.)               # Ignore group for major 1.xx.xx
    # (?P<val>\d+)?\.                # Capture group for minor xx.1.xx
    # (?:\*|\d+)$             # Ignore capture group for patch xx.xx.1
    # """
    # rPatch = r"""
    # ^PROJECT_NUMBER\s*=\s*  # Match 'PROJECT_NUMBER'
    # (?:\d+)\.               # Ignore capture group for major 1.xx.xx
    # (?:\d+)?\.              # Ignore capture group for minor xx.1.xx
    # (?P<val>\*|\d+)$               # Capture group for patch xx.xx.1
    # """
# rDoxyVersion = r"""
# ^PROJECT_NUMBER\s*=\s*  # Match 'PROJECT_NUMBER'
# (?P<major>\d+\.)        # Capture group for major 1.xx.xx
# (?P<minor>\d+\.)?       # Capture group for major xx.1.xx
# (?P<patch>\*|\d+)$      # Capture group for major xx.xx.1
# # ^PROJECT_NUMBER\s*=\s*(\d+\.)(\d+\.)?(\*|\d+)$

# PREPROCESSOR_REGEX = {
#     'major': rPreprocessorMajor,
#     'minor': rPreprocessorMinor,
#     'patch': rPreprocessorPatch
# }

# DOXY_REGEX = {
#     'major': rDoxyMajor,
#     'minor': rDoxyMinor,
#     'patch': rDoxyPatch
# }
