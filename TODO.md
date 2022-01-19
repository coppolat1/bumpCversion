# bumpCversion
Development of a version bump utility to use with a C repository that uses
semantic pre-processor version definitions.

### 'To Do' List
- [x] Add ability to specify a configuration file as an argument.
  - [ ] Clean this up
- [ ] Check if a config file exists in the CWD and use it.
  - [ ] Is recursing the whole tree desirable?
- [ ] Bump version number in Doxyfile also.
   - Maybe we can choose which regex to use by file extension type.
- [ ] Are configuration files needed?
- [ ] Is support for other scripting a good feature?
   - i.e., script to check for content in 'unreleased' changelog section.

### 'Should I Do' List
- [ ] Use the 'choices' argument in parser.add_argument() to only allow the user to
      select one of the components that it has already parsed from the config file.

### Completed Column ✓
- [x] Completed task title
- [x] Create command line interface and add support for arguments.
   - example: `$> bumpCversion (version_file_path) (major|minor|patch)`
- [x] Zero patch when minor is bumped?