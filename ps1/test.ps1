
# cd $Env:UserProfile\Documents\Repositories\job-hunting\ps1
# clear
# .\test.ps1

# Write-Host colors:
# Black, DarkBlue, DarkGreen, DarkCyan, DarkRed, DarkMagenta,
# DarkYellow, Gray, DarkGray, Blue, Green, Cyan, Red, Magenta, Yellow, White

[string]$HomeDirectory = "${Env:UserProfile}"
[string]$RepositoriesDirectory = "${HomeDirectory}\Documents\Repositories"
[string]$RepositoryPath = "job-hunting"
[string]$EnvironmentName = "jh"

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