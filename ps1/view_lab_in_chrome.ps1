
."${RepositoriesDirectory}\${RepositoryPath}\ps1\function_definitions.ps1"

$TokenString = Get-Token-String
If ($TokenString -Eq "") {
	Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
	Write-Host "             Launching the Jupyter server in its own window" -ForegroundColor Green
	Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
	$argList = "${RepositoriesDirectory}\${RepositoryPath}\${EnvironmentName}\Scripts\jupyter-lab.exe --no-browser --config=${HomeDirectory}\.jupyter\jupyter_notebook_config.py --notebook-dir=${RepositoriesDirectory}"
	Start-Process PowerShell -argumentlist $argList
	Read-Host "Verify the Jupyter server is running, then press ENTER to continue..."
}

Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                          Getting the Jupyter Lab token" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
$ListResults = (jupyter notebook list) | Out-String
Write-Host $ListResults

# Open the webpage in Chrome
$TokenRegex = [regex] '(?m)http://localhost:8888/\?token=([^ ]+) :: '
$TokenString = $TokenRegex.Match($ListResults).Groups[1].Value
If ($TokenString -Ne "") {
	Write-Host ""
	Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
	Write-Host "                          Opening the workspace in Chrome" -ForegroundColor Green
	Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
	# All other workspaces have a name that is part of the URL:
	# http(s)://<server:port>/<lab-location>/lab/workspaces/foo
	Start-Process "chrome.exe" "http://localhost:8888/lab/workspaces/${EnvironmentName}&token=${TokenString}"
}