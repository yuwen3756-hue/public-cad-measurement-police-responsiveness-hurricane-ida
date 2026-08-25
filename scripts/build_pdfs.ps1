param(
    [string]$Python = "python",
    [string]$PdfLaTeX = "pdflatex",
    [string]$BibTeX = "bibtex"
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
    Invoke-Checked $BibTeX @($Stem)
    Invoke-Checked $PdfLaTeX @("-interaction=nonstopmode", "-halt-on-error", "$Stem.tex")
    Invoke-Checked $PdfLaTeX @("-interaction=nonstopmode", "-halt-on-error", "$Stem.tex")
    Invoke-Checked $PdfLaTeX @("-interaction=nonstopmode", "-halt-on-error", "$Stem.tex")
}

Push-Location $sourceDir
try {
    Build-LaTeXDocument "main_paper_r12_2"
    Build-LaTeXDocument "math_appendix_r12_2"
} finally {
    Pop-Location
}

$mainOut = Join-Path $paperDir "Beland_Current_Status_Main_2026-08-24_R12_2.pdf"
$appendixOut = Join-Path $paperDir "Beland_Current_Status_Appendix_2026-08-24_R12_2.pdf"
$combinedOut = Join-Path $paperDir "Beland_Current_Status_2026-08-24_R12_2.pdf"
Copy-Item -LiteralPath (Join-Path $sourceDir "main_paper_r12_2.pdf") -Destination $mainOut -Force
Copy-Item -LiteralPath (Join-Path $sourceDir "math_appendix_r12_2.pdf") -Destination $appendixOut -Force
Invoke-Checked $Python @((Join-Path $PSScriptRoot "combine_pdfs.py"), $mainOut, $appendixOut, $combinedOut)

foreach ($stem in @("main_paper_r12_2", "math_appendix_r12_2")) {
    foreach ($extension in @("aux", "bbl", "blg", "log", "out", "toc", "pdf")) {
        $artifact = Join-Path $sourceDir "$stem.$extension"
        if (Test-Path -LiteralPath $artifact) {
            Remove-Item -LiteralPath $artifact -Force
        }
    }
}

Write-Output "PDF_BUILD_PASS"
