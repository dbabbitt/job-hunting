
# Create the conda environment
cd "${RepositoriesDirectory}\${RepositoryPath}"
Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
# Assume here that if the environment folder is missing, the environment was already deleted
If (Test-Path -Path $EnvironmentPath -PathType Container) {
	#Write-Host "${EnvironmentName} is a conda environment." -ForegroundColor Red
	Write-Host "               Updating the ${DisplayName} conda environment (${EnvironmentName})" -ForegroundColor Green
} Else {
	#Write-Host "${EnvironmentName} is not a conda environment." -ForegroundColor Green
	Write-Host "               Creating the ${DisplayName} conda environment (${EnvironmentName})" -ForegroundColor Green
}
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
# You can control where a conda environment lives by providing a path to a target directory when creating the environment.
conda env update --prefix $EnvironmentPath --file environment.yml --prune
# conda env update --prefix /mnt/c/Users/daveb/OneDrive/Documents/GitHub/job-hunting/jh_env --file environment.yml --prune
conda info --envs