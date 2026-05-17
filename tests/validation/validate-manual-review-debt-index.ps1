param(
  [switch]$Update
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$indexRelativePath = 'data/exports/_index/manual-review-debt.json'
$indexPath = Join-Path $repoRoot $indexRelativePath
$datasets = @('official_raw', 'derived_metrics', 'supercombo_enrichment')

function ConvertTo-RelativePath {
  param([Parameter(Mandatory = $true)][string]$Path)

  $resolved = (Resolve-Path -LiteralPath $Path).Path
  return $resolved.Substring($repoRoot.Length + 1).Replace('\', '/')
}

function Test-Property {
  param(
    [Parameter(Mandatory = $true)][object]$Object,
    [Parameter(Mandatory = $true)][string]$Name
  )
  return $null -ne $Object.PSObject.Properties[$Name]
}

function Add-Count {
  param(
    [Parameter(Mandatory = $true)][hashtable]$Counts,
    [Parameter(Mandatory = $true)][string]$Key
  )

  if (-not $Counts.ContainsKey($Key)) {
    $Counts[$Key] = 0
  }
  $Counts[$Key] += 1
}

function ConvertTo-CountEntries {
  param([Parameter(Mandatory = $true)][hashtable]$Counts)

  return @(
    $Counts.GetEnumerator() |
      Sort-Object Name |
      ForEach-Object {
        [ordered]@{
          id = [string]$_.Name
          row_count = [int]$_.Value
        }
      }
  )
}

function Read-JsonFile {
  param([Parameter(Mandatory = $true)][string]$Path)
  return Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json
}

function ConvertTo-CanonicalJson {
  param([Parameter(Mandatory = $true)][object]$Value)
  return (($Value | ConvertTo-Json -Depth 100) + "`n")
}

function New-ManualReviewDebtIndex {
  $exportRoot = Join-Path $repoRoot 'data/exports'
  if (-not (Test-Path -LiteralPath $exportRoot -PathType Container)) {
    throw 'Missing data/exports'
  }

  $datasetEntries = @()
  $reasonTotals = @{}
  $manifestWithheldTotal = 0
  $manualReviewRowTotal = 0
  $manualReviewFileCount = 0
  $mismatchCount = 0

  $characterDirs = @(
    Get-ChildItem -LiteralPath $exportRoot -Directory |
      Where-Object { $_.Name -ne '_index' } |
      Sort-Object Name
  )

  foreach ($characterDir in $characterDirs) {
    $characterSlug = $characterDir.Name
    $manifestPath = Join-Path $characterDir.FullName 'snapshot_manifest.json'
    if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
      throw "Missing snapshot manifest for $characterSlug"
    }

    $manifest = Read-JsonFile $manifestPath
    foreach ($dataset in $datasets) {
      if (-not (Test-Property $manifest.datasets $dataset)) {
        throw "Missing dataset in snapshot manifest: $characterSlug/$dataset"
      }

      $datasetInfo = $manifest.datasets.$dataset
      $manualReviewPath = Join-Path $characterDir.FullName "${dataset}_manual_review.json"
      if (-not (Test-Path -LiteralPath $manualReviewPath -PathType Leaf)) {
        throw "Missing manual-review sidecar for $characterSlug/$dataset"
      }

      $rows = @(Read-JsonFile $manualReviewPath)
      $manualReviewFileCount += 1
      $manualReviewRowCount = $rows.Count
      $manualReviewRowTotal += $manualReviewRowCount
      $manifestWithheldTotal += [int]$datasetInfo.withheld_review_count

      $reasonCounts = @{}
      $confirmationCounts = @{}
      $publishEligibleCounts = [ordered]@{
        true_count = 0
        false_count = 0
        null_count = 0
      }

      foreach ($row in $rows) {
        foreach ($reason in @($row.reason_codes)) {
          Add-Count $reasonCounts ([string]$reason)
          Add-Count $reasonTotals ([string]$reason)
        }

        if ((Test-Property $row 'publish_eligible') -and $null -ne $row.publish_eligible) {
          if ($row.publish_eligible -eq $true) {
            $publishEligibleCounts.true_count += 1
          } elseif ($row.publish_eligible -eq $false) {
            $publishEligibleCounts.false_count += 1
          } else {
            throw "Unexpected publish_eligible value in $characterSlug/$dataset"
          }
        } else {
          $publishEligibleCounts.null_count += 1
        }

        if ((Test-Property $row 'confirmation_status') -and $null -ne $row.confirmation_status) {
          Add-Count $confirmationCounts ([string]$row.confirmation_status)
        }
      }

      $matchesManifest = ($manualReviewRowCount -eq [int]$datasetInfo.withheld_review_count)
      if (-not $matchesManifest) {
        $mismatchCount += 1
      }

      $datasetEntries += [ordered]@{
        character_slug = $characterSlug
        dataset = $dataset
        publication_state = [string]$datasetInfo.publication_state
        published_record_count = [int]$datasetInfo.published_record_count
        manifest_withheld_review_count = [int]$datasetInfo.withheld_review_count
        manual_review_row_count = [int]$manualReviewRowCount
        manual_review_count_matches_manifest = [bool]$matchesManifest
        snapshot_manifest_path = ConvertTo-RelativePath $manifestPath
        manual_review_path = ConvertTo-RelativePath $manualReviewPath
        published_run_id = $datasetInfo.published_run_id
        published_snapshot_ids = @($datasetInfo.published_snapshot_ids)
        reason_code_counts = @(ConvertTo-CountEntries $reasonCounts)
        publish_eligible_counts = $publishEligibleCounts
        confirmation_status_counts = @(ConvertTo-CountEntries $confirmationCounts)
      }
    }
  }

  return [ordered]@{
    schema_version = 'manual-review-debt-index/v1'
    generated = $true
    generator = 'tests/validation/validate-manual-review-debt-index.ps1 -Update'
    last_generated = '2026-05-18'
    tracking_issue = '#256'
    source_paths = @(
      'data/exports/*/snapshot_manifest.json',
      'data/exports/*/*_manual_review.json'
    )
    not_current_fact_authority = $true
    normal_public_answer_authority = $false
    summary = [ordered]@{
      character_count = [int]$characterDirs.Count
      dataset_count = [int]$datasetEntries.Count
      manual_review_file_count = [int]$manualReviewFileCount
      manual_review_row_count = [int]$manualReviewRowTotal
      manifest_withheld_review_count = [int]$manifestWithheldTotal
      withheld_count_mismatch_count = [int]$mismatchCount
    }
    reason_code_totals = @(ConvertTo-CountEntries $reasonTotals)
    datasets = @($datasetEntries)
  }
}

$expected = New-ManualReviewDebtIndex
$expectedJson = ConvertTo-CanonicalJson $expected

if ($Update) {
  $indexDirectory = Split-Path -Parent $indexPath
  if (-not (Test-Path -LiteralPath $indexDirectory -PathType Container)) {
    New-Item -ItemType Directory -Path $indexDirectory | Out-Null
  }
  Set-Content -LiteralPath $indexPath -Value $expectedJson -Encoding UTF8 -NoNewline
  Write-Host "Manual-review debt index updated: $indexRelativePath"
  return
}

if (-not (Test-Path -LiteralPath $indexPath -PathType Leaf)) {
  throw "Missing manual-review debt index: $indexRelativePath"
}

$actualJson = Get-Content -LiteralPath $indexPath -Raw -Encoding UTF8
if ($actualJson -ne $expectedJson) {
  throw "Manual-review debt index is stale. Regenerate with: pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-manual-review-debt-index.ps1 -Update"
}

if ($expected.summary.withheld_count_mismatch_count -ne 0) {
  throw 'Manual-review debt index found withheld row count mismatches'
}

Write-Host 'Manual-review debt index OK'
