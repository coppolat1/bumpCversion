import os
import argparse
import configparser
from filetypes import Doxy, PreProcessor
from typing import NamedTuple


class ConfigStruct(NamedTuple):
    name: str
    paths: list


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

    # append every path from .cfg's filesToBump variable
    config.read(config_file)
    for section in config.sections():
        if config.has_option(section, 'filestobump'):
            values = [value.strip() for value in config.get(
                section, 'filestobump').split(',')]
            components.append(ConfigStruct(section, values))
    return config_file_exists, components


# If a version file was specified on the CLI, use it. Otherwise,
# look for a configuration file.
def get_target_files(args):
    target_files = []
    if args.version_file:
        target_files.append(args.version_file)
        return target_files
    else:
        config_file_exists, cfg_components = get_config(args.config_file)

        if not config_file_exists:
            print("Nothing to do!")
            return

        for comp in cfg_components:
            if args.component == comp.name:
                print("\nUsing component:", comp.name + '\n')
                for path in comp.paths:
                    target_files.append(path)

    return target_files


# return the object representing the filetype
def get_filetype_object(args, target_files):
    print("Checking component for file type...")
    for file in target_files:
        if "Doxyfile" in file:
            print("Using Doxyfile...")
            filetype = Doxy(args, file)
            return filetype
        elif file.endswith('.h'):
            print("Using '.h' file...")
            filetype = PreProcessor(args, file)
            return filetype
        else:
            print("ERROR: Filetype not supported.")
    return filetype


def main():

    # Parse command line arguments
    args = parse_args()

    # users desired part (major, minor, or patch) to bump
    part_to_bump = args.part

    # get file we're interested in
    target_files = get_target_files(args)

    while target_files:

        # Creates object representing first file from `target_files`, then pops it off list
        filetype = get_filetype_object(args, target_files)

        # Print file were working with
        print("Target file: " + target_files[0])

        # Print version, before we bump it
        print("Pre-bump string:  ", filetype.version_tostr())

        # Bump filetype object local variable of version
        print("Bumping " + str(args.part) + "...")
        filetype.bump(part_to_bump)

        # Overwrite file based on filetype objects fields
        filetype.overwrite_version()

        # Print version, after we bump it
        print("Post-bump string:  ", filetype.version_tostr() + '\n')

        # Pop `target_files` until out of files
        target_files.pop(0)


if __name__ == '__main__':
    main()
