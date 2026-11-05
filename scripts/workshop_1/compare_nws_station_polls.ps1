param(
    [Parameter(Mandatory = $true)]
    [string]$FirstPollPath,

    [Parameter(Mandatory = $true)]
    [string]$SecondPollPath
)

$ErrorActionPreference = "Stop"

function Get-FeatureMap {
    param([object[]]$Features)

    $result = @{}
    foreach ($feature in $Features) {
        if ([string]::IsNullOrWhiteSpace([string]$feature.id)) {
            throw "A station-observation feature has no id."
        }
        if ($result.ContainsKey([string]$feature.id)) {
            throw "Duplicate feature id within one poll: $($feature.id)"
        }
        $result[[string]$feature.id] = $feature
    }
    return $result
}

function ConvertTo-StableFeatureText {
    param([object]$Feature)
    return ($Feature | ConvertTo-Json -Depth 100 -Compress)
}

$firstResolved = (Resolve-Path -LiteralPath $FirstPollPath).Path
$secondResolved = (Resolve-Path -LiteralPath $SecondPollPath).Path
$firstPayload = Get-Content -Raw -LiteralPath $firstResolved | ConvertFrom-Json
$secondPayload = Get-Content -Raw -LiteralPath $secondResolved | ConvertFrom-Json
$firstFeatures = @($firstPayload.features)
$secondFeatures = @($secondPayload.features)
$firstMap = Get-FeatureMap -Features $firstFeatures
$secondMap = Get-FeatureMap -Features $secondFeatures

$firstIds = @($firstMap.Keys | Sort-Object)
$secondIds = @($secondMap.Keys | Sort-Object)
$sharedIds = @($firstIds | Where-Object { $secondMap.ContainsKey($_) })
$firstOnlyIds = @($firstIds | Where-Object { -not $secondMap.ContainsKey($_) })
$secondOnlyIds = @($secondIds | Where-Object { -not $firstMap.ContainsKey($_) })

$changedIds = @()
$unchangedIds = @()
$sameTimestampChangedIds = @()
foreach ($id in $sharedIds) {
    $firstText = ConvertTo-StableFeatureText -Feature $firstMap[$id]
    $secondText = ConvertTo-StableFeatureText -Feature $secondMap[$id]
    if ($firstText -eq $secondText) {
        $unchangedIds += $id
    }
    else {
        $changedIds += $id
        if ($firstMap[$id].properties.timestamp -eq $secondMap[$id].properties.timestamp) {
            $sameTimestampChangedIds += $id
        }
    }
}

[pscustomobject]@{
    FirstPollPath = $firstResolved
    SecondPollPath = $secondResolved
    FirstFeatureCount = $firstFeatures.Count
    SecondFeatureCount = $secondFeatures.Count
    SharedIds = $sharedIds.Count
    FirstOnlyIds = $firstOnlyIds.Count
    SecondOnlyIds = $secondOnlyIds.Count
    UnchangedSharedPayloads = $unchangedIds.Count
    ChangedSharedPayloads = $changedIds.Count
    SameTimestampChangedPayloads = $sameTimestampChangedIds.Count
    ChangedIds = $changedIds
    SameTimestampChangedIds = $sameTimestampChangedIds
}
