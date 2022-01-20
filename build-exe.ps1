<#
.SYNOPSIS
   Executable generation script for bumpCversion.py
.DESCRIPTION
   Create executable with pyinstaller, move it to the
   bin folder and remove build artifacts.
#>

Write-Host "Running pyinstaller!" -ForegroundColor yellow
pyinstaller -F bumpCversion.py

# Create /bin dir, if it does not exist
if (-Not (Test-Path '.\bin')) {
   md -path '.\bin' > $null
}

Copy-Item -Path dist/bumpCversion.exe -Destination bin/

# Clean up build artifacts
Write-Host "Cleaning build artifacts" -ForegroundColor yellow
Remove-Item .\dist               -Recurse -ErrorAction SilentlyContinue
Remove-Item .\build              -Recurse -ErrorAction SilentlyContinue
Remove-Item .\__pycache__\       -Recurse -ErrorAction SilentlyContinue
Remove-Item .\bumpCversion.spec           -ErrorAction SilentlyContinue