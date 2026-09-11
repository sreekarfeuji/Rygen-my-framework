param(
    [string]$Test = "tests/",
    [string]$Browser = "c",
    [ValidateRange(0, 2147483647)]
    [int]$Workers = 0
)

if ($Test -in @("c", "m", "f")) {
    if ($PSBoundParameters.ContainsKey("Browser")) {
        $RequestedWorkers = 0
        if ($PSBoundParameters.ContainsKey("Workers") -or
            -not [int]::TryParse($Browser, [ref]$RequestedWorkers) -or
            $RequestedWorkers -lt 1) {
            throw "Usage: .\run.ps1 m 2 (worker count must be a positive integer)"
        }
        $Workers = $RequestedWorkers
    }
    $Browser = $Test
    $Test = "tests/"
}

if ($Browser -notin @("c", "m", "f")) {
    throw "Browser must be c (Chrome), m (Edge), or f (Firefox)."
}

$WorkerArgs = @()
$RunMode = "sequentially"
if ($Workers -gt 0) {
    $WorkerArgs = @("-n", [string]$Workers)
    $RunMode = "with $Workers parallel workers"
}

switch ($Browser) {
    "c" {
        $BrowserName = "Google Chrome"
        $BrowserArgs = @("--browser", "chromium", "--browser-channel", "chrome")
    }
    "m" {
        $BrowserName = "Microsoft Edge"
        $BrowserArgs = @("--browser", "chromium", "--browser-channel", "msedge")
    }
    "f" {
        $BrowserName = "Firefox"
        $BrowserArgs = @("--browser", "firefox")
    }
}
$ResultsDir = Join-Path $PSScriptRoot "reports/allure-results"
$HtmlReport = Join-Path $PSScriptRoot "reports/report.html"
Push-Location $PSScriptRoot
try {
    Write-Host "`n==> Running tests on $BrowserName $RunMode..." -ForegroundColor Cyan
    python -m pytest $Test @BrowserArgs @WorkerArgs
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
