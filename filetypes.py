import re

from exceptions import DoxyException, PreProcessorException


class SemanticVersionNumber(object):

    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def bump(self, part, reset):
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

        if reset:
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


class Filetype(object):

    def __init__(self, target_file):

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

    def get_version_from_file(self):
        content = ""
        # Open file for reading
        with open(self.target_file, 'r', errors='ignore', encoding='utf-8', newline='') as input:
            content = input.read()

        # Get match objects
        match_obj_major = re.search(self.r_major, content, re.X)
        match_obj_minor = re.search(self.r_minor, content, re.X)
        match_obj_patch = re.search(self.r_patch, content, re.X)

        try:
            major_val = match_obj_major.group('val')
            minor_val = match_obj_minor.group('val')
            patch_val = match_obj_patch.group('val')
        except AttributeError:
            raise(PreProcessorException(Exception))

        self.version_number = SemanticVersionNumber(int(major_val),
                                                    int(minor_val),
                                                    int(patch_val))

    def update_version_in_file(self):
        # Open file for reading
        with open(self.target_file, 'r', errors='ignore', encoding='utf-8', newline='') as input:
            content = input.read()

        # Get match objects
        match_obj_major = re.search(self.r_major, content, re.X)
        match_obj_minor = re.search(self.r_minor, content, re.X)
        match_obj_patch = re.search(self.r_patch, content, re.X)

        # Build replacement strings
        major_repl = self.__build_replacement_string(match_obj_major,
                                                     self.version_number.major)
        minor_repl = self.__build_replacement_string(match_obj_minor,
                                                     self.version_number.minor)
        patch_repl = self.__build_replacement_string(match_obj_patch,
                                                     self.version_number.patch)

        # Substitute with new updated versions
        content = match_obj_major.re.sub(major_repl, content)
        content = match_obj_minor.re.sub(minor_repl, content)
        content = match_obj_patch.re.sub(patch_repl, content)

        # Write modified contents back to file
        with open(self.target_file, 'w', errors='ignore', encoding='utf-8', newline='') as input:
            input.write(content)

    def __build_replacement_string(self, match_obj, new_version):
        return ('#define ' +
                match_obj.group('varName') +
                match_obj.group('nSpaces') + '(' +
                str(new_version) +
                match_obj.group('unsigned') + ')')


class Doxy(Filetype):
    #   Define regex patterns
    r_pattern = r"PROJECT_NUMBER(?P<n_spaces>\s*)=\s*(?P<major>\d+)\.(?P<minor>\d+)?\.(?P<patch>\*|\d+)"
    num_spaces = ''

    # initializes version based off regex
    def get_version_from_file(self):
        content = ""
        # Open file for reading
        with open(self.target_file, 'r', errors='ignore', encoding='utf-8', newline='') as input:
            content = input.read()

        # get version
        matchObj = re.search(self.r_pattern, content)

        try:
            self.num_spaces = matchObj.group('n_spaces')
            major_val = matchObj.group('major')
            minor_val = matchObj.group('minor')
            patch_val = matchObj.group('patch')
        except AttributeError:
            raise(DoxyException(Exception))

        self.version_number = SemanticVersionNumber(int(major_val),
                                                    int(minor_val),
                                                    int(patch_val))

    def update_version_in_file(self):
        # Open file for reading
        with open(self.target_file, 'r', errors='ignore', encoding='utf-8', newline='') as input:
            content = input.read()

        # Build replacement string
        version_repl = self.__build_replacement_string(self.version_number)

        # Substitute version
        content = re.sub(self.r_pattern, version_repl, content)

        # Write replaced contents back to file
        with open(self.target_file, 'w', errors='ignore', encoding='utf-8', newline='') as input:
            input.write(content)

    def __build_replacement_string(self, new_version):
        return('PROJECT_NUMBER' +
               self.num_spaces +
               '= ' +
               str(new_version.major) + '.' +
               str(new_version.minor) + '.' +
               str(new_version.patch))
