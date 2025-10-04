# Windows Development Environment Setup Script
# For installing all tools mentioned in the marks reader project

Write-Host "=== Windows Development Environment Setup ===" -ForegroundColor Cyan
Write-Host "This script will install the following programs:" -ForegroundColor Yellow
Write-Host "  1. Git for Windows (version control)" -ForegroundColor White
Write-Host "  2. Node.js LTS (JavaScript runtime)" -ForegroundColor White
Write-Host "  3. Python 3 (if not already installed)" -ForegroundColor White
Write-Host "  4. Claude Code CLI (AI coding assistant)" -ForegroundColor White
Write-Host "  5. GitHub CLI (gh command)" -ForegroundColor White
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "WARNING: Not running as Administrator. Some installations may fail." -ForegroundColor Red
    Write-Host "Press Ctrl+C to cancel and re-run as Admin, or any other key to continue..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Set execution policy for current user
Write-Host "`nSetting PowerShell execution policy..." -ForegroundColor Cyan
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force

# 1. Install Git for Windows
Write-Host "`n[1/5] Installing Git for Windows..." -ForegroundColor Cyan
try {
    winget install --id Git.Git -e --source winget --silent
    Write-Host "  Git installed successfully" -ForegroundColor Green
} catch {
    Write-Host "  Git installation failed: $_" -ForegroundColor Red
}

# 2. Install Node.js LTS
Write-Host "`n[2/5] Installing Node.js LTS..." -ForegroundColor Cyan
try {
    winget install OpenJS.NodeJS.LTS --silent
    Write-Host "  Node.js installed successfully" -ForegroundColor Green
} catch {
    Write-Host "  Node.js installation failed: $_" -ForegroundColor Red
}

# 3. Check Python (usually pre-installed on Windows 10/11)
Write-Host "`n[3/5] Checking Python installation..." -ForegroundColor Cyan
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "  Python already installed: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  Python not found. Installing..." -ForegroundColor Yellow
    try {
        winget install Python.Python.3.12 --silent
        Write-Host "  Python installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "  Python installation failed: $_" -ForegroundColor Red
    }
}

# 4. Install GitHub CLI
Write-Host "`n[4/5] Installing GitHub CLI..." -ForegroundColor Cyan
try {
    winget install --id GitHub.cli --silent
    Write-Host "  GitHub CLI installed successfully" -ForegroundColor Green
} catch {
    Write-Host "  GitHub CLI installation failed: $_" -ForegroundColor Red
}

# Refresh PATH for this session
Write-Host "`nRefreshing environment variables..." -ForegroundColor Cyan
$env:PATH = [System.Environment]::GetEnvironmentVariable("Path","User") + ";" + [System.Environment]::GetEnvironmentVariable("Path","Machine")

# 5. Install Claude Code CLI via npm (requires Node.js)
Write-Host "`n[5/5] Installing Claude Code CLI..." -ForegroundColor Cyan
Write-Host "  Waiting for Node.js to be available..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

try {
    # Refresh PATH again to pick up npm
    $env:PATH = [System.Environment]::GetEnvironmentVariable("Path","User") + ";" + [System.Environment]::GetEnvironmentVariable("Path","Machine")

    npm install -g @anthropic-ai/claude-code
    Write-Host "  Claude Code CLI installed successfully" -ForegroundColor Green
} catch {
    Write-Host "  Claude Code CLI installation failed: $_" -ForegroundColor Red
    Write-Host "  You may need to restart PowerShell and run: npm install -g @anthropic-ai/claude-code" -ForegroundColor Yellow
}

# Add necessary paths to user PATH
Write-Host "`nConfiguring PATH environment variables..." -ForegroundColor Cyan
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
$pathsToAdd = @(
    "C:\Program Files\Git\cmd",
    "$env:USERPROFILE\AppData\Roaming\npm",
    "$env:USERPROFILE\.local\bin"
)

foreach ($pathToAdd in $pathsToAdd) {
    if ($currentPath -notlike "*$pathToAdd*") {
        Write-Host "  Adding to PATH: $pathToAdd" -ForegroundColor Yellow
        $currentPath += ";$pathToAdd"
    }
}
[Environment]::SetEnvironmentVariable("Path", $currentPath, "User")

# Set Claude Code Git Bash path
Write-Host "`nConfiguring Claude Code environment variables..." -ForegroundColor Cyan
[Environment]::SetEnvironmentVariable("CLAUDE_CODE_GIT_BASH_PATH", "C:\Program Files\Git\bin\bash.exe", "User")
Write-Host "  CLAUDE_CODE_GIT_BASH_PATH set" -ForegroundColor Green

# Install Python packages for marks_reader
Write-Host "`nInstalling Python packages..." -ForegroundColor Cyan
try {
    python -m pip install --upgrade pip
    python -m pip install openpyxl
    Write-Host "  Python packages installed successfully" -ForegroundColor Green
} catch {
    Write-Host "  Python package installation failed: $_" -ForegroundColor Red
}

# Summary
Write-Host "`n=== Installation Summary ===" -ForegroundColor Cyan
Write-Host "Programs installed (verify with commands below):" -ForegroundColor Yellow
Write-Host "  git --version" -ForegroundColor White
Write-Host "  node --version" -ForegroundColor White
Write-Host "  npm --version" -ForegroundColor White
Write-Host "  python --version" -ForegroundColor White
Write-Host "  gh --version" -ForegroundColor White
Write-Host "  claude doctor" -ForegroundColor White

Write-Host "`nNEXT STEPS:" -ForegroundColor Cyan
Write-Host "1. RESTART PowerShell (or restart your computer)" -ForegroundColor Yellow
Write-Host "2. Verify installations by running the commands above" -ForegroundColor Yellow
Write-Host "3. Configure Claude Code CLI:" -ForegroundColor Yellow
Write-Host "     claude config" -ForegroundColor White
Write-Host "4. Configure Git:" -ForegroundColor Yellow
Write-Host "     git config --global user.name ""Your Name""" -ForegroundColor White
Write-Host "     git config --global user.email ""your.email@example.com""" -ForegroundColor White
Write-Host "5. Login to GitHub CLI:" -ForegroundColor Yellow
Write-Host "     gh auth login" -ForegroundColor White

Write-Host "`nSetup script complete!" -ForegroundColor Green
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
