param(
    [ValidatePattern("^[A-Z]{2}$")]
    [string]$Area = "OK",

    [ValidatePattern("^poll_[0-9]+$")]
    [string]$PollLabel = "poll_1",

    [string]$RawDirectory = "data/raw/nws_alerts",

    [string]$UserAgent = "multi-hazard-weather-monitoring/0.1 (github.com/KevMasMas/multi-hazard-weather-monitoring)"
)

$ErrorActionPreference = "Stop"

# Windows PowerShell 5.1 may otherwise negotiate an obsolete TLS version.
if ($PSVersionTable.PSVersion.Major -lt 6) {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
}

$headers = @{
    "User-Agent" = $UserAgent
    "Accept" = "application/geo+json"
}

$retrievedAtUtc = [DateTime]::UtcNow
$timestamp = $retrievedAtUtc.ToString("yyyyMMddTHHmmssZ")
$requestUri = "https://api.weather.gov/alerts/active?area=$Area"

New-Item -ItemType Directory -Force -Path $RawDirectory | Out-Null

$rawPath = Join-Path $RawDirectory "${PollLabel}_active_${Area}_${timestamp}.geojson"
$headersPath = Join-Path $RawDirectory "${PollLabel}_active_${Area}_${timestamp}_response_headers.json"

$response = Invoke-WebRequest `
    -Uri $requestUri `
    -Headers $headers `
    -UseBasicParsing `
    -OutFile $rawPath `
    -PassThru

$responseHeaders = [ordered]@{}
foreach ($headerName in $response.Headers.Keys) {
    $responseHeaders[$headerName] = @($response.Headers[$headerName])
}
$responseHeaders | ConvertTo-Json -Depth 5 |
    Set-Content -LiteralPath $headersPath -Encoding utf8

$payload = Get-Content -Raw -LiteralPath $rawPath | ConvertFrom-Json
$features = @($payload.features)
$featureIds = @($features | ForEach-Object { $_.id })
$hash = Get-FileHash -Algorithm SHA256 -LiteralPath $rawPath

[pscustomobject]@{
    PollLabel = $PollLabel
    RequestUri = $requestUri
    RetrievedAtUtc = $retrievedAtUtc.ToString("o")
    StatusCode = [int]$response.StatusCode
    ContentType = [string]$response.Headers["Content-Type"]
    FeatureCount = $features.Count
    DistinctFeatureIds = @($featureIds | Sort-Object -Unique).Count
    MissingGeometry = @($features | Where-Object { $null -eq $_.geometry }).Count
    RawPath = (Resolve-Path -LiteralPath $rawPath).Path
    RawBytes = (Get-Item -LiteralPath $rawPath).Length
    Sha256 = $hash.Hash
    ResponseHeadersPath = (Resolve-Path -LiteralPath $headersPath).Path
    UserAgent = $UserAgent
}

