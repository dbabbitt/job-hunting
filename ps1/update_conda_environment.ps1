
$OldPath = Get-Location

# Create the conda environment
cd "C:\Users\dev\Documents\repositories\${RepositoryPath}"
$CommandString = "conda activate ${EnvironmentName}"
$ResultString = cmd /c $CommandString '2>&1'
Write-Host ""
Write-Host "---------------------------------------------------------------------------------" -ForegroundColor Green
If ($ResultString -Like "Could not find conda environment*") {
	Write-Host "                Creating the ${DisplayName} conda environment" -ForegroundColor Green
} Else {
	Write-Host "                Updating the ${DisplayName} conda environment" -ForegroundColor Green
}
Write-Host "---------------------------------------------------------------------------------" -ForegroundColor Green
conda env update --file environment.yml --prune

cd $OldPath