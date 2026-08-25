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
    $log = "$Stem.log"
    $findings = Select-String -LiteralPath $log -Pattern $patterns
    if ($findings) {
        throw "LaTeX validation failed for ${Stem}: $($findings.Line -join '; ')"
    }
    $blg = "$Stem.blg"
    $bibWarnings = Select-String -LiteralPath $blg -Pattern "Warning--"
    if ($bibWarnings) {
        throw "BibTeX validation failed for ${Stem}: $($bibWarnings.Line -join '; ')"
    }
}

Push-Location $sourceDir
try {
    Invoke-Checked $Python @((Join-Path $PSScriptRoot "build_r14_evidence.py"))
    Build-LaTeXDocument "main_paper_r14_0"
    Build-LaTeXDocument "math_appendix_r14_0"
    Assert-CleanLaTeXLog "main_paper_r14_0"
    Assert-CleanLaTeXLog "math_appendix_r14_0"
} finally {
    Pop-Location
}

$mainOut = Join-Path $paperDir "Beland_Current_Status_Main_2026-08-24_R14_0.pdf"
$appendixOut = Join-Path $paperDir "Beland_Current_Status_Appendix_2026-08-24_R14_0.pdf"
$combinedOut = Join-Path $paperDir "Beland_Current_Status_2026-08-24_R14_0.pdf"
Copy-Item -LiteralPath (Join-Path $sourceDir "main_paper_r14_0.pdf") -Destination $mainOut -Force
Copy-Item -LiteralPath (Join-Path $sourceDir "math_appendix_r14_0.pdf") -Destination $appendixOut -Force
Invoke-Checked $Python @((Join-Path $PSScriptRoot "combine_pdfs.py"), $mainOut, $appendixOut, $combinedOut)

foreach ($stem in @("main_paper_r14_0", "math_appendix_r14_0")) {
    foreach ($extension in @("aux", "bbl", "blg", "log", "out", "toc", "pdf")) {
        $artifact = Join-Path $sourceDir "$stem.$extension"
        if (Test-Path -LiteralPath $artifact) {
            Remove-Item -LiteralPath $artifact -Force
        }
    }
}

Write-Output "PDF_BUILD_PASS"
