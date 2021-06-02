
# cd $Env:UserProfile\Documents\GitHub\job-hunting\ps1
# clear
# .\launch_job_hunting_flask_app.ps1
# 
# Or, just run it from another PowerShell script:
# $argList = "-file `"$RepositoriesDirectory\$RepositoryPath\ps1\launch_job_hunting_flask_app.ps1`""
# Start-Process powershell -argumentlist $argList

# Set up global variables
$RepositoryPath = "job-hunting"
$EnvironmentName = "jh"
$HomeDirectory = $Env:UserProfile
$RepositoriesDirectory = "D:\Documents\GitHub"

Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                          Activating the ${EnvironmentName} environment" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
cd "${RepositoriesDirectory}\${RepositoryPath}"
conda activate $RepositoriesDirectory\$RepositoryPath\$EnvironmentName
$env:FLASK_DEBUG = '1'
$env:FLASK_APP = 'flaskr'
$env:FLASK_ENV = 'development'

<# Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "          Initializing the flaskr db from the ${RepositoryPath} repository" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
flask init-db #>

Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "       Running the flaskr app from the ${RepositoryPath} repository" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
flask run --host localhost --port 5000