# BeaverSec Installation Script for Windows

Write-Host "BeaverSec Installation" -ForegroundColor Green
Write-Host "======================" -ForegroundColor Green

# Check Python version
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Python 3.8+ is required but not found" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "Error: Python 3.8+ is required but not found" -ForegroundColor Red
    exit 1
}

# Parse Python version
$versionMatch = [regex]::Match($pythonVersion, "(\d+)\.(\d+)")
if ($versionMatch.Success) {
    $major = [int]$versionMatch.Groups[1].Value
    $minor = [int]$versionMatch.Groups[2].Value
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
        Write-Host "Error: Python 3.8+ required (found $pythonVersion)" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Error: Could not determine Python version" -ForegroundColor Red
    exit 1
}

Write-Host "Found $pythonVersion" -ForegroundColor Green

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Install development dependencies if requested
if ($args[0] -eq "--dev") {
    Write-Host "Installing development dependencies..." -ForegroundColor Yellow
    pip install -r requirements-dev.txt
}

# Install BeaverSec
Write-Host "Installing BeaverSec..." -ForegroundColor Yellow
pip install -e .

# Create configuration directory
$configDir = "$env:USERPROFILE\.beaversec"
New-Item -ItemType Directory -Force -Path $configDir | Out-Null
New-Item -ItemType Directory -Force -Path "$configDir\logs" | Out-Null
New-Item -ItemType Directory -Force -Path "$configDir\credentials" | Out-Null

# Create default configuration
if (-not (Test-Path "$configDir\config.yaml")) {
    Write-Host "Creating default configuration..." -ForegroundColor Yellow
    Copy-Item "beaversec\config\templates\config.yaml.template" "$configDir\config.yaml"
}

Write-Host ""
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To start using BeaverSec:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\Activate.ps1"
Write-Host "  beaversec --help"
Write-Host ""
Write-Host "Or run directly:" -ForegroundColor Cyan
Write-Host "  venv\Scripts\beaversec --help"