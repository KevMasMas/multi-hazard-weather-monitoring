param(
    [ValidatePattern("^[A-Z]{2}$")]
    [string]$Area = "OK",

    [string]$RawDirectory = "data/raw/nws_alerts",

    [ValidateRange(1, 50)]
    [int]$MaxPages = 20,

    [ValidateRange(0, 300)]
    [int]$DelaySeconds = 30,

    [string]$UserAgent = "multi-hazard-weather-monitoring/0.1 (github.com/KevMasMas/multi-hazard-weather-monitoring)"
)

$ErrorActionPreference = "Stop"

if ($PSVersionTable.PSVersion.Major -lt 6) {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
}

$headers = @{
    "User-Agent" = $UserAgent
    "Accept" = "application/geo+json"
}

$captureTimestamp = [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssZ")
$nextUri = "https://api.weather.gov/alerts?area=$Area"
$pageNumber = 0
$pageSummaries = @()

New-Item -ItemType Directory -Force -Path $RawDirectory | Out-Null

while (-not [string]::IsNullOrWhiteSpace($nextUri)) {
    $pageNumber++
    if ($pageNumber -gt $MaxPages) {
        throw "Pagination exceeded MaxPages=$MaxPages. No complete-response claim can be made."
    }

    if ($pageNumber -gt 1 -and $DelaySeconds -gt 0) {
        Start-Sleep -Seconds $DelaySeconds
    }

    $rawPath = Join-Path $RawDirectory (
        "recent_7d_{0}_{1}_page_{2}.geojson" -f $Area, $captureTimestamp, $pageNumber
    )

    $response = Invoke-WebRequest `
        -UseBasicParsing `
        -Uri $nextUri `
        -Headers $headers `
        -OutFile $rawPath `
        -PassThru

    $payload = Get-Content -Raw -LiteralPath $rawPath | ConvertFrom-Json
    $features = @($payload.features)
    $hash = Get-FileHash -Algorithm SHA256 -LiteralPath $rawPath

    $pageSummaries += [pscustomobject]@{
        Page = $pageNumber
        RequestUri = $nextUri
        StatusCode = [int]$response.StatusCode
        FeatureCount = $features.Count
        RawPath = (Resolve-Path -LiteralPath $rawPath).Path
        RawBytes = (Get-Item -LiteralPath $rawPath).Length
        Sha256 = $hash.Hash
        NextUri = [string]$payload.pagination.next
    }

    $nextUri = [string]$payload.pagination.next
}

$pageSummaries

