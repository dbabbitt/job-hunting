
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
<# Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host " Installing the package for run-time control of the Intel Math Kernel Library" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
conda install -c intel mkl-service --yes #>
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

# https://stackoverflow.com/questions/42563757/conda-update-condahttperror-http-none/60342954#60342954
# From anaconda3\Library\bin copy below files and paste them in anaconda3/DLLs:
$DllsFolder = "${EnvironmentPath}\DLLs"
$AnacondaName = "anaconda3"
$AnacondaFolder = "${HomeDirectory}\${AnacondaName}"
# -   libcrypto-1_1-x64.dll
$DllPath = "${EnvironmentPath}\Library\bin\libcrypto-1_1-x64.dll"
If (!(Test-Path -Path $DllPath -PathType Leaf)) {
	$DllPath = "${AnacondaFolder}\Library\bin\libcrypto-1_1-x64.dll"
}
# Write-Host "Copying libcrypto-1_1-x64.dll to the DLLs folder" -ForegroundColor Green
Copy-Item $DllPath -Destination $DllsFolder
# -   libssl-1_1-x64.dll
$DllPath = "${EnvironmentPath}\Library\bin\libssl-1_1-x64.dll"
If (!(Test-Path -Path $DllPath -PathType Leaf)) {
	$DllPath = "${AnacondaFolder}\Library\bin\libssl-1_1-x64.dll"
}
# Write-Host "Copying libssl-1_1-x64.dll to the DLLs folder" -ForegroundColor Green
Copy-Item $DllPath -Destination $DllsFolder

# https://stackoverflow.com/questions/43916440/error-loading-jupyter-notebook-extensions
# I solved this problem by removing jupyter-notebook, jupyter_contrib_nbextensions,
# and jupyter_nbextensions_configurator, and starting it from scratch
# Note: It only works on Anaconda environment
$CommandString = "conda activate ${EnvironmentPath}"
Write-Host "CommandString = '${CommandString}'" -ForegroundColor Red
$ResultString = cmd /c $CommandString '2>&1'
Write-Host "${ResultString}" -ForegroundColor Yellow

# Uninstallation
# For the different source of installation, you can remove these package through:

$CommandString = "python -m pip uninstall jupyter --yes"
Write-Host "CommandString = '${CommandString}'" -ForegroundColor Red
$ResultString = cmd /c $CommandString '2>&1'
Write-Host "${ResultString}" -ForegroundColor Yellow

$CommandString = "python -m pip uninstall jupyter_contrib_nbextensions --yes"
Write-Host "CommandString = '${CommandString}'" -ForegroundColor Red
$ResultString = cmd /c $CommandString '2>&1'
Write-Host "${ResultString}" -ForegroundColor Yellow

$CommandString = "python -m pip uninstall jupyter_nbextensions_configurator --yes"
Write-Host "CommandString = '${CommandString}'" -ForegroundColor Red
$ResultString = cmd /c $CommandString '2>&1'
Write-Host "${ResultString}" -ForegroundColor Yellow

# or

$CommandString = "conda remove --force jupyter notebook --yes --prefix ${EnvironmentPath}"
Write-Host "CommandString = '${CommandString}'" -ForegroundColor Red
$ResultString = cmd /c $CommandString '2>&1'
Write-Host "${ResultString}" -ForegroundColor Yellow

$CommandString = "conda remove --force jupyter_nbextensions_configurator --yes --prefix ${EnvironmentPath}"
Write-Host "CommandString = '${CommandString}'" -ForegroundColor Red
$ResultString = cmd /c $CommandString '2>&1'
Write-Host "${ResultString}" -ForegroundColor Yellow

$CommandString = "conda remove --force jupyter_contrib_nbextensions --yes --prefix ${EnvironmentPath}"
Write-Host "CommandString = '${CommandString}'" -ForegroundColor Red
$ResultString = cmd /c $CommandString '2>&1'
Write-Host "${ResultString}" -ForegroundColor Yellow

# But I'd advise you to run both of the above commands

# Installation
# It's better to install all the packages from anaconda:

$CommandString = "conda install jupyter notebook --yes --prefix ${EnvironmentPath}"
Write-Host "CommandString = '${CommandString}'" -ForegroundColor Red
$ResultString = cmd /c $CommandString '2>&1'
Write-Host "${ResultString}" -ForegroundColor Yellow

$CommandString = "conda update notebook --yes --prefix ${EnvironmentPath}"
Write-Host "CommandString = '${CommandString}'" -ForegroundColor Red
$ResultString = cmd /c $CommandString '2>&1'
Write-Host "${ResultString}" -ForegroundColor Yellow

$CommandString = "conda install -c conda-forge jupyter_nbextensions_configurator --yes --prefix ${EnvironmentPath}"
Write-Host "CommandString = '${CommandString}'" -ForegroundColor Red
$ResultString = cmd /c $CommandString '2>&1'
Write-Host "${ResultString}" -ForegroundColor Yellow

$CommandString = "conda install -c conda-forge jupyter_contrib_nbextensions --yes --prefix ${EnvironmentPath}"
Write-Host "CommandString = '${CommandString}'" -ForegroundColor Red
$ResultString = cmd /c $CommandString '2>&1'
Write-Host "${ResultString}" -ForegroundColor Yellow

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
Write-Host "CommandString = '${CommandString}'" -ForegroundColor Red
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