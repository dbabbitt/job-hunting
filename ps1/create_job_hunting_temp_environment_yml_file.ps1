
# cd $Env:UserProfile\Documents\Repositories\job-hunting\ps1
# clear
# .\create_job_hunting_temp_environment_yml_file.ps1

# Set up global variables
$DisplayName = "Job Hunting"
$RepositoryPath = "job-hunting"
$EnvironmentName = "jh"
$HomeDirectory = $Env:UserProfile
$RepositoriesDirectory = "${HomeDirectory}\Documents\Repositories"
$EnvironmentPath = "${RepositoriesDirectory}\${RepositoryPath}\${EnvironmentName}"

."${RepositoriesDirectory}\${RepositoryPath}\ps1\create_temp_environment_yml_file.ps1"