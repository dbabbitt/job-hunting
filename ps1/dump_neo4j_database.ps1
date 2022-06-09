
# https://neo4j.com/docs/operations-manual/current/backup-restore/offline-backup/
# Stop the neo4j database and run this in a PowerShell window:
# 
# conda activate base
# cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\ps1
# cls
# .\dump_neo4j_database.ps1

# Change directory to the top-level extracted directory
$OldPath = Get-Location
cd C:\neo4j
cls

Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                     Dumping Neo4j to a Time-stamped File" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
$timestamp = Get-Date -format "yyyyMMdd";
$CommandString = "bin/neo4j-admin dump --database=neo4j --to=C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\saves\dumps\neo4j-${timestamp}.dump"
# Write-Host "CommandString = '${CommandString}'" -ForegroundColor Red
Invoke-Expression $CommandString

cd $OldPath