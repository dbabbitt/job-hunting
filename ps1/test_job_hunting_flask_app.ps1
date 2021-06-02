
# cd $Env:UserProfile\Documents\GitHub\job-hunting\ps1
# clear
# .\test_job_hunting_flask_app.ps1
# 
# Or, just run it from another PowerShell script:
# $argList = "-file `"$RepositoriesDirectory\$RepositoryPath\ps1\test_job_hunting_flask_app.ps1`""
# Start-Process powershell -argumentlist $argList

# Set up global variables
$RepositoryPath = "job-hunting"
$EnvironmentName = "jh"
$HomeDirectory = $Env:UserProfile
$RepositoriesDirectory = "D:\Documents\GitHub"
$AppName = "flaskr"

Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                          Activating the ${EnvironmentName} environment" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
cd "${RepositoriesDirectory}\${RepositoryPath}\${AppName}"
conda activate $RepositoriesDirectory\$RepositoryPath\$EnvironmentName
$env:FLASK_DEBUG = '1'
$env:FLASK_APP = $AppName
$env:FLASK_ENV = 'development'

Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "       Running the test from the ${RepositoryPath} repository" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
pytest -vv --exitfirst