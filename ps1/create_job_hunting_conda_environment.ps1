
# You have to manually stop the jupyter server before you run this in a PowerShell window:
# 
# cd C:\Users\dev\Documents\Repositories\job-hunting\ps1
# clear
# .\create_job_hunting_conda_environment.ps1

# Set up global variables
$DisplayName = "Job Hunting"
$RepositoryPath = "job-hunting"
$EnvironmentName = "jh"
$EnvironmentPath = "C:\Users\dev\anaconda3\envs\${EnvironmentName}"

# Delete environment
$TokenRegex = [regex] '(?m)http://localhost:8888/\?token=([^ ]+) :: '
$ListResults = (jupyter notebook list) | Out-String
$TokenString = $TokenRegex.Match($ListResults).Groups[1].Value
If ($TokenString -Ne "") {
	Read-Host "Stop the Jupyter server manually, then press ENTER to continue..."
}
."C:\Users\dev\Documents\Repositories\job-hunting\ps1\update_conda_environment.ps1"

<# # Create environment
."C:\Users\dev\Documents\repositories\job-hunting\ps1\create_conda_environment.ps1"

# Bring up the workspace in Chrome
$TokenRegex = [regex] '(?m)http://localhost:8888/\?token=([^ ]+) :: '
$ListResults = (jupyter notebook list) | Out-String
$TokenString = $TokenRegex.Match($ListResults).Groups[1].Value
If ($TokenString -Eq "") {
	Read-Host "Launch the Jupyter server manually, then press ENTER to continue..."
}
."C:\Users\dev\Documents\Repositories\job-hunting\ps1\launch_lab_in_chrome.ps1" #>