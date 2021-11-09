# bumpCversion
Development of a version bump utility to use with a C repository that uses semantic
pre-processor version definitions.

### 'To Do' List
- [ ] How do we handle multiple files?
   - Have 'version-file' arg support multiple files?
   - Add config file
      - One config file per repo vs. one per library/component?
      - This config file would get added to VCS and outline each library, which files to check in, etc.
      ```
      config file:
      [bumpCversion]
      
      [group:$libname]
      [$libname:file:$filename]
      [$libname:file:$filename1]

      [group:$libname1]
      [$libname:file:$filename]
      [$libname:file:$filename1]

      usage:
      $> bumpCversion.py $libname1 major
      ```
- [ ] Bump version number in Doxyfile also.
   - Maybe we can choose which regex to use by file extension type.
- [ ] Are configuration files needed?
- [ ] Is support for other scripting a good feature?
   - i.e., script to check for content in 'unreleased' changelog section.


### Completed Column ✓
- [x] Completed task title
- [x] Create command line interface and add support for arguments.
   - example: `$> bumpCversion (version_file_path) (major|minor|patch)`
- [x] Zero patch when minor is bumped?