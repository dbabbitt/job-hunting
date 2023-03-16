
# cd $Env:UserProfile\Documents\GitHub\job-hunting\ps1
# clear
# .\test.ps1

# Write-Host colors:
# Black, DarkBlue, DarkGreen, DarkCyan, DarkRed, DarkMagenta,
# DarkYellow, Gray, DarkGray, Blue, Green, Cyan, Red, Magenta, Yellow, White

[string]$HomeDirectory = "${Env:UserProfile}"
[string]$RepositoriesDirectory = "D:\Documents\GitHub"
[string]$RepositoryPath = "job-hunting"
[string]$EnvironmentName = "jh_env"

."${RepositoriesDirectory}\${RepositoryPath}\ps1\function_definitions.ps1"

$OldPath = Get-Location

cd "${RepositoriesDirectory}\${RepositoryPath}"
# flask init-db
Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "       Running the flaskr app from the ${RepositoryPath} repository" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
$server = Start-Process flask -ArgumentList 'run --host localhost --port 5000' -PassThru 
Read-Host "${server.Id}"

cd $OldPath