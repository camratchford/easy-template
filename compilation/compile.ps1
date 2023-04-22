# # PWD should be the same directory is this file resides

$ScriptPath = split-path -parent $MyInvocation.MyCommand.Definition

Set-Location $ScriptPath
$DistPath = Join-Path -Path $ScriptPath -ChildPath "dist"
$BuildPath = Join-Path $ScriptPath -ChildPath .\build -ErrorAction SilentlyContinue
$SpecPath = Join-Path $ScriptPath -ChildPath .\ezt.spec -ErrorAction SilentlyContinue

# if (Test-Path -Path $BuildPath) {
#     Remove-Item -Path $BuildPath -Recurse -Force    
# }
# if (Test-Path -Path $DistPath) {
#     Remove-Item -Path $DistPath -Recurse -Force    
# }
# if (Test-Path -Path $SpecPath) {
#     Remove-Item -Path $SpecPath -Recurse -Force    
# }

# $ExeName = "ezt"
# $IncludePaths = (Get-Item -Path $ScriptPath).Parent.FullName

# $PackageName = "Easy-Template"
# $ModulePath = (Join-Path -Path $IncludePaths -ChildPath 'ez_temp')

# $IconPath = (Join-Path -Path $ScriptPath -ChildPath "media/ezt.png").FullName
# $ScriptFile = (Join-Path -Path $IncludePaths -ChildPath "cli.py")
# $VenvPackages = Join-Path -Path (Get-Item -Path $ScriptPath).Parent.FullName -ChildPath ".\venv\Lib\site-packages"

# $CompileParams = @{
#     ScriptBlock = { 
#         Param ($ExeName, $IncludePaths, $VenvPackages, $ModulePath, $PackageName, $DistPath, $IconPath, $ScriptFile)
#         pip install "$IncludePaths"
#         pyinstaller -y --console --clean --onefile --name="$ExeName" --paths="$IncludePaths" --collect-submodules="ez_temp" "$ScriptFile"
#     }
#     ArgumentList = $ExeName, $IncludePaths, $VenvPackages, $ModulePath, $PackageName, $DistPath, $IconPath, $ScriptFile
# }

# Invoke-Command @CompileParams

$VENV_PATH= (Join-Path (Split-Path -Parent $ScriptPath) -ChildPath "venv")

#!/bin/bash
$EXE_NAME="ezt"
$INCLUDE_PATHS="../"
$SCRIPT_FILE="../cli.py"
Start-Process -FilePath (Join-Path -Path $VENV_PATH -ChildPath "scripts\activate")
Start-Process -FilePath (Join-Path -Path $VENV_PATH -ChildPath "scripts\pip") -ArgumentList @('install -r "C:\Users\cameron\PycharmProjects\easy-template - Copy\ez_temp\requirements.txt"')  -Wait -NoNewWindow
Start-Process -FilePath (Join-Path -Path $VENV_PATH -ChildPath "scripts\pip") -ArgumentList @("install ..") -Wait -NoNewWindow
Start-Process -FilePath (Join-Path -Path $VENV_PATH -ChildPath "scripts\pyinstaller") -ArgumentList @("-y", "--clean", "--console", "--onefile", "--name=$EXE_NAME", "--paths=$INCLUDE_PATHS", "--collect-submodules=ez_temp", $SCRIPT_FILE) -Wait -NoNewWindow

#.\dist\ezt.exe --help
#
#.\dist\ezt.exe -v "valid_vars.yml" "valid_README.md.j2"
