param(
    [ValidatePattern("^[A-Z0-9]{4}$")]
    [string]$StationId = "KOKC",

    [ValidatePattern("^(poll|page)_[0-9]+$")]
    [string]$PollLabel = "poll_1",

    [string]$Cursor = "",

    [ValidateRange(1, 500)]
    [int]$Limit = 200,

    [string]$RawDirectory = "data/raw/nws_station_observations",

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

$retrievedAtUtc = [DateTime]::UtcNow
$timestamp = $retrievedAtUtc.ToString("yyyyMMddTHHmmssZ")
if ([string]::IsNullOrWhiteSpace($Cursor)) {
    $requestUri = "https://api.weather.gov/stations/$StationId/observations?limit=$Limit"
}
else {
    $encodedCursor = [Uri]::EscapeDataString($Cursor)
    $requestUri = "https://api.weather.gov/stations/$StationId/observations?cursor=$encodedCursor"
}

New-Item -ItemType Directory -Force -Path $RawDirectory | Out-Null

$baseName = "${PollLabel}_${StationId}_${timestamp}"
$rawPath = Join-Path $RawDirectory "${baseName}.geojson"
$headersPath = Join-Path $RawDirectory "${baseName}_response_headers.json"
$metadataPath = Join-Path $RawDirectory "${baseName}_metadata.json"

$response = Invoke-WebRequest `
    -Uri $requestUri `
    -Headers $headers `
    -UseBasicParsing `
    -OutFile $rawPath `
    -PassThru

$responseHeaders = [ordered]@{}
foreach ($headerName in $response.Headers.Keys) {
    if ($headerName -ne "Set-Cookie") {
        $responseHeaders[$headerName] = @($response.Headers[$headerName])
    }
}
$responseHeaders | ConvertTo-Json -Depth 5 |
    Set-Content -LiteralPath $headersPath -Encoding utf8

$payload = Get-Content -Raw -LiteralPath $rawPath | ConvertFrom-Json
$features = @($payload.features)
$featureIds = @($features | ForEach-Object { $_.id })
$timestamps = @(
    $features |
        Where-Object { $null -ne $_.properties.timestamp } |
        ForEach-Object { [DateTimeOffset]$_.properties.timestamp }
)
$hash = Get-FileHash -Algorithm SHA256 -LiteralPath $rawPath

$oldestObservationUtc = $null
$newestObservationUtc = $null
if ($timestamps.Count -gt 0) {
    $oldestObservationUtc = ($timestamps | Sort-Object | Select-Object -First 1).ToUniversalTime().ToString("o")
    $newestObservationUtc = ($timestamps | Sort-Object | Select-Object -Last 1).ToUniversalTime().ToString("o")
}

$metadata = [ordered]@{
    poll_label = $PollLabel
    station_id = $StationId
    request_method = "GET"
    request_uri = $requestUri
    cursor_supplied = -not [string]::IsNullOrWhiteSpace($Cursor)
    retrieved_at_utc = $retrievedAtUtc.ToString("o")
    status_code = [int]$response.StatusCode
    content_type = [string]$response.Headers["Content-Type"]
    user_agent = $UserAgent
    feature_count = $features.Count
    distinct_feature_ids = @($featureIds | Sort-Object -Unique).Count
    missing_geometry = @($features | Where-Object { $null -eq $_.geometry }).Count
    oldest_observation_utc = $oldestObservationUtc
    newest_observation_utc = $newestObservationUtc
    next_page_present = [bool]$payload.pagination.next
    raw_file = (Resolve-Path -LiteralPath $rawPath).Path
    raw_bytes = (Get-Item -LiteralPath $rawPath).Length
    sha256 = $hash.Hash
    response_headers_file = (Resolve-Path -LiteralPath $headersPath).Path
}
$metadata | ConvertTo-Json -Depth 5 |
    Set-Content -LiteralPath $metadataPath -Encoding utf8

[pscustomobject]$metadata
