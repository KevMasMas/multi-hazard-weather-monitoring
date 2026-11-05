param(
    [string]$ArchivePath = "data/raw/noaa_storm_events/details/year=2024/StormEvents_details-ftp_v1.0_d2024_c20260728.csv.gz",
    [string]$OutputPath = "workshop_1/samples/noaa_storm_events/details_sample.csv"
)

$ErrorActionPreference = "Stop"

$resolvedArchive = (Resolve-Path -LiteralPath $ArchivePath).Path
$decompressedCsv = [System.IO.Path]::ChangeExtension($resolvedArchive, $null)

if (-not (Test-Path -LiteralPath $decompressedCsv)) {
    $inputStream = [System.IO.File]::OpenRead($resolvedArchive)
    try {
        $gzipStream = [System.IO.Compression.GzipStream]::new(
            $inputStream,
            [System.IO.Compression.CompressionMode]::Decompress
        )
        try {
            $outputStream = [System.IO.File]::Create($decompressedCsv)
            try {
                $gzipStream.CopyTo($outputStream)
            }
            finally {
                $outputStream.Dispose()
            }
        }
        finally {
            $gzipStream.Dispose()
        }
    }
    finally {
        $inputStream.Dispose()
    }
}

$hazardTypes = @(
    "Heavy Rain",
    "Flash Flood",
    "Flood",
    "Strong Wind",
    "High Wind",
    "Thunderstorm Wind",
    "Excessive Heat",
    "Heat",
    "Cold/Wind Chill",
    "Extreme Cold/Wind Chill",
    "Heavy Snow",
    "Ice Storm",
    "Winter Storm",
    "Winter Weather"
)

$candidateRows = @(
    Import-Csv -LiteralPath $decompressedCsv |
        Where-Object {
            $_.STATE -eq "OKLAHOMA" -and
            $_.EVENT_TYPE -in $hazardTypes
        }
)

$sortedCandidates = @(
    $candidateRows |
        Sort-Object `
            { [int]$_.BEGIN_YEARMONTH },
            { [int]$_.BEGIN_DAY },
            { [int]$_.BEGIN_TIME },
            { [int]$_.EVENT_ID }
)

# Seed the sample with up to 25 records from every requested event type. Then
# fill the remaining slots chronologically. This keeps rare hazard families in
# the evidence while remaining deterministic.
$seedRows = @(
    foreach ($hazardType in $hazardTypes) {
        $sortedCandidates |
            Where-Object { $_.EVENT_TYPE -eq $hazardType } |
            Select-Object -First 25
    }
)

$selectedEventIds = @{}
foreach ($row in $seedRows) {
    $selectedEventIds[$row.EVENT_ID] = $true
}

$remainingSlots = 250 - $seedRows.Count
$fillRows = @(
    $sortedCandidates |
        Where-Object { -not $selectedEventIds.ContainsKey($_.EVENT_ID) } |
        Select-Object -First $remainingSlots
)

$sampleRows = @(
    $seedRows + $fillRows |
        Sort-Object `
            { [int]$_.BEGIN_YEARMONTH },
            { [int]$_.BEGIN_DAY },
            { [int]$_.BEGIN_TIME },
            { [int]$_.EVENT_ID }
)

if ($sampleRows.Count -lt 200) {
    throw "The filtered source produced only $($sampleRows.Count) rows; at least 200 are required."
}

$outputDirectory = Split-Path -Parent $OutputPath
New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null
$sampleRows | Export-Csv -LiteralPath $OutputPath -NoTypeInformation -Encoding utf8

$outputHash = Get-FileHash -Algorithm SHA256 -LiteralPath $OutputPath

[pscustomobject]@{
    CandidateRows = $candidateRows.Count
    SampleRows = $sampleRows.Count
    Columns = @($sampleRows[0].PSObject.Properties.Name).Count
    DistinctEventIds = @($sampleRows.EVENT_ID | Sort-Object -Unique).Count
    OutputPath = (Resolve-Path -LiteralPath $OutputPath).Path
    Sha256 = $outputHash.Hash
}

