
# cd C:\Users\dev\Documents\Repositories\job-hunting\ps1
# clear
# .\test.ps1

$EnvironmentName = "myenv"
$CommandString = "conda activate ${EnvironmentName}"
Write-Host "CommandString = '${CommandString}'" -ForegroundColor Yellow
$ResultString = cmd /c $CommandString '2>&1'
Write-Host "ResultString = '${ResultString}'" -ForegroundColor Yellow
If ($ResultString -Like "Could not find conda environment*") {
	Write-Host "${EnvironmentName} is not a conda environment." -ForegroundColor Red
} Else {
	Write-Host "${EnvironmentName} is a conda environment." -ForegroundColor Green
}