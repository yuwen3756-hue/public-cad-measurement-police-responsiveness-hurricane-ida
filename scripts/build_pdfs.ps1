param(
    [string]$Python = "python",
    [string]$PdfLaTeX = "pdflatex",
    [string]$BibTeX = "bibtex",
    [switch]$RunRawSourceAudit
)

$ErrorActionPreference = "Stop"
$packageRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$sourceDir = Join-Path $packageRoot "source"
$paperDir = Join-Path $packageRoot "paper"
New-Item -ItemType Directory -Path $paperDir -Force | Out-Null

function Invoke-Checked {
    param([string]$Program, [string[]]$Arguments)
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Program failed with exit code $LASTEXITCODE"
    }
}

function Build-LaTeXDocument {
    param([string]$Stem)
    Invoke-Checked $PdfLaTeX @("-interaction=nonstopmode", "-halt-on-error", "$Stem.tex")
    $sourceText = Get-Content -LiteralPath "$Stem.tex" -Raw
    if ($sourceText -match "\\bibliography\{") {
        Invoke-Checked $BibTeX @($Stem)
    }
    Invoke-Checked $PdfLaTeX @("-interaction=nonstopmode", "-halt-on-error", "$Stem.tex")
    Invoke-Checked $PdfLaTeX @("-interaction=nonstopmode", "-halt-on-error", "$Stem.tex")
    Invoke-Checked $PdfLaTeX @("-interaction=nonstopmode", "-halt-on-error", "$Stem.tex")
}

function Assert-CleanLaTeXLog {
    param([string]$Stem)
    $patterns = @(
        "LaTeX Warning:.*undefined",
        "Citation .* undefined",
        "Reference .* undefined",
        "There were undefined references",
        "Overfull \\hbox",
        "Overfull \\vbox"
    )
    $findings = Select-String -LiteralPath "$Stem.log" -Pattern $patterns
    if ($findings) {
        throw "LaTeX validation failed for ${Stem}: $($findings.Line -join '; ')"
    }
    if (Test-Path -LiteralPath "$Stem.blg") {
        $bibWarnings = Select-String -LiteralPath "$Stem.blg" -Pattern "Warning--"
        if ($bibWarnings) {
            throw "BibTeX validation failed for ${Stem}: $($bibWarnings.Line -join '; ')"
        }
    }
}

Invoke-Checked $Python @((Join-Path $PSScriptRoot "build_r15_evidence.py"))
if ($RunRawSourceAudit) {
    Invoke-Checked $Python @((Join-Path $PSScriptRoot "audit_public_source_lineage.py"))
}
Invoke-Checked $Python @((Join-Path $PSScriptRoot "build_r15_1_refinements.py"))

$stems = @(
    "main_paper_r16_0",
    "empirical_supplement_r16_0",
    "research_status_note_r16_0",
    "legacy_technical_archive_r16_0"
)
Push-Location $sourceDir
try {
    foreach ($stem in $stems) {
        Build-LaTeXDocument $stem
        Assert-CleanLaTeXLog $stem
    }
} finally {
    Pop-Location
}

$mainOut = Join-Path $paperDir "Public_CAD_Main_2026-08-25_R16_0.pdf"
$suppOut = Join-Path $paperDir "Public_CAD_Empirical_Supplement_2026-08-25_R16_0.pdf"
$statusOut = Join-Path $paperDir "Public_CAD_Research_Status_Note_2026-08-25_R16_0.pdf"
$legacyOut = Join-Path $paperDir "Public_CAD_Legacy_Technical_Archive_2026-08-25_R16_0.pdf"
$combinedOut = Join-Path $paperDir "Public_CAD_2026-08-25_R16_0.pdf"

Copy-Item -LiteralPath (Join-Path $sourceDir "main_paper_r16_0.pdf") -Destination $mainOut -Force
Copy-Item -LiteralPath (Join-Path $sourceDir "empirical_supplement_r16_0.pdf") -Destination $suppOut -Force
Copy-Item -LiteralPath (Join-Path $sourceDir "research_status_note_r16_0.pdf") -Destination $statusOut -Force
Copy-Item -LiteralPath (Join-Path $sourceDir "legacy_technical_archive_r16_0.pdf") -Destination $legacyOut -Force
Invoke-Checked $Python @((Join-Path $PSScriptRoot "combine_pdfs.py"), $mainOut, $suppOut, $combinedOut)

foreach ($stem in $stems) {
    foreach ($extension in @("aux", "bbl", "blg", "log", "out", "toc", "pdf")) {
        $artifact = Join-Path $sourceDir "$stem.$extension"
        if (Test-Path -LiteralPath $artifact) {
            Remove-Item -LiteralPath $artifact -Force
        }
    }
}

Write-Output "PDF_BUILD_PASS"
