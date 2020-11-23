
# cd $Env:UserProfile\Documents\Repositories\job-hunting\ps1
# clear
# .\test.ps1

# Write-Host colors:
# Black, DarkBlue, DarkGreen, DarkCyan, DarkRed, DarkMagenta,
# DarkYellow, Gray, DarkGray, Blue, Green, Cyan, Red, Magenta, Yellow, White

[string]$HomeDirectory = "${Env:UserProfile}"
[string]$RepositoriesDirectory = "${HomeDirectory}\Documents\Repositories"
[string]$RepositoryPath = "job-hunting"
."${RepositoriesDirectory}\${RepositoryPath}\ps1\function_definitions.ps1"

$OldPath = Get-Location

$EnvironmentName = "jh"
$ExecutablePath = "${HomeDirectory}\Anaconda3\envs\${EnvironmentName}\python.exe"
Write-Host ""

$OldConfigPath = "${HomeDirectory}\.jupyter\old_jupyter_notebook_config.py"
If (Test-Path -Path $OldConfigPath -PathType Leaf) {
	Read-Host "You better rescue your old_jupyter_notebook_config.py in the .jupyter folder, we are about to overwrite it. Then press ENTER to continue..."
}
$NewConfigPath = "${HomeDirectory}\.jupyter\jupyter_notebook_config.py"
Copy-Item $NewConfigPath -Destination $OldConfigPath
$ConfigPath = "${HomeDirectory}\Documents\repositories\${RepositoryPath}\jupyter_notebook_config.py"
If (Test-Path -Path $ConfigPath -PathType Leaf) {
	Copy-Item $ConfigPath -Destination $NewConfigPath
}

$PythonVersion = Get-Python-Version $EnvironmentName
Write-Host "PythonVersion = '${PythonVersion}'" -ForegroundColor Yellow

# sys.getdefaultencoding()
$CommandString = -Join($ExecutablePath, ' -c "import sys; print(sys.getdefaultencoding())"')
Write-Host "CommandString = '${CommandString}'" -ForegroundColor Gray
$DefaultEncoding = Invoke-Expression $CommandString
Write-Host "DefaultEncoding = '${DefaultEncoding}'" -ForegroundColor Magenta

# locale.getpreferredencoding()
$CommandString = -Join($ExecutablePath, ' -c "import locale; print(locale.getpreferredencoding())"')
Write-Host "CommandString = '${CommandString}'" -ForegroundColor Gray
$PreferredEncoding = Invoke-Expression $CommandString
Write-Host "PreferredEncoding = '${PreferredEncoding}'" -ForegroundColor Cyan

# sys.stdin.encoding
$CommandString = -Join($ExecutablePath, ' -c "import sys; print(sys.stdin.encoding)"')
Write-Host "CommandString = '${CommandString}'" -ForegroundColor Gray
$StdinEncoding = Invoke-Expression $CommandString
Write-Host "StdinEncoding = '${StdinEncoding}'" -ForegroundColor Blue

cd $OldPath