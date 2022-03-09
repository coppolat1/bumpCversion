import re

from exceptions import DoxyException, PreProcessorException


class SemanticVersionNumber(object):

    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def set(self, major, minor, patch):
        """Set version
        """
        self.major = major
        self.minor = minor
        self.patch = patch

    def bump(self, part, dont_reset):
        """Bump a semantic version number

        part  -- The part to bump
        reset -- Should we reset the lower parts when the higher when the
                 higher part is bumped
        """
        if (part == 'major'):
            self.major += 1
        elif (part == 'minor'):
            self.minor += 1
        elif (part == 'patch'):
            self.patch += 1

        if (not dont_reset):
            if (part == 'major'):
                self.minor = 0
                self.patch = 0
            elif (part == 'minor'):
                self.patch = 0

    def __str__(self):
        """String representation of this class
        """
        return str(str(self.major) + "." +
                   str(self.minor) + "." +
                   str(self.patch))


class Filetype():

    def __init__(self, args, target_file):
        self.args = args
        self.target_file = target_file
        self.version_number = SemanticVersionNumber(0, 0, 0)
        self.get_version_from_file()


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

    def get_version_from_file(self):
        content = ""
        # Open file for reading
        with open(self.target_file, 'r', errors='ignore', encoding='utf-8') as input:
            content = input.read()

        # Get match objects and save them
        self._match_obj_major = re.search(self.r_major, content, re.X)
        self._match_obj_minor = re.search(self.r_minor, content, re.X)
        self._match_obj_patch = re.search(self.r_patch, content, re.X)

        try:
            major_val = self._match_obj_major.group('val')
            minor_val = self._match_obj_minor.group('val')
            patch_val = self._match_obj_patch.group('val')
        except AttributeError:
            raise(PreProcessorException(Exception))

        self.version_number.set(int(major_val),
                                int(minor_val),
                                int(patch_val))

    def update_version_in_file(self):
        # Open file for reading
        with open(self.target_file, 'r', errors='ignore', encoding='utf-8') as input:
            content = input.read()

        # Build replacement strings
        major_repl = self.__build_replacement_string(self._match_obj_major,
                                                     self.version_number.major)
        minor_repl = self.__build_replacement_string(self._match_obj_minor,
                                                     self.version_number.minor)
        patch_repl = self.__build_replacement_string(self._match_obj_patch,
                                                     self.version_number.patch)

        # Substitute with new updated versions
        content = self._match_obj_major.re.sub(major_repl, content)
        content = self._match_obj_minor.re.sub(minor_repl, content)
        content = self._match_obj_patch.re.sub(patch_repl, content)

        # Write modified contents back to file
        with open(self.target_file, 'w', errors='ignore', encoding='utf-8') as input:
            input.write(content)

    def __build_replacement_string(self, match_obj, new_version):
        return ('#define ' +
                match_obj.group('varName') +
                match_obj.group('nSpaces') + '(' +
                str(new_version) +
                match_obj.group('unsigned') + ')')


class Doxy(Filetype):
    #   Define regex patterns
    r_pattern = r"PROJECT_NUMBER\s*=\s*(?P<major>\d+)\.(?P<minor>\d+)?\.(?P<patch>\*|\d+)"

    # initializes version based off regex
    def get_version_from_file(self):
        content = ""
        # Open file for reading
        with open(self.target_file, 'r', errors='ignore', encoding='utf-8') as input:
            content = input.read()

        # get version
        matchObj = re.search(self.r_pattern, content)

        try:
            majorVal = matchObj.group('major')
            minorVal = matchObj.group('minor')
            patchVal = matchObj.group('patch')
        except AttributeError:
            raise(DoxyException(Exception))

        self.version_number.set(int(majorVal),
                                int(minorVal),
                                int(patchVal))

    def update_version_in_file(self):
        file_contents = []
        with open(self.target_file, "r") as input:
            for line in input:
                file_contents.append(line)
        with open(self.target_file, "w", encoding='utf-8') as output:
            for line in file_contents:
                if 'PROJECT_NUMBER' in line and not line.startswith('#'):
                    temp = line.rpartition(
                        '=')[0] + line.rpartition('=')[1] + str(self.version_number) + '\n'
                    line = temp
                output.write(line)
