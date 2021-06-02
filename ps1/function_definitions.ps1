
function Format-Json {
    <#
    .SYNOPSIS
        Prettifies JSON output.
    .DESCRIPTION
        Reformats a JSON string so the output looks better than what ConvertTo-Json outputs.
    .PARAMETER Json
        Required: [string] The JSON text to prettify.
    .PARAMETER Minify
        Optional: Returns the json string compressed.
    .PARAMETER Indentation
        Optional: The number of spaces (1..1024) to use for indentation. Defaults to 4.
    .PARAMETER AsArray
        Optional: If set, the output will be in the form of a string array, otherwise a single string is output.
    .EXAMPLE
        $json | ConvertTo-Json | Format-Json -Indentation 2
    #>
    [CmdletBinding(DefaultParameterSetName = 'Prettify')]
    Param(
        [Parameter(Mandatory = $true, Position = 0, ValueFromPipeline = $true)]
        [string]$Json,

        [Parameter(ParameterSetName = 'Minify')]
        [switch]$Minify,

        [Parameter(ParameterSetName = 'Prettify')]
        [ValidateRange(1, 1024)]
        [int]$Indentation = 4,

        [Parameter(ParameterSetName = 'Prettify')]
        [switch]$AsArray
    )

    if ($PSCmdlet.ParameterSetName -eq 'Minify') {
        return ($Json | ConvertFrom-Json) | ConvertTo-Json -Depth 100 -Compress
    }

    # If the input JSON text has been created with ConvertTo-Json -Compress
    # then we first need to reconvert it without compression
    if ($Json -notmatch '\r?\n') {
        $Json = ($Json | ConvertFrom-Json) | ConvertTo-Json -Depth 100
    }

    $indent = 0
    $regexUnlessQuoted = '(?=([^"]*"[^"]*")*[^"]*$)'

    $result = $Json -split '\r?\n' |
        ForEach-Object {
            # If the line contains a ] or } character, 
            # we need to decrement the indentation level unless it is inside quotes.
            if ($_ -match "[}\]]$regexUnlessQuoted") {
                $indent = [Math]::Max($indent - $Indentation, 0)
            }

            # Replace all colon-space combinations by ": " unless it is inside quotes.
            $line = (' ' * $indent) + ($_.TrimStart() -replace ":\s+$regexUnlessQuoted", ': ')

            # If the line contains a [ or { character, 
            # we need to increment the indentation level unless it is inside quotes.
            if ($_ -match "[\{\[]$regexUnlessQuoted") {
                $indent += $Indentation
            }

            $line
        }

    if ($AsArray) { return $result }
    return $result -Join [Environment]::NewLine
}

function Add-Python-Executable-To-Path {
    <#
    .SYNOPSIS
        Adds python's executable path associated with the environment to the PATH if necessary.
    .EXAMPLE
        Add-Python-Executable-To-Path $EnvironmentPath
    #>
    [CmdletBinding(DefaultParameterSetName = 'EnvironmentPath')]
    Param(
        [Parameter(Mandatory = $true, Position = 0, ValueFromPipeline = $true)]
        [string]$EnvironmentPath
    )
	$ExecutablePath = "${EnvironmentPath}\python.exe"
	$PathArray = $ExecutablePath -Split "\\"
	$PythonFolder = $PathArray[0..($PathArray.count - 2)] -Join "\"
	if (!($env:Path -Like "*$PythonFolder*")) {
		# Write-Host "The ${EnvironmentPath} executable path is not in PATH" -ForegroundColor Red
		$env:Path = "${EnvironmentPath};" + $env:Path
	}
}

function Get-Python-Version {
    <#
    .SYNOPSIS
        Get the version of python associated with the environment.
    .EXAMPLE
        $PythonVersion = Get-Python-Version $EnvironmentPath
    #>
    [CmdletBinding(DefaultParameterSetName = 'EnvironmentPath')]
    Param(
        [Parameter(Mandatory = $true, Position = 0, ValueFromPipeline = $true)]
        [string]$EnvironmentPath
    )
	$CommandString = "cd ${EnvironmentPath} & python --version"
	$PythonVersion = cmd /c $CommandString '2>&1'
	$PythonVersion = $PythonVersion.Trim()
	
	Return $PythonVersion
}

