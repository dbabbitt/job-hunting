
# https://neo4j.com/docs/operations-manual/current/installation/windows
# Run this in a PowerShell window:
# 
# conda activate base; cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\ps1; cls; .\run_neo4j_as_console_application.ps1
#
# Stop the server by typing Ctrl-C in the console

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

# Call the function with the desired version
Switch-Neo4j -version "5.24.2"

Write-Host ""
Write-Host "-----------------------------------------------------------------------------" -ForegroundColor Green
Write-Host "                         Running Neo4j as a console" -ForegroundColor Green
Write-Host "-----------------------------------------------------------------------------" -ForegroundColor Green
bin\neo4j console --verbose
# "C:\Program Files\Java\jdk-11\bin\java.exe" -cp C:\neo4j\plugins\*;C:\neo4j\conf\*;C:\neo4j\lib\* -XX:+UseG1GC -XX:-OmitStackTraceInFastThrow -XX:+AlwaysPreTouch -XX:+UnlockExperimentalVMOptions -XX:+TrustFinalNonStaticFields -XX:+DisableExplicitGC -XX:MaxInlineLevel=15 -XX:-UseBiasedLocking -Djdk.nio.maxCachedBufferSize=262144 -Dio.netty.tryReflectionSetAccessible=true -Djdk.tls.ephemeralDHKeySize=2048 -Djdk.tls.rejectClientInitiatedRenegotiation=true -XX:FlightRecorderOptions=stackdepth=256 -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints -Dlog4j2.disable.jmx=true -Dfile.encoding=UTF-8 org.neo4j.server.CommunityEntryPoint --home-dir=C:\neo4j --config-dir=C:\neo4j\conf

# Change directory to the top-level extracted directory
cd $OldPath