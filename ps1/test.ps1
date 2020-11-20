
# cd C:\Users\dev\Documents\Repositories\job-hunting\ps1
# clear
# .\test.ps1

$EnvironmentName = "flask"
$EnvironmentPath = "C:\Users\dev\anaconda3\envs\${EnvironmentName}"
If ( Test-Path -Path $EnvironmentPath -PathType Container ) {
	Write-Host "${EnvironmentPath} exists." -ForegroundColor Green
} Else {
	Write-Host "${EnvironmentPath} does not exist." -ForegroundColor Red
}
$EnvironmentName = "jh"
$EnvironmentPath = "C:\Users\dev\anaconda3\envs\${EnvironmentName}"
If ( Test-Path -Path $EnvironmentPath -PathType Container ) {
	Write-Host "${EnvironmentPath} exists." -ForegroundColor Green
} Else {
	Write-Host "${EnvironmentPath} does not exist." -ForegroundColor Red
}