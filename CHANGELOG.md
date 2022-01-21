# bumpCversion Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog],
and this project adheres to [Semantic Versioning].

## [Unreleased]
None

## [0.5.0] - 2022-01-20
### Added
- Logic to check for config file in execution directory, only if --config-file is not specified.

## [0.4.0] - 2022-01-20
### Changed
- Build script to use nuitka instead of pyinstaller to avoid anti-virus issues.

## [0.3.0] - 2022-01-19
### Added
- `bin` folder to put executables built with `pyinstaller`
- Build script to ease creation of tags/releases
- `test` folder and move test items into it
- This changelog

## [0.2.0] - 2022-01-19
### Added
- Launch args for vscode
- Config file handling and add a test config file: `.bump.cfg`
- A sample input file for testing
- `TODO.md`
- Arguments and the ability to parse them

## [0.1.0] - 2021-11-08
### Added
- Initial tag with the ability to find and replace version numbers in C
  preprocessor definition style version definitions


[Unreleased]: https://github.com/coppolat1/bumpCversion/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/coppolat1/bumpCversion/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/coppolat1/bumpCversion/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/coppolat1/bumpCversion/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/coppolat1/bumpCversion/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/coppolat1/bumpCversion/releases/tag/v0.1.0

[Keep a Changelog]: https://keepachangelog.com/en/1.0.0/
[Semantic Versioning]: https://semver.org/spec/v2.0.0.html

<!---
Keep a Changelog Sections

### Added      for new features.
### Changed    for changes in existing functionality.
### Deprecated for soon-to-be removed features.
### Removed    for now removed features.
### Fixed      for any bug fixes.
### Security   in case of vulnerabilities.
-->