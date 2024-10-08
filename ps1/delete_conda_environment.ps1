
."${RepositoriesDirectory}\${RepositoryPath}\ps1\function_definitions.ps1"

# Delete environment
Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                   Deleting the ${DisplayName} conda environment (${EnvironmentName})" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
conda remove --name $EnvironmentName --all --yes

# You have to manually delete the folder if you don't manually stop the server
# `jupyter notebook stop 8888` Won't work on Windows as of 2020-11-19
If (Test-Path -Path $EnvironmentPath -PathType Container) {
	$TokenString = Get-Token-String
	If ($TokenString -Ne "") {
		Read-Host "Stop the Jupyter server manually, then press ENTER to continue..."
	}
	Write-Host ""
	Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
	Write-Host "    Recursively removing ${EnvironmentPath}" -ForegroundColor Green
	Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
	Remove-Item -Recurse -Force $EnvironmentPath
}

# Delete the kernel from the Launcher
$KernelPath = "${HomeDirectory}\AppData\Roaming\jupyter\kernels\${EnvironmentName}"
If (Test-Path -Path $KernelPath -PathType Container) {
	$TokenString = Get-Token-String
	If ($TokenString -Ne "") {
		Read-Host "Stop the Jupyter server manually, then press ENTER to continue..."
	}
	Write-Host ""
	Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
	Write-Host "         Recursively removing ${KernelPath}" -ForegroundColor Green
	Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
	Remove-Item -Recurse -Force $KernelPath
}
conda info --envs