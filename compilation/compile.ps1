# # PWD should be the same directory is this file resides

$ScriptPath = split-path -parent $MyInvocation.MyCommand.Definition
$RepoRoot = Split-Path -Parent $ScriptPath


Set-Location $ScriptPath

$DistPath = Join-Path -Path $ScriptPath -ChildPath "dist"
$BuildPath = Join-Path $ScriptPath -ChildPath .\build -ErrorAction SilentlyContinue
$SpecPath = Join-Path $ScriptPath -ChildPath .\ezt.spec -ErrorAction SilentlyContinue




$VENV_PATH= (Join-Path $RepoRoot -ChildPath "venv")

if (!(Test-Path $VENV_PATH)) {
    python -m venv $VENV_PATH
}

$EXE_NAME="ezt"
$INCLUDE_PATHS="../"
$SCRIPT_FILE="../cli.py"
Start-Process -FilePath (Join-Path -Path $VENV_PATH -ChildPath "scripts\activate")
Start-Process -FilePath (Join-Path -Path $VENV_PATH -ChildPath "scripts\pip") -ArgumentList @("install -r `"$RepoRoot\ez_temp\requirements.txt`"")  -Wait -NoNewWindow
Start-Process -FilePath (Join-Path -Path $VENV_PATH -ChildPath "scripts\pip") -ArgumentList @("install ..") -Wait -NoNewWindow
Start-Process -FilePath (Join-Path -Path $VENV_PATH -ChildPath "scripts\pyinstaller") -ArgumentList @("-y", "--clean", "--console", "--onefile", "--name=$EXE_NAME", "--paths=$INCLUDE_PATHS", "--collect-submodules=ez_temp", $SCRIPT_FILE) -Wait -NoNewWindow

#.\dist\ezt.exe --help
#
#.\dist\ezt.exe -v "valid_vars.yml" "valid_README.md.j2"
Copy-Item "C:\Users\Installer\git_repos\easy-template\compilation\dist\ezt.exe" "C:\ToolBox\Utilities\PSModules\PLM-Templating\1.0.0\ezt\ezt.exe" -Force
