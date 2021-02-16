
."${RepositoriesDirectory}\${RepositoryPath}\ps1\function_definitions.ps1"

$OldPath = Get-Location

# Update conda
conda deactivate
conda config --set auto_update_conda true
conda config --set report_errors false
<# # You might have to un-comment this to compile some libraries
Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                             Installing m2w64-toolchain" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
conda install m2w64-toolchain --yes #>
Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host " Installing the package for run-time control of the Intel Math Kernel Library" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
conda install -c intel mkl-service --yes
<# # You can force a re-download of your environment packages by un-commenting this out
Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "              Removing all unused base conda packages and caches" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
conda clean --all --yes #>
Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "              Checking all base conda packages for potential updates" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
conda update --all --yes
<# Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                   Uninstalling the inexplicably corrupted pyzmq" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
conda uninstall pyzmq --yes
Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                               Reinstalling pyzmq" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
# Reinstalling jupyter-lab to force all the uninstalls to come back
conda install pyzmq jupyterlab --yes #>

# Update Node.js
Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                Checking all NPM packages for potential updates" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
<# $CommandString = "npm cache clean"
Invoke-Expression $CommandString #>
$CommandString = "npm install -g npm"
Invoke-Expression $CommandString
$CommandString = "npm update -g"
Invoke-Expression $CommandString

# Create the conda environment
."${RepositoriesDirectory}\${RepositoryPath}\ps1\update_conda_environment.ps1"

# Add the kernel to the Launcher
Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                        Adding the kernel to the Launcher" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Add-Python-Executable-To-Path $EnvironmentPath
Add-Kernel-To-Launcher $EnvironmentPath -DisplayName $DisplayName
$KernelPath = "${HomeDirectory}\AppData\Roaming\jupyter\kernels\${EnvironmentName}\kernel.json"
If (Test-Path -Path $KernelPath -PathType Leaf) {
	Add-Logos-To-Kernel-Folder $EnvironmentName -RepositoryPath $RepositoryPath
	(Get-Content $KernelPath) | ConvertFrom-Json | ConvertTo-Json -depth 7 | Format-Json -Indentation 2
}

# Add a workspace file for bookmarking. You can create a temporary workspace file in the 
# $Env:UserProfile\.jupyter\lab\workspaces folder by going to this URL:
# http://localhost:8888/lab/?clone=$EnvironmentName
Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                        Importing the workspace file" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
$WorkspacePath = Import-Workspace-File $RepositoryPath
If ($WorkspacePath -Ne $null) {
	If (Test-Path -Path $WorkspacePath -PathType Leaf) {
		(Get-Content $WorkspacePath) | ConvertFrom-Json | ConvertTo-Json -depth 7 | Format-Json -Indentation 2
	}
}

# Clean up the mess
Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                          Cleaning the staging area" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
# jupyter-lab clean
$CommandString = "${RepositoriesDirectory}\${RepositoryPath}\${EnvironmentName}\Scripts\jupyter-lab.exe clean"
Invoke-Expression $CommandString
# jupyter labextension list
$CommandString = "${RepositoriesDirectory}\${RepositoryPath}\${EnvironmentName}\Scripts\jupyter-labextension.exe list"
$ExtensionsList = Invoke-Expression $CommandString
if (!($ExtensionsList -Like "*No installed extensions*")) {
	Write-Host ""
	Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
	Write-Host "                     Updating the Jupyter Lab extensions" -ForegroundColor Green
	Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
	# jupyter labextension update --all
	$CommandString = "${RepositoriesDirectory}\${RepositoryPath}\${EnvironmentName}\Scripts\jupyter-labextension.exe update --all"
	Invoke-Expression $CommandString
}
Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                       Rebuilding the Jupyter Lab assets" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
#,"${HomeDirectory}\anaconda3\etc\jupyter","C:\ProgramData\jupyter"
$ConfigFoldersList = @("${HomeDirectory}\.jupyter")
ForEach ($ConfigFolder in $ConfigFoldersList) {
	$OldConfigPath = "${ConfigFolder}\old_jupyter_notebook_config.py"
	If (Test-Path -Path $OldConfigPath -PathType Leaf) {
		Read-Host "You better rescue your old_jupyter_notebook_config.py in the ${ConfigFolder} folder, we are about to overwrite it. Then press ENTER to continue..."
	}
	$NewConfigPath = "${ConfigFolder}\jupyter_notebook_config.py"
	Copy-Item $NewConfigPath -Destination $OldConfigPath
	$ConfigPath = "${RepositoriesDirectory}\${RepositoryPath}\jupyter_notebook_config.py"
	If (Test-Path -Path $ConfigPath -PathType Leaf) {
		Copy-Item $ConfigPath -Destination $NewConfigPath
	}
}
# jupyter-lab build
$CommandString = "${RepositoriesDirectory}\${RepositoryPath}\${EnvironmentName}\Scripts\jupyter-lab.exe build"
Invoke-Expression $CommandString

# Copy the favicon asset to the static directory
$IconPath = "${RepositoriesDirectory}\${RepositoryPath}\${EnvironmentName}\saves\ico\notebook_static_favicon.ico"
If (Test-Path -Path $IconPath -PathType Leaf) {
	$FaviconsFoldersList = @("${HomeDirectory}\anaconda3\share\jupyter\lab\static\favicons","${RepositoriesDirectory}\${RepositoryPath}\${EnvironmentName}\share\jupyter\lab\static\favicons")
	ForEach ($FaviconsFolder in $FaviconsFoldersList) {
		$NewIconPath = "${FaviconsFolder}\favicon.ico"
		If (!(Test-Path -Path $NewIconPath -PathType Leaf)) {
			If (!(Test-Path -Path $FaviconsFolder -PathType Container)) {
				New-Item -ItemType Directory -Path $FaviconsFolder
			}
			Copy-Item $IconPath -Destination $NewIconPath
		}
	}
}

cd $OldPath