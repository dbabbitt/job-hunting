
# https://neo4j.com/docs/operations-manual/current/installation/windows
# Run this in a PowerShell window:
# 
# D:
# cd D:\Documents\GitHub\job-hunting\ps1
# cls
# .\run_neo4j_from_docker_container.ps1

# Set up global variables
$DbmsConnectorHttpListenAddress = "7474"
$DbmsConnectorBoltListenAddress = "7687"
$DataVolume = "$HOME/neo4j/data"
$ImportVolume = "$HOME/neo4j/import"

$OldPath = Get-Location

Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                         Running Neo4j from Docker" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
docker run --publish=${DbmsConnectorHttpListenAddress}:${DbmsConnectorHttpListenAddress} --publish=${DbmsConnectorBoltListenAddress}:${DbmsConnectorBoltListenAddress} --volume=${DataVolume}:/data --volume=${ImportVolume}:/var/lib/neo4j/import neo4j

cd $OldPath