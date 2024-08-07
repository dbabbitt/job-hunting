
# You have to manually stop the jupyter server before you run this in a PowerShell window
# if you are deleting the environment before recreating it:
# 
# conda activate base
# cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\ps1
# cls
# .\create_job_hunting_conda_environment.ps1

# Set up global variables
$DisplayName = "Job Hunting"
$RepositoryPath = "job-hunting"
$EnvironmentName = "jh_env"

$HomeDirectory = $Env:UserProfile
$EnvironmentsDirectory = "${HomeDirectory}\anaconda3\envs"
$RepositoriesDirectory = "C:\Users\daveb\OneDrive\Documents\GitHub"
$PowerScriptsDirectory = "${RepositoriesDirectory}\${RepositoryPath}\ps1"
$EnvironmentPath = "${RepositoriesDirectory}\${RepositoryPath}\${EnvironmentName}"
$OldPath = Get-Location

# Delete environment folder
."${PowerScriptsDirectory}\delete_conda_environment.ps1"

# Create environment folder
."${PowerScriptsDirectory}\create_conda_environment.ps1"
# ."${PowerScriptsDirectory}\update_conda_environment.ps1"

# Bring up the workspace in Chrome
."${PowerScriptsDirectory}\view_lab_in_chrome.ps1"

# Bring up the flaskr app in Chrome
# ."${PowerScriptsDirectory}\view_flaskr_in_chrome.ps1"

cd $OldPath