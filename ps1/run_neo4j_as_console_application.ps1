
# https://neo4j.com/docs/operations-manual/current/installation/windows
# Run this in a PowerShell window:
# 
# conda activate base; cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\ps1; cls; .\run_neo4j_as_console_application.ps1
#
# Stop the server by typing Ctrl-C in the console

# Change directory to the top-level extracted directory
$OldPath = Get-Location
cd C:\neo4j
cls

Write-Host ""
Write-Host "-----------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                         Running Neo4j as a console" -ForegroundColor Green
Write-Host "-----------------------------------------------------------------------------" -ForegroundColor Green
bin\neo4j console --verbose
# "C:\Program Files\Java\jdk-11\bin\java.exe" -cp C:\neo4j\plugins\*;C:\neo4j\conf\*;C:\neo4j\lib\* -XX:+UseG1GC -XX:-OmitStackTraceInFastThrow -XX:+AlwaysPreTouch -XX:+UnlockExperimentalVMOptions -XX:+TrustFinalNonStaticFields -XX:+DisableExplicitGC -XX:MaxInlineLevel=15 -XX:-UseBiasedLocking -Djdk.nio.maxCachedBufferSize=262144 -Dio.netty.tryReflectionSetAccessible=true -Djdk.tls.ephemeralDHKeySize=2048 -Djdk.tls.rejectClientInitiatedRenegotiation=true -XX:FlightRecorderOptions=stackdepth=256 -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints -Dlog4j2.disable.jmx=true -Dfile.encoding=UTF-8 org.neo4j.server.CommunityEntryPoint --home-dir=C:\neo4j --config-dir=C:\neo4j\conf

cd $OldPath