
# cd $Env:UserProfile\Documents\GitHub\job-hunting\ps1
# clear
# .\create_job_hunting_temp_environment_yml_file.ps1

# Set up global variables
$DisplayName = "Job Hunting"
$RepositoryPath = "job-hunting"
$EnvironmentName = "jh"
$HomeDirectory = $Env:UserProfile
$RepositoriesDirectory = "D:\Documents\GitHub"
$EnvironmentPath = "${RepositoriesDirectory}\${RepositoryPath}\${EnvironmentName}"

$OldPath = Get-Location

."${RepositoriesDirectory}\${RepositoryPath}\ps1\create_temp_environment_yml_file.ps1"

Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "       Running Compare It! to compare the old and new yml files" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Start-Process "C:\Program Files (x86)\Compare It!\wincmp3.exe" -ArgumentList "${RepositoriesDirectory}\${RepositoryPath}\environment.yml ${RepositoriesDirectory}\${RepositoryPath}\tmp_environment.yml"

Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "       Running Notepad++ so you can sort the new yml file" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Start-Process "C:\Program Files\Notepad++\notepad++.exe" -ArgumentList "${RepositoriesDirectory}\${RepositoryPath}\tmp_environment.yml"

cd $OldPath