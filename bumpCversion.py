import os
import typer
import configparser
from exceptions import FileNotSupportedException, VersionException
from filetypes import Doxy, PreProcessor
from typing import NamedTuple


class ConfigStruct(NamedTuple):
    name: str
    paths: list


app = typer.Typer()

# Create list of found versions (length should be == 1)
versions = set()

# Get file we're interested in
target_files = []


@app.command()
def display_version(config: str):
    """
    Print out all components respective versions
    """
    if os.path.exists(config):
        print_versions(config, versions)


@app.command()
def dry_run(config: str, component: str, part: str, reset: bool):
    """
    Print out current and expected versions (without modifying files)
    """
    if os.path.exists(config):
        target_files = get_target_files(config, component)
        print_dry(config, component, part, target_files, reset, versions)


@app.command()
def bump(config: str = typer.Argument(
        ..., help="Configuration file to read from. If this argument is \
            not supplied the program will check for the existence of a \
            configuration file in the CWD"),
        component: str = typer.Argument(
        ..., help="A component defined in the config file, of which to bump"),
        part: str = typer.Argument(
        ..., help="Part to bump: major, minor, patch"),
        reset: bool = typer.Option(
        False, help="Reset the patch and/or minor to zero when bumping the \
            higher parts")):
    """
    Bump version numbers from files specified in config
    """

    # Check to see if version number is the same across all files
    print("Checking component [" + str(component) +
          "] for verison number congruence...\n")

    if os.path.exists(config) and valid_version_congruence(config, versions):

        target_files = get_target_files(config, component)

        while target_files:

            print("Checking component [" +
                  str(component) + "] for file type...")

            # Creates object representing first file from `target_files`, then pops it off list
            filetype = get_filetype_object(target_files)

            # Print file were working with
            print("Target file: " + target_files[0])

            # Print version, before we bump it
            print("Pre-bump string:  ", filetype.version_number)

            # Bump filetype object local variable of version
            print("Bumping " + str(part) + "...")
            filetype.version_number.bump(part, reset)

            # Overwrite file based on filetype objects fields
            filetype.update_version_in_file()

            # Print version, after we bump it
            print("Post-bump string:  ", filetype.version_number, '\n')

            # Pop `target_files` until out of files
            target_files.pop(0)


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


def get_target_files(config, component):
    """
    If a version file was specified on the CLI, use it. Otherwise, look for a configuration file.
    """
    target_files = []

    config_file_exists, cfg_components = get_config(config)

    if not config_file_exists:
        print("Nothing to do, configuration does not exist!")
        return

    for comp in cfg_components:
        if component == comp.name:
            print("\nUsing component:", comp.name + '\n')
            for path in comp.paths:
                target_files.append(path)

    return target_files


def valid_version_congruence(config, versions):
    """
    Check to see if version number is the same across all files per component.
    """
    config_file_exists, cfg_components = get_config(config)
    for component in cfg_components:
        if config_file_exists:
            while component.paths:
                filetype = get_filetype_object(component.paths)
                # add version to unique set
                versions.add(str(filetype.version_number))
                component.paths.pop(0)
            if len(versions) == 1:
                versions.clear()
                continue
            else:
                print("Multiple Verisons Found -> " + str(versions))
                raise(VersionException(Exception))

    return 1


def print_dry(config, component, part, target_files, reset, versions):
    """
    Print expected bump value of version found from first target file.
    """
    if valid_version_congruence(config, versions):
        if target_files:
            filetype = get_filetype_object(target_files)
            print("Current version = " + str(filetype.version_number))
            filetype.version_number.bump(part, reset)
            print("Expected version post-bump = " +
                  str(filetype.version_number) + "\n")


def print_versions(config, versions):
    """
    Print expected bump value of version found from first target file.
    """
    if valid_version_congruence(config, versions):
        config_file_exists, cfg_components = get_config(config)
        for component in cfg_components:
            if config_file_exists:
                filetype = get_filetype_object(component.paths)
                print("Component: [" + component.name + "]" +
                      " -> " + str(filetype.version_number))


def get_filetype_object(target_files):
    """
    Return the object representing the filetype.
    """
    for file in target_files:
        if "Doxyfile" in file:
            filetype = Doxy(file)
            return filetype
        elif file.endswith('.h'):
            filetype = PreProcessor(file)
            return filetype
        else:
            raise(FileNotSupportedException(Exception))
    return filetype


if __name__ == '__main__':
    app()
