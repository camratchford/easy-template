# # PWD should be the same directory is this file resides
$PreviousPWD = Get-Location


$ScriptPath = split-path -parent $MyInvocation.MyCommand.Definition
$RepoRoot = Split-Path -Parent $ScriptPath


Set-Location $ScriptPath

$DistPath = Join-Path -Path $ScriptPath -ChildPath "dist"
$BuildPath = Join-Path $ScriptPath -ChildPath build -ErrorAction SilentlyContinue
$IconPath = Join-Path $ScriptPath -ChildPath media\ezt.png -ErrorAction SilentlyContinue
$SpecPath = Join-Path $ScriptPath -ChildPath ezt.spec -ErrorAction SilentlyContinue




$VENV_PATH= (Join-Path $RepoRoot -ChildPath "venv")


if (!(Test-Path $VENV_PATH)) {
    python -m venv $VENV_PATH

}

$EXE_NAME="ezt"
$INCLUDE_PATHS="../"
$SCRIPT_FILE="../cli.py"
Start-Process -FilePath (Join-Path -Path $VENV_PATH -ChildPath "scripts\activate")
Start-Process -FilePath (Join-Path -Path $VENV_PATH -ChildPath "scripts\pip") -ArgumentList @("install pillow")  -Wait -NoNewWindow
Start-Process -FilePath (Join-Path -Path $VENV_PATH -ChildPath "scripts\pip") -ArgumentList @("install -e ..") -Wait -NoNewWindow
Start-Process -FilePath (Join-Path -Path $VENV_PATH -ChildPath "scripts\pyinstaller") -ArgumentList @("-y", "--clean", "--console", "--onefile", "--icon=$IconPath", "--name=$EXE_NAME", "--paths=$INCLUDE_PATHS", "--collect-submodules=ez_temp", $SCRIPT_FILE) -Wait -NoNewWindow


Set-Location $PreviousPWD