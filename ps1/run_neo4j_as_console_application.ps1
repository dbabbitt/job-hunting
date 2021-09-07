
# https://neo4j.com/docs/operations-manual/current/installation/windows
# Run this in a PowerShell window:
# 
# conda activate base
# D:
# cd D:\Documents\GitHub\job-hunting\ps1
# cls
# .\run_neo4j_as_console_application.ps1
#
# Stop the server by typing Ctrl-C in the console

# Change directory to the top-level extracted directory
$OldPath = Get-Location
cd C:\neo4j
cls

Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                     Running Neo4j as a console" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
bin\neo4j console

cd $OldPath