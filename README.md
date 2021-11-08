# bumpCversion

## Overview

Development of a version bump utility to use with a C repository that uses semantic
pre-processor version definitions. Where a version `1.2.0` is represented in a
header file as:
```
#define LIBNAME_VERSION_MAJOR        (1U)
#define LIBNAME_VERSION_MINOR        (2U)
#define LIBNAME_VERSION_PATCH        (0U)
```