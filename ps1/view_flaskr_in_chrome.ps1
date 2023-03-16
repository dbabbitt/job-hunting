
# cd $Env:UserProfile\OneDrive\Documents\GitHub\job-hunting\ps1
# cls
# .\view_flaskr_in_chrome.ps1

# Launch Flaskr App
$FlaskrUrl = "http://localhost:5000"
$HttpRequest = [System.Net.WebRequest]::Create($FlaskrUrl)
$HttpStatus = 500
try {
    $HttpResponse = $HttpRequest.GetResponse()
    $HttpStatus = [int]$HttpResponse.StatusCode
}
catch [System.Management.Automation.MethodInvocationException] {
    Write-Host ""
    Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
    Write-Host "              Launching the flaskr app in its own window" -ForegroundColor Green
    Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
    $argList = "-file `"$PowerScriptsDirectory\launch_job_hunting_flask_app.ps1`" -NoExit"
    Start-Process PowerShell -argumentlist $argList
    Read-Host "Verify the Flask server is running, then press ENTER to continue..."
}
finally {
    If ($HttpResponse -ne $null) {
        $HttpResponse.Close()
    }
}

# Open the webpage in Chrome
$HttpRequest = [System.Net.WebRequest]::Create($FlaskrUrl)
try {
    $HttpResponse = $HttpRequest.GetResponse()
    $HttpStatus = [int]$HttpResponse.StatusCode
    If ($HttpStatus -eq 200) {
        Write-Host ""
        Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
        Write-Host "                  Opening the flaskr app in Chrome" -ForegroundColor Green
        Write-Host "-------------------------------------------------------------------------------" -ForegroundColor Green
        Start-Process "chrome.exe" $FlaskrUrl
    }
}
catch [System.Management.Automation.MethodInvocationException] {
    Write-Host "Ran into an issue: ${PSItem} Check the debug output in the flaskr app window." -ForegroundColor Red
}
finally {
    If ($HttpResponse -ne $null) {
        $HttpResponse.Close()
    }
}