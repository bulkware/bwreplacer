$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# Keep all generated Windows artifacts in one disposable directory.
# Extract the version from the packaging authority so archive names match MSI metadata.
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$buildRoot = Join-Path $projectRoot "build\windows"
$frozenPath = Join-Path $buildRoot "bwReplacer"
$installerPath = Join-Path $buildRoot "installer"
$metadataPath = Join-Path $projectRoot "pyproject.toml"
$metadata = Get-Content -Raw $metadataPath
$versionMatch = [regex]::Match($metadata, '(?m)^version\s*=\s*"(?<version>[^"]+)"')
if (-not $versionMatch.Success) {
    throw "Unable to determine the version from pyproject.toml."
}
$version = $versionMatch.Groups["version"].Value

Remove-Item -Recurse -Force $buildRoot -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $buildRoot | Out-Null

# Install the project itself so cx_Freeze has its runtime dependency, PySide6.
python -m pip install --upgrade ".[release]"
if ($LASTEXITCODE -ne 0) {
    throw "Windows build dependency installation failed."
}

cxfreeze build
if ($LASTEXITCODE -ne 0) {
    throw "cx_Freeze portable build failed."
}
if (-not (Test-Path -LiteralPath $frozenPath -PathType Container)) {
    throw "cx_Freeze did not produce the expected portable directory: $frozenPath"
}

$portableArchive = Join-Path $buildRoot "bwreplacer-$version-win64-portable.zip"
Compress-Archive -Path $frozenPath -DestinationPath $portableArchive -Force

cxfreeze bdist_msi
if ($LASTEXITCODE -ne 0) {
    throw "cx_Freeze MSI build failed."
}
if (-not (Test-Path -LiteralPath $installerPath -PathType Container)) {
    throw "cx_Freeze did not produce the expected MSI directory: $installerPath"
}

Write-Host "Portable archive: $portableArchive"
Get-ChildItem -LiteralPath $installerPath -Filter "*.msi" | ForEach-Object {
    Write-Host "MSI: $($_.FullName)"
}
