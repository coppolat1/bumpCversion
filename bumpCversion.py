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


def main():

    print("Pre-bump string:  ", test_str)
    #val = input("Bump major, minor or patch? ")

    options = ['Major',
               'Minor',
               'Patch',
               'Do not update' ]

    user_selected_option = ask_multiple_choice_question(
        'Which version component would you like to bump', options)

    if user_selected_option == 0:
        reobj = re.compile(rPreprocessorMajor, re.X)
        rep = reobj.sub(bump_revision_general, test_str)
    elif user_selected_option == 1:
        reobj = re.compile(rPreprocessorMinor, re.X)
        rep = reobj.sub(bump_revision_general, test_str)
    elif user_selected_option == 2:
        reobj = re.compile(rPreprocessorPatch, re.X)
        rep = reobj.sub(bump_revision_general, test_str)
    else:
        print('Skipping update')


    print('Updated version to: \n', rep)


if __name__ == '__main__':
    main()
