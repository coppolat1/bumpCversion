# bumpCversion
Development of a version bump utility to use with a C repository that uses
semantic pre-processor version definitions.

### 'To Do' List
- [x] Check if a config file exists in the CWD and use it.
  - [ ] Is recursing the whole tree desirable?
- [ ] Is support for other scripting a good feature?
   - i.e., script to check for content in 'unreleased' changelog section.

### 'Should I Do' List
- [ ] Use the 'choices' argument in parser.add_argument() to only allow the user to
      select one of the components that it has already parsed from the config file.
- Config file questions:
  - Where should the `.bump.cfg` file live in a repository?
    - Put it in it's own folder -> `/trunk/repo-tools/.bump.cfg`
      - This might be the better solution, at first.
    - Put it in source folder -> `/trunk/base/.bump.cfg`

### Completed Column ✓
- [x] Completed task title
- [x] Create command line interface and add support for arguments.
  - example: `$> bumpCversion (version_file_path) (major|minor|patch)`
- [x] Zero patch when minor is bumped?
- [x] Add ability to specify a configuration file as an argument.
  - [x] Clean this up
- [x] Bump version number in Doxyfile also.
   - [x] Maybe we can choose which regex to use by file extension type.