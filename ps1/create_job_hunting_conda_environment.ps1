
# You have to manually stop the jupyter server before you run this in a PowerShell window
# if you are deleting the environment before recreating it:
# 
# cd $Env:UserProfile\Documents\Repositories\job-hunting\ps1
# clear
# .\create_job_hunting_conda_environment.ps1

# Set up global variables
$DisplayName = "Job Hunting"
$RepositoryPath = "job-hunting"
$EnvironmentName = "jh"

$HomeDirectory = $Env:UserProfile
$EnvironmentsDirectory = "${HomeDirectory}\anaconda3\envs"
$RepositoriesDirectory = "${HomeDirectory}\Documents\Repositories"
$PowerScriptsDirectory = "${RepositoriesDirectory}\${RepositoryPath}\ps1"
$EnvironmentPath = "${RepositoriesDirectory}\${RepositoryPath}\${EnvironmentName}"

# Delete environment
# ."${PowerScriptsDirectory}\delete_conda_environment.ps1"

# Create environment
$OldPath = Get-Location
# ."${PowerScriptsDirectory}\create_conda_environment.ps1"
# ."${PowerScriptsDirectory}\update_conda_environment.ps1"
cd $OldPath

# Launch Flask App
Write-Host "---------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "              Launching the flaskr app in its own window" -ForegroundColor Green
Write-Host "---------------------------------------------------------------------------------" -ForegroundColor Green
$argList = "-file `"$PowerScriptsDirectory\launch_job_hunting_flask_app.ps1`" -NoExit"
Start-Process PowerShell -argumentlist $argList

# Bring up the flaskr app in Chrome
Start-Sleep -Seconds 20
# ."${PowerScriptsDirectory}\view_flaskr_in_chrome.ps1"

# Bring up the workspace in Chrome
# ."${PowerScriptsDirectory}\view_lab_in_chrome.ps1"