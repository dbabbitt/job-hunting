
# You have to manually stop the jupyter server before you run this in a PowerShell window
# if you are deleting the environment before recreating it:
# 
# cd C:\Users\dev\Documents\Repositories\job-hunting\ps1
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
$EnvironmentPath = "${EnvironmentsDirectory}\${EnvironmentName}"

# Delete environment
."${PowerScriptsDirectory}\delete_conda_environment.ps1"

# Create environment
<# $OldPath = Get-Location
."${PowerScriptsDirectory}\update_conda_environment.ps1"
cd $OldPath #>
."${PowerScriptsDirectory}\create_conda_environment.ps1"

# Bring up the workspace in Chrome
."${PowerScriptsDirectory}\launch_lab_in_chrome.ps1"