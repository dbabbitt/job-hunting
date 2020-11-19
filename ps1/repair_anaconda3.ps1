
# cd C:\Users\dev\Documents\repositories\job-hunting\ps1
# clear
# .\repair_anaconda3.ps1

$AnacondaName = "anaconda3"
$HomeFolder = "C:\Users\dev"
$AnacondaFolder = "${HomeFolder}\${AnacondaName}"
$BackupName = "${AnacondaName}_old"
$BackupFolder = "${HomeFolder}\${BackupFolder}"
#Remove-Item -Recurse -Force $BackupFolder
# THIS DELETED MY ENTIRE DEV FOLDER!!!
#Get-Childitem -Path $BackupFolder -Recurse | Remove-Item -Recurse -Force
If ([System.IO.File]::Exists($BackupFolder)) {
	Read-Host "Delete or rename the ${BackupName} folder manually, then press ENTER to continue..."
}
If (!([System.IO.File]::Exists($BackupFolder))) {
	Rename-Item $AnacondaFolder $BackupFolder
}
If (!([System.IO.File]::Exists($AnacondaFolder))) {
	# $PathVargs = {C:\Users\dev\Downloads\Anaconda3-2020.07-Windows-x86_64.exe}
	# Invoke-Command -ScriptBlock $PathVargs
	Read-Host "Launch the Anaconda3 installer manually, then press ENTER to continue when it is complete..."
	cd $HomeFolder
	robocopy $BackupName $AnacondaName /S
}

$CommandString = "jupyter notebook --version"
Write-Host "CommandString = ${CommandString}" -ForegroundColor Red
$VersionResults = cmd /c $CommandString '2>&1'
$VersionResults = $VersionResults.Trim()
Write-Host "VersionResults = ${VersionResults}" -ForegroundColor Red
