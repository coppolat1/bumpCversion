#ifndef LIBNAME_VERSION_H
#define LIBNAME_VERSION_H

/*--------------------------------------------------------------------------------------------------------------
 *                                                 Definitions
 *------------------------------------------------------------------------------------------------------------*/
/*
 * Major Version
 *
 * A change in this number signifies breaking changes and most likely is not backwards compatible with previous versions such as:
 *    - Major API changes
 *    - Total Refactoring
 *    - Protocol Changes
 *    - Header File Name Changes
 * Major version MUST be incremented if any backwards incompatible changes are introduced to the public API. It MAY also include
 * minor and patch level changes. Patch and minor version MUST be reset to 0 when major version is incremented.
 */
#define LIBNAME_VERSION_MAJOR        (21U)

/*
 * Minor Version
 *
 * A change in this number signifies small backwards compatible changes, such as:
 *    - New External Functions
 *    - New or Removed Internal Functions
 *    - Minor API Changes
 *       - An argument type or name might change as this typically won't break end user calls
 *       - Function Names cannot change
 *    - Larger Bug fixes that might change behavior
 *    - File Locations
 * Minor version number MUST be incremented if new, backwards compatible functionality is introduced to the public API.
 * It MUST be incremented if any public API functionality is marked as deprecated.
 * It MAY be incremented if substantial new functionality or improvements are introduced within the private code.
 * It MAY include patch level changes. Patch version MUST be reset to 0 when minor version is incremented.
 */
#define LIBNAME_VERSION_MINOR        (0U)

/*
 * Patch Version
 *
 * A change in this number signifies a backwards compatible bug fix, performance improvement or internal tweak such as:
 *    - Spelling
 *    - Comments
 *    - Documentation
 *    - Minor Bug Fixes
 *       - Examples:
 *          - Initializations
 *          - Local variable type changes
 *          - Bug fixes that will not change behavior
 *
 * These changes MUST be backwards compatible with any previous Minor or Patch Version within this Major Version.
 */
#define LIBNAME_VERSION_PATCH        (0U)


/*--------------------------------------------------------------------------------------------------------------
 *                                         Public (Exportable) Functions
 *------------------------------------------------------------------------------------------------------------*/

LIBNAMEFUNC uint32_t NAIAPI libname_GetVersionMajor(void);

LIBNAMEFUNC uint32_t NAIAPI libname_GetVersionMinor(void);

LIBNAMEFUNC uint32_t NAIAPI libname_GetVersionPatch(void);


#endif
