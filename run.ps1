param([string]$Test = "tests/")
$ResultsDir = Join-Path $PSScriptRoot "reports/allure-results"
$HtmlReport = Join-Path $PSScriptRoot "reports/report.html"
Push-Location $PSScriptRoot
try {
    Write-Host "`n==> Running tests..." -ForegroundColor Cyan
    python -m pytest $Test
    $TestExitCode = $LASTEXITCODE
    Write-Host "`n==> Opening HTML report..." -ForegroundColor Cyan
    $allureCli = Get-Command allure -ErrorAction SilentlyContinue
    if ($allureCli) {
        allure serve $ResultsDir
    } elseif (Test-Path -LiteralPath $HtmlReport) {
        Write-Host "[+] Allure CLI not found. Opening reports/report.html..." -ForegroundColor Green
        Start-Process -FilePath $HtmlReport
    } else {
        Write-Host "[!] No report generated." -ForegroundColor Yellow
    }
} finally {
    Pop-Location
}
exit $TestExitCode