function Add-Kernel-To-Launcher {
    <#
    .SYNOPSIS
        Adds python's executable path associated with the environment to the PATH if necessary.
    .EXAMPLE
        Add-Kernel-To-Launcher $EnvironmentPath -DisplayName $DisplayName
    #>
    [CmdletBinding(DefaultParameterSetName = 'EnvironmentPath')]
    Param(
        [Parameter(Mandatory = $true, Position = 0, ValueFromPipeline = $true)]
        [string]$EnvironmentPath,
		
        [Parameter(ParameterSetName = 'DisplayName')]
        [string]$DisplayName = "Python"
    )
	$PythonVersion = Get-Python-Version $EnvironmentPath
	
	$ExecutablePath = "${EnvironmentPath}\python.exe"
	
	# Fix LookupError: unknown encoding: cp65001
	$CommandString = -Join('cd ', $EnvironmentPath, ' & python -c "import os; os.environ[', "'PYTHONIOENCODING'", "] = 'UTF-8'", '"')
	# Write-Host "CommandString = '${CommandString}'" -ForegroundColor Gray
	cmd /c $CommandString '2>&1'
	
	$PathArray = $EnvironmentPath -Split "\\"
	$EnvironmentName = $PathArray[$PathArray.count - 1]
	$CommandString = -Join('cd ', $EnvironmentPath, ' & python -m ipykernel install --user --name ', $EnvironmentName, ' --display-name "', $DisplayName, ' (', $PythonVersion, ')"')
	# Write-Host "CommandString = '${CommandString}'" -ForegroundColor Gray
	cmd /c $CommandString '2>&1'
	# Invoke-Expression $CommandString
}

function Import-Workspace-File {
    <#
    .SYNOPSIS
        Import the local workspace file into the Jupyter Lab workspaces.
    .DESCRIPTION
        Returns the newly created workspace path.
    .EXAMPLE
        $WorkspacePath = Import-Workspace-File $RepositoryPath
    #>
    [CmdletBinding(DefaultParameterSetName = 'RepositoryPath')]
    Param(
        [Parameter(Mandatory = $true, Position = 0, ValueFromPipeline = $true)]
        [string]$RepositoryPath,
		
        [Parameter(ParameterSetName = 'RepositoriesDirectory')]
        [string]$RepositoriesDirectory = "D:\Documents\GitHub"
    )
	$CommandString = "cd ${RepositoriesDirectory}\${RepositoryPath} & python -m jupyterlab workspaces import workspace.json"
	# Write-Host "CommandString = '${CommandString}'" -ForegroundColor Red
	# $WorkspacePath = (jupyter-lab workspaces import workspace.json) | Out-String
	$WorkspacePath = cmd /c $CommandString '2>&1'
	# Write-Host "WorkspacePath = '${WorkspacePath}'" -ForegroundColor Red
	If ($WorkspacePath -Ne $null) {
		$WorkspacePath = $WorkspacePath.Trim()
		$WorkspacePath = $WorkspacePath -csplit ' '
		$WorkspacePath = $WorkspacePath[$WorkspacePath.Count - 1]
	}
	
	Return $WorkspacePath
}

function Add-Logos-To-Kernel-Folder {
    <#
    .SYNOPSIS
        Copy the 32x32 and 64x64 PNGs to the kernel folder if available.
    .EXAMPLE
        Add-Logos-To-Kernel-Folder $EnvironmentName -RepositoryPath $RepositoryPath
    #>
    Param(
        [Parameter(Mandatory = $true, Position = 0, ValueFromPipeline = $true)]
        [string]$EnvironmentName,
		
        [Parameter(ParameterSetName = 'RepositoryPath')]
        [string]$RepositoryPath,
		
        [Parameter(ParameterSetName = 'RepositoriesDirectory')]
        [string]$RepositoriesDirectory = "D:\Documents\GitHub"
    )
	$KernelFolder = "${Env:UserProfile}\AppData\Roaming\jupyter\kernels\${EnvironmentName}"
	$LogoFolder = "${RepositoriesDirectory}\${RepositoryPath}\saves\png"
	$SmallPath = "${LogoFolder}\logo-32x32.png"
	If (Test-Path -Path $SmallPath -PathType Leaf) {
		Copy-Item $SmallPath -Destination $KernelFolder
	}
	$LargePath = "${LogoFolder}\logo-64x64.png"
	If (Test-Path -Path $LargePath -PathType Leaf) {
		Copy-Item $LargePath -Destination $KernelFolder
	}
}

function Get-Token-String {
    <#
    .SYNOPSIS
        Get the token string from the running Jupyter Lab.
    .EXAMPLE
        $TokenString = Get-Token-String
    #>
	$ListResults = (python -m jupyter notebook list) | Out-String
	$TokenRegex = [regex] '(?m)http://localhost:8888/\?token=([^ ]+) :: '
	$TokenString = $TokenRegex.Match($ListResults).Groups[1].Value
	
	Return $TokenString
}