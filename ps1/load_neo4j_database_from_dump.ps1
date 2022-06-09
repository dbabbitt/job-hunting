
# https://neo4j.com/docs/operations-manual/current/backup-restore/restore-dump/
# Stop the neo4j database and run this in a PowerShell window:
# 
# conda activate base
# cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\ps1
# cls
# .\load_neo4j_database_from_dump.ps1

# Change directory to the top-level extracted directory
$OldPath = Get-Location
cd C:\neo4j
cls

Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                     Loading Neo4j from a Dump File" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
$TimeStamp = Get-Date -format "yyyyMMdd";
$DumpName = Read-Host -Prompt "Dump name [neo4j-${TimeStamp}.dump]"
If ([string]::IsNullOrWhiteSpace($DumpName)) {
	$DumpName = "neo4j-${TimeStamp}.dump"
}
$CommandString = "bin/neo4j-admin load --from=C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\saves\dumps\${DumpName} --database=neo4j --force"
# Write-Host "CommandString = '${CommandString}'" -ForegroundColor Red
Invoke-Expression $CommandString

cd $OldPath