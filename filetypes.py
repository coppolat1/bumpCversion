import re

from exceptions import DoxyException, PreProcessorException


class Filetype():

    version = ["0", "0", "0"]  # [major, minor, patch]
    # Namespace(config_file='./tests/.bump.cfg', version_file=None, part='minor', dont_reset=False, component='naibrd')
    args = None
    target_file = None  # init as None

    def __init__(self, args, target_file):
        self.args = args
        self.target_file = target_file
        self.init_version()

    def set_version(self, major, minor, patch):
        self.version[0] = major
        self.version[1] = minor
        self.version[2] = patch

    # return content with bumped version

    def bump(self, part_to_bump):
        if part_to_bump == 'major':
            self.version[0] = str(int(self.version[0]) + 1)
            if not(self.args.dont_reset):
                self.version[1] = "0"
                self.version[2] = "0"
        elif part_to_bump == 'minor':
            self.version[1] = str(int(self.version[1]) + 1)
            if not(self.args.dont_reset):
                self.version[2] = "0"
        elif part_to_bump == 'patch':
            self.version[2] = str(int(self.version[2]) + 1)

    def version_tostr(self):
        return '.'.join(self.version)


class PreProcessor(Filetype):
    #   Define regex patterns
    r_major = r"""
    \#define\s                  # Match '#define '
    (?P<varName>[A-Z_]*MAJOR)   # Capture group for pre-processor name + 'MAJOR'
    (?P<nSpaces>\s*)\(          # Capture group for spaces between name and '('
    (?P<val>\d+)                # Capture group for any number of digits
    (?P<unsigned>[uU]?)\)       # Capture group to capture 'U' (zero or one times) and ')'
    """
    r_minor = r"""
    \#define\s              # Match '#define '
    (?P<varName>[A-Z_]*MINOR)    # Capture group for pre-processor name + 'MINOR'
    (?P<nSpaces>\s*)\(      # Capture group for spaces between name and '('
    (?P<val>\d+)            # Capture group for any number of digits
    (?P<unsigned>[uU]?)\)   # Capture group to capture 'U' (zero or one times) and ')'
    """
    r_patch = r"""
    \#define\s              # Match '#define '
    (?P<varName>[A-Z_]*PATCH)    # Capture group for pre-processor name + 'PATCH'
    (?P<nSpaces>\s*)\(      # Capture group for spaces between name and '('
    (?P<val>\d+)            # Capture group for any number of digits
    (?P<unsigned>[uU]?)\)   # Capture group to capture 'U' (zero or one times) and ')'
    """
    r_var = r'#define\s*([A-Z_]*[VERSION_MAJOR|VERSION_MINOR|VERSION_PATCH])'

    # initializes version based off regex
    def init_version(self):
        content = ""
        # Open file for reading
        with open(self.target_file, 'r', errors='ignore', encoding='utf-8') as input:
            content = input.read()

        # get major
        matchMaj = re.search(self.r_major, content, re.X)
        # get minor
        matchMin = re.search(self.r_minor, content, re.X)
        # get patch
        matchPat = re.search(self.r_patch, content, re.X)

        try:
            majorVal = matchMaj.group('val')
            minorVal = matchMin.group('val')
            patchVal = matchPat.group('val')
        except AttributeError:
            raise(PreProcessorException(Exception))

        self.set_version(majorVal, minorVal, patchVal)

    def overwrite_version(self):
        file_contents = []
        with open(self.target_file, "r") as input:
            for line in input:
                file_contents.append(line)
        with open(self.target_file, "w", encoding='utf-8') as output:
            for line in file_contents:
                matchObj = re.search(self.r_var, line, re.X)
                if matchObj != None: # preprocessor name ends in VERSION_MAJOR|VERSION_MINOR|VERSION_PATCH
                    if 'MAJOR' in line:
                        line = self.replace_part(self.version[0], line)
                    elif 'MINOR' in line:
                        line = self.replace_part(self.version[1], line)
                    elif 'PATCH' in line:
                        line = self.replace_part(self.version[2], line)
                output.write(line)

    def replace_part(self, part_num, line):
        line = re.sub(r'(\d+)', part_num, line)  # change contents
        return line


class Doxy(Filetype):
    #   Define regex patterns
    r_pattern = r"PROJECT_NUMBER\s*=\s*(?P<major>\d+)\.(?P<minor>\d+)?\.(?P<patch>\*|\d+)"

    # initializes version based off regex
    def init_version(self):
        content = ""
        # Open file for reading
        with open(self.target_file, 'r', errors='ignore', encoding='utf-8') as input:
            content = input.read()

        # get version
        version = re.search(self.r_pattern, content)

        try:
            majorVal = version.group('major')
            minorVal = version.group('minor')
            patchVal = version.group('patch')
        except AttributeError:
            raise(DoxyException(Exception))

        self.set_version(majorVal, minorVal, patchVal)

    def overwrite_version(self):
        file_contents = []
        with open(self.target_file, "r") as input:
            for line in input:
                file_contents.append(line)
        with open(self.target_file, "w", encoding='utf-8') as output:
            for line in file_contents:
                if 'PROJECT_NUMBER' in line and not line.startswith('#'):
                    temp = line.rpartition(
                        '=')[0] + line.rpartition('=')[1] + '.'.join(self.version) + '\n'
                    line = temp
                output.write(line)
