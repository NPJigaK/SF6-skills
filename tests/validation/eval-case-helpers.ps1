Set-StrictMode -Version Latest

function ConvertFrom-EvalYamlScalar {
  param([Parameter(Mandatory = $true)][AllowEmptyString()][string]$Value)

  $trimmed = $Value.Trim()
  if ($trimmed.Length -ge 2) {
    $first = $trimmed.Substring(0, 1)
    $last = $trimmed.Substring($trimmed.Length - 1, 1)
    if (($first -eq '"' -and $last -eq '"') -or ($first -eq "'" -and $last -eq "'")) {
      return $trimmed.Substring(1, $trimmed.Length - 2).Replace('\"', '"').Replace("''", "'")
    }
  }
  return $trimmed
}

function ConvertTo-StringArray {
  param([AllowNull()][object]$Value)

  if ($null -eq $Value) {
    return @()
  }
  return @($Value | ForEach-Object { [string]$_ })
}

function Read-EvalQuestionFile {
  param(
    [Parameter(Mandatory = $true)][string]$RepoRoot,
    [Parameter(Mandatory = $true)][string]$RelativePath
  )

  $path = Join-Path $RepoRoot $RelativePath
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
    throw "Missing eval file: $RelativePath"
  }

  $content = Get-Content -LiteralPath $path -Raw -Encoding UTF8
  $normalized = $content -replace "`r`n", "`n"
  $lines = $normalized -split "`n"
  $cases = @()
  $issues = @()
  $currentCase = $null
  $currentListKey = $null
  $seenCasesRoot = $false

  for ($index = 0; $index -lt $lines.Count; $index++) {
    $line = $lines[$index]
    $lineNumber = $index + 1

    if ([string]::IsNullOrWhiteSpace($line)) {
      continue
    }

    if ($line -match '^cases:\s*$') {
      $seenCasesRoot = $true
      continue
    }

    if ($line -match '^([A-Za-z0-9_]+):') {
      $issues += "$RelativePath line $lineNumber has unsupported top-level eval key: $($Matches[1])"
      continue
    }

    if ($line -match '^  -\s+([A-Za-z0-9_]+):\s*(.*)$') {
      if ($null -ne $currentCase) {
        $cases += [pscustomobject]$currentCase
      }

      $currentCase = [ordered]@{
        source_file = $RelativePath
      }
      $key = $Matches[1]
      $currentCase[$key] = ConvertFrom-EvalYamlScalar $Matches[2]
      $currentListKey = $null
      continue
    }

    if ($line -match '^    ([A-Za-z0-9_]+):\s*(.*)$') {
      if ($null -eq $currentCase) {
        $issues += "$RelativePath line $lineNumber defines a case field before a case item"
        continue
      }

      $key = $Matches[1]
      $value = $Matches[2]
      if ([string]::IsNullOrWhiteSpace($value)) {
        $currentCase[$key] = @()
        $currentListKey = $key
      } else {
        $currentCase[$key] = ConvertFrom-EvalYamlScalar $value
        $currentListKey = $null
      }
      continue
    }

    if ($line -match '^      -\s*(.*)$') {
      if ($null -eq $currentCase -or [string]::IsNullOrWhiteSpace($currentListKey)) {
        $issues += "$RelativePath line $lineNumber has a list item outside a list field"
        continue
      }
      $currentCase[$currentListKey] = @(ConvertTo-StringArray $currentCase[$currentListKey]) + @(ConvertFrom-EvalYamlScalar $Matches[1])
      continue
    }

    $issues += "$RelativePath line $lineNumber has unsupported YAML shape"
  }

  if ($null -ne $currentCase) {
    $cases += [pscustomobject]$currentCase
  }

  if (-not $seenCasesRoot) {
    $issues += "$RelativePath missing top-level cases key"
  }
  if ($cases.Count -eq 0) {
    $issues += "$RelativePath contains no eval cases"
  }

  return [pscustomobject]@{
    RelativePath = $RelativePath
    Cases = $cases
    Issues = $issues
  }
}

function Get-EvalQuestionFiles {
  param([Parameter(Mandatory = $true)][string]$RepoRoot)

  $questionRoot = Join-Path $RepoRoot 'evals/questions'
  if (-not (Test-Path -LiteralPath $questionRoot -PathType Container)) {
    throw 'Missing eval question directory: evals/questions'
  }

  return @(
    Get-ChildItem -LiteralPath $questionRoot -File -Filter '*.yaml' |
      Sort-Object FullName |
      ForEach-Object { $_.FullName.Substring($RepoRoot.Length + 1).Replace('\', '/') }
  )
}

function Get-EvalCaseIndex {
  param(
    [Parameter(Mandatory = $true)][string]$RepoRoot,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  $index = @{}
  foreach ($relativePath in @(Get-EvalQuestionFiles $RepoRoot)) {
    $parsed = Read-EvalQuestionFile -RepoRoot $RepoRoot -RelativePath $relativePath
    foreach ($issue in @($parsed.Issues)) {
      $Issues.Value += $issue
    }

    foreach ($case in @($parsed.Cases)) {
      $caseId = if ($null -ne $case.PSObject.Properties['id']) { [string]$case.id } else { '' }
      if ([string]::IsNullOrWhiteSpace($caseId)) {
        $Issues.Value += "$relativePath contains an eval case with an empty id"
        continue
      }
      if ($index.ContainsKey($caseId)) {
        $Issues.Value += "Duplicate eval case id: $caseId ($($index[$caseId].source_file), $relativePath)"
      } else {
        $index[$caseId] = $case
      }
    }
  }

  return $index
}
