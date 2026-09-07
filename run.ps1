param(
    [string]$Test = "tests/"
)

$ResultsDir = "allure-results"
Write-Host "`n==> Running tests..." -ForegroundColor Cyan
python -m pytest $Test
Write-Host "`n==> Opening HTML report..." -ForegroundColor Cyan
$allureCli = Get-Command allure -ErrorAction SilentlyContinue
if ($allureCli) {
    allure serve $ResultsDir
} elseif (Test-Path "report.html") {
    Write-Host "[+] Allure CLI not found. Opening standalone HTML report (report.html)..." -ForegroundColor Green
    Start-Process "report.html"
} else {
    Write-Host "[!] No report generated." -ForegroundColor Yellow
}
