
# cd $Env:UserProfile\OneDrive\Documents\GitHub\job-hunting\ps1
# cls
# .\launch_job_hunting_flask_app.ps1
# 
# Or, just run it from another PowerShell script:
# $argList = "-file `"$RepositoriesDirectory\$RepositoryPath\ps1\launch_job_hunting_flask_app.ps1`""
# Start-Process powershell -argumentlist $argList

# Set up global variables
$RepositoryPath = "job-hunting"
$EnvironmentName = "jh_env"
$HomeDirectory = $Env:UserProfile
$RepositoriesDirectory = "${HomeDirectory}\OneDrive\Documents\GitHub"

Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                          Activating the ${EnvironmentName} environment" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
cd "${RepositoriesDirectory}\${RepositoryPath}"
conda activate $RepositoriesDirectory\$RepositoryPath\$EnvironmentName
$env:FLASK_DEBUG = '1'
$env:FLASK_APP = 'flaskr'
$env:FLASK_ENV = 'development'

Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "       Running the flaskr app from the ${RepositoryPath} repository" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
cd "${RepositoriesDirectory}\${RepositoryPath}"

# Use type myapp.wsgi > nul to manually trigger a soft reload
flask run --no-reload --host localhost --port 5000