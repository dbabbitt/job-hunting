
# https://neo4j.com/docs/operations-manual/current/installation/windows
# Run this in a PowerShell window:
# 
# D:
# cd D:\Documents\GitHub\job-hunting\ps1
# cls
# .\run_anaconda3_from_docker_container.ps1

# Set up global variables
$HostPort = "8888"
$ContainerPort = "8888"
$RepositoriesDirectory = "D:\Documents\GitHub"

$OldPath = Get-Location

Write-Host ""
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                         Running Neo4j from Docker" -ForegroundColor Green
Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
docker run --name=anaconda3 -i -t -v ${RepositoriesDirectory}:/opt/notebooks -p ${HostPort}:${ContainerPort} continuumio/anaconda3 /bin/bash -c "conda install jupyter -y --quiet && mkdir -p /opt/notebooks && jupyter notebook --notebook-dir=/opt/notebooks --ip='*' --port=${ContainerPort} --no-browser --allow-root"

cd $OldPath