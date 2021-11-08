import os
import re

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

'''
Utility Functions
'''


def ask_question(question):
    answer = input('{}: '.format(question))
    return answer.strip()


def ask_multiple_choice_question(question, choices):
    while True:
        print('{}?'.format(question))
        for i in range(len(choices)):
            print('{}. {}'.format(i, choices[i]))

        try:
            user_choice = int(ask_question('Enter Choice'))
        except ValueError:
            user_choice = None

        if user_choice in range(len(choices)):
            break
        else:
            print('Incorrect choice. Please choose a number between 0 and {}'.format(
                len(choices) - 1))
    return user_choice


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


def main():

    # Open file for reading
    file_path = os.path.join(os.getcwd(), 'sample-input-file.h')
    with open(file_path, 'r', errors='ignore', encoding='utf-8') as f:
        content = f.read()

    print("Pre-bump string:  ", get_major_minor_patch_str(content))

    options = ['Major',
               'Minor',
               'Patch',
               'Do not update']

    user_selected_option = ask_multiple_choice_question(
        'Which version component would you like to bump', options)

    if user_selected_option == 0:
        reobj = re.compile(rPreprocessorMajor, re.X)
        content = reobj.sub(bump_revision_general, content)
    elif user_selected_option == 1:
        reobj = re.compile(rPreprocessorMinor, re.X)
        content = reobj.sub(bump_revision_general, content)
    elif user_selected_option == 2:
        reobj = re.compile(rPreprocessorPatch, re.X)
        content = reobj.sub(bump_revision_general, content)
    else:
        print('Skipping update')

    # Write back to file with replaced contents
    with open(file_path, 'w', errors='ignore', encoding='utf-8') as f:
        f.write(content)
    print("Post-bump string:  ", get_major_minor_patch_str(content))


if __name__ == '__main__':
    main()
