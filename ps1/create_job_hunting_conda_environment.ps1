
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
$OldPath = Get-Location

# Delete environment
# ."${PowerScriptsDirectory}\delete_conda_environment.ps1"

# Create environment
# ."${PowerScriptsDirectory}\create_conda_environment.ps1"
# ."${PowerScriptsDirectory}\update_conda_environment.ps1"

# Bring up the workspace in Chrome
."${PowerScriptsDirectory}\view_lab_in_chrome.ps1"

# Bring up the flaskr app in Chrome
# ."${PowerScriptsDirectory}\view_flaskr_in_chrome.ps1"

cd $OldPath