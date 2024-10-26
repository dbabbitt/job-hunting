
# https://neo4j.com/docs/operations-manual/current/installation/windows
# Run this in a PowerShell window:
# 
# conda activate base; cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\ps1; cls; .\copy_neo4j_database_to_other_server.ps1

# Record previous directory
$OldPath = Get-Location

# Clear the screen
cls

# Function to switch Neo4j servers and Java versions
function Switch-Neo4j {
    param (
        [string]$version = "4.4.7"
    )
    
    switch ($version) {
        "4.4.7" {
            $env:NEO4J_HOME = "C:\neo4j"
            $env:JAVA_HOME = "C:\Program Files\Java\jdk-11"
        }
        "5.13.0" {
            $env:NEO4J_HOME = "C:\neo4j-community-5.13.0-windows"
            $env:JAVA_HOME = "C:\Program Files\Java\jdk-17"
        }
        "5.24.2" {
            $env:NEO4J_HOME = "C:\neo4j-community-5.24.2"
            $env:JAVA_HOME = "C:\Program Files\Java\jdk-23.0.1"
        }
        default {
            Write-Output "Invalid version specified. Use '4.4.7', '5.13.0', or '5.24.2'."
            return
        }
    }
    
    # Update PATH to include the correct Neo4j directory
    $newPath = ($env:PATH -split ";") -replace "C:\\neo4j.*?\\bin", "$env:NEO4J_HOME\bin"
    $env:PATH = ($newPath -join ";")
    
    # Update PATH to include the correct Java bin directory
    $newPath = ($env:PATH -split ";") -replace "C:\\Program Files\\Java\\jdk-.*?\\bin", "$env:JAVA_HOME\bin"
    $env:PATH = ($newPath -join ";")

    # Change directory to the selected Neo4j home
    if ($env:NEO4J_HOME) {
        Set-Location -Path $env:NEO4J_HOME
        Write-Host "Changed directory to $env:NEO4J_HOME" -ForegroundColor Yellow
    } else {
        Write-Host "NEO4J_HOME environment variable is not set." -ForegroundColor Red
        Write-Host "Changing directory to C:\neo4j." -ForegroundColor Yellow
        cd C:\neo4j
    }
}

$fromVersion = "5.24.2"
$toVersion = "5.13.0"

Write-Host ""
Write-Host "-----------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                     Copying neo4j Database to $toVersion Server" -ForegroundColor Green
Write-Host "-----------------------------------------------------------------------------" -ForegroundColor Green

Switch-Neo4j -version $fromVersion
Write-Host "Stop the $fromVersion Neo4j server" -ForegroundColor Yellow
cmd.exe /c "$env:NEO4J_HOME\bin\neo4j stop"

# Dump the database
Write-Host "Dump the $fromVersion Neo4j database" -ForegroundColor Yellow

# Create the directory if not exists
$dumpsFolder = "$env:NEO4J_HOME\data\dumps"
if (-Not (Test-Path -Path $dumpsFolder)) {
    New-Item -Path $dumpsFolder -ItemType Directory
}

# Delete the previous file if exists
$archivePath = "$dumpsFolder\neo4j.dump"
if (Test-Path $archivePath) {
    Remove-Item $archivePath -Force
}

switch ($fromVersion) {
    "4.4.7" {
        cmd.exe /c "$env:NEO4J_HOME\bin\neo4j-admin dump --database=neo4j --to=$dumpsFolder --verbose"
    }
    default {
        cmd.exe /c "$env:NEO4J_HOME\bin\neo4j-admin database dump --verbose --overwrite-destination=true --to-path=$dumpsFolder neo4j"
    }
}

Switch-Neo4j -version $toVersion
Write-Host "Stop the $toVersion Neo4j server" -ForegroundColor Yellow
cmd.exe /c "$env:NEO4J_HOME\bin\neo4j stop"

Write-Host "Load the database dump into the $toVersion Neo4j server" -ForegroundColor Yellow
switch ($toVersion) {
    "4.4.7" {
        # cmd.exe /c "$env:NEO4J_HOME\bin\neo4j-admin load -h"
        cmd.exe /c "$env:NEO4J_HOME\bin\neo4j-admin load --force --verbose --database=neo4j --from=$archivePath"
    }
    default {
        cmd.exe /c "$env:NEO4J_HOME\bin\neo4j-admin database load --from-path=$dumpsFolder neo4j --overwrite-destination=true"
    }
}

# Pause to keep the window open
Read-Host -Prompt "Press Enter to continue"

switch ($toVersion) {
    "4.4.7" {
        Write-Host "Migrate the neo4j database to the earlier AF format" -ForegroundColor Yellow
        cmd.exe /c "$env:NEO4J_HOME\bin\neo4j-admin migrate"
    }
    default {
        Write-Host "Migrate the neo4j database to the AF4.3.0 format" -ForegroundColor Yellow
        cmd.exe /c "$env:NEO4J_HOME\bin\neo4j-admin database migrate neo4j"
    }
}

# Change directory to previous
Set-Location -Path $OldPath

# Pause to keep the window open
Read-Host -Prompt "Press Enter to exit"