$ScriptPath = split-path -parent $MyInvocation.MyCommand.Definition

$ExeName = "ezt"
$IncludePaths = (Get-Item -Path $ScriptPath).Parent.FullName 

$DistPath = (Join-Path -Path $ScriptPath -ChildPath "dist").FullName
$ModuleName = "ez_temp"

$IconPath = (Join-Path -Path $ScriptPath -ChildPath "media/ezt.png").FullName
$ScriptFile = (Join-Path -Path $IncludePaths -ChildPath "cli.py")
$VenvPackages = Join-Path -Path (Get-Item -Path $ScriptPath).Parent.FullName -ChildPath ".\venv\Lib\site-packages"

$CompileParams = @{
    ScriptBlock = { 
        Param ($ExeName, $IncludePaths, $DistPath, $ModuleName, $PackageName, $ScriptFile)
        pyinstaller -y --clean --onefile --console --name="$ExeName" --paths="$IncludePaths" --paths="$VenvPackages" --distpath="$DistPath" --splash="$IconPath" "$ScriptFile"
    }
    ArgumentList = $ExeName, $IncludePaths, $DistPath, $ModuleName, $PackageName, $ScriptFile
}

Invoke-Command @CompileParams
