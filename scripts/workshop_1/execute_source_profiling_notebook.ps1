param(
    [string]$NotebookPath = "notebooks/01_source_profiling.ipynb",
    [int]$CellTimeoutSeconds = 300
)

$ErrorActionPreference = "Stop"

$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $repositoryRoot

$uvCommand = Get-Command uv -ErrorAction SilentlyContinue
if ($null -eq $uvCommand) {
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $uvCandidate = $userPath.Split(";") |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
        ForEach-Object { Join-Path $_ "uv.exe" } |
        Where-Object { Test-Path -LiteralPath $_ } |
        Select-Object -First 1
    if ($null -eq $uvCandidate) {
        throw "uv is not installed or available on PATH. Install astral-sh.uv before running this script."
    }
    $uvExecutable = $uvCandidate
}
else {
    $uvExecutable = $uvCommand.Source
}

$lockPath = Join-Path $repositoryRoot "requirements-workshop1.lock"
if (-not (Test-Path -LiteralPath $lockPath)) {
    throw "requirements-workshop1.lock is missing. Generate and review it before execution."
}

$venvPath = Join-Path $repositoryRoot ".venv"
if (-not (Test-Path -LiteralPath $venvPath)) {
    $managedPythonRoot = Join-Path $env:APPDATA "uv\python"
    $managedPython = Get-ChildItem -LiteralPath $managedPythonRoot -Directory -Filter "cpython-3.12.*-windows-x86_64-none" -ErrorAction SilentlyContinue |
        Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName "python.exe") } |
        Sort-Object Name -Descending |
        Select-Object -First 1
    if ($null -ne $managedPython) {
        $pythonSelector = Join-Path $managedPython.FullName "python.exe"
    }
    else {
        $pythonSelector = "3.12"
    }

    & $uvExecutable venv $venvPath --python $pythonSelector
    if ($LASTEXITCODE -ne 0) {
        throw "uv failed to create the Workshop 1 virtual environment."
    }
}

& $uvExecutable pip sync $lockPath --python (Join-Path $venvPath "Scripts\python.exe")
if ($LASTEXITCODE -ne 0) {
    throw "uv failed to synchronize Workshop 1 dependencies."
}

$resolvedNotebook = (Resolve-Path -LiteralPath (Join-Path $repositoryRoot $NotebookPath)).Path
$jupyter = Join-Path $venvPath "Scripts\jupyter-nbconvert.exe"
& $jupyter `
    --to notebook `
    --execute `
    --inplace `
    "--ExecutePreprocessor.timeout=$CellTimeoutSeconds" `
    $resolvedNotebook
if ($LASTEXITCODE -ne 0) {
    throw "Notebook execution failed. Inspect the failing cell before retrying."
}

[pscustomobject]@{
    Notebook = $resolvedNotebook
    Python = (Join-Path $venvPath "Scripts\python.exe")
    UvVersion = (& $uvExecutable --version)
    Status = "executed"
}
