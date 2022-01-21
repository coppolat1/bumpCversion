<#
.SYNOPSIS
   Executable generation script for bumpCversion.py
.DESCRIPTION
   Create executable with nuitka, move it to the
   bin folder and remove build artifacts.
#>

Write-Host "Generating a Windows executable!" -ForegroundColor yellow
nuitka --onefile --msvc=14.2 --remove-output .\bumpCversion.py

# Create /bin dir, if it does not exist
if (-Not (Test-Path '.\bin')) {
   md -path '.\bin' > $null
}

Move-Item -Path '.\bumpCversion.exe' -Destination '.\bin' -Force

# Clean up build artifacts
Write-Host "Cleaning build artifacts"  -ForegroundColor yellow
Remove-Item '.\bumpCversion.cmd'       -ErrorAction SilentlyContinue