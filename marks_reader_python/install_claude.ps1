# Claude Code CLI Installation Script
# Installs Claude Code CLI and all prerequisites on Windows

Write-Host "=== Claude Code CLI Installation ===" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "WARNING: Not running as Administrator. Installations may fail." -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press Ctrl+C to cancel and restart as Admin, or any key to continue..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Step 1: Set Execution Policy
Write-Host "[Step 1/5] Setting PowerShell execution policy..." -ForegroundColor Cyan
try {
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
    Write-Host "  Execution policy set to RemoteSigned" -ForegroundColor Green
} catch {
    Write-Host "  Failed to set execution policy: $_" -ForegroundColor Red
    exit 1
}

# Step 2: Install Git for Windows
Write-Host "`n[Step 2/5] Installing Git for Windows..." -ForegroundColor Cyan
Write-Host "  Checking if Git is already installed..." -ForegroundColor Yellow

$gitInstalled = $false
try {
    $gitVersion = & git --version 2>&1
    Write-Host "  Git already installed: $gitVersion" -ForegroundColor Green
    $gitInstalled = $true
} catch {
    Write-Host "  Git not found. Installing..." -ForegroundColor Yellow
    try {
        winget install --id Git.Git -e --source winget --accept-source-agreements --accept-package-agreements
        Write-Host "  Git installed successfully" -ForegroundColor Green
        $gitInstalled = $true
    } catch {
        Write-Host "  Git installation failed: $_" -ForegroundColor Red
        Write-Host "  Please install Git manually from: https://git-scm.com/downloads/win" -ForegroundColor Yellow
    }
}

# Step 3: Install Node.js
Write-Host "`n[Step 3/5] Installing Node.js LTS..." -ForegroundColor Cyan
Write-Host "  Checking if Node.js is already installed..." -ForegroundColor Yellow

$nodeInstalled = $false
try {
    $nodeVersion = & node --version 2>&1
    $npmVersion = & npm --version 2>&1
    Write-Host "  Node.js already installed: $nodeVersion" -ForegroundColor Green
    Write-Host "  npm version: $npmVersion" -ForegroundColor Green
    $nodeInstalled = $true
} catch {
    Write-Host "  Node.js not found. Installing..." -ForegroundColor Yellow
    try {
        winget install OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements
        Write-Host "  Node.js installed successfully" -ForegroundColor Green
        $nodeInstalled = $true

        # Refresh PATH to pick up Node.js
        Write-Host "  Refreshing environment..." -ForegroundColor Yellow
        $env:PATH = [System.Environment]::GetEnvironmentVariable("Path","User") + ";" + [System.Environment]::GetEnvironmentVariable("Path","Machine")
        Start-Sleep -Seconds 3
    } catch {
        Write-Host "  Node.js installation failed: $_" -ForegroundColor Red
        Write-Host "  Please install Node.js manually from: https://nodejs.org" -ForegroundColor Yellow
    }
}

# Verify prerequisites are installed
if (-not $gitInstalled -or -not $nodeInstalled) {
    Write-Host "`nPrerequisites not met. Please install missing components and run this script again." -ForegroundColor Red
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Step 4: Install Claude Code CLI via npm
Write-Host "`n[Step 4/5] Installing Claude Code CLI..." -ForegroundColor Cyan

# Refresh PATH again
$env:PATH = [System.Environment]::GetEnvironmentVariable("Path","User") + ";" + [System.Environment]::GetEnvironmentVariable("Path","Machine")

try {
    Write-Host "  Running: npm install -g @anthropic-ai/claude-code" -ForegroundColor Yellow
    npm install -g @anthropic-ai/claude-code
    Write-Host "  Claude Code CLI installed successfully" -ForegroundColor Green
} catch {
    Write-Host "  Installation failed: $_" -ForegroundColor Red
    Write-Host "  Try running manually: npm install -g @anthropic-ai/claude-code" -ForegroundColor Yellow
}

# Step 5: Configure PATH and Environment Variables
Write-Host "`n[Step 5/5] Configuring environment variables..." -ForegroundColor Cyan

# Add paths
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
$pathsToAdd = @(
    "C:\Program Files\Git\cmd",
    "C:\Program Files\Git\bin",
    "$env:USERPROFILE\AppData\Roaming\npm"
)

$pathUpdated = $false
foreach ($pathToAdd in $pathsToAdd) {
    if ($currentPath -notlike "*$pathToAdd*") {
        Write-Host "  Adding to PATH: $pathToAdd" -ForegroundColor Yellow
        $currentPath += ";$pathToAdd"
        $pathUpdated = $true
    }
}

if ($pathUpdated) {
    [Environment]::SetEnvironmentVariable("Path", $currentPath, "User")
    Write-Host "  PATH updated" -ForegroundColor Green
} else {
    Write-Host "  PATH already configured" -ForegroundColor Green
}

# Set Git Bash path for Claude
Write-Host "  Setting CLAUDE_CODE_GIT_BASH_PATH..." -ForegroundColor Yellow
[Environment]::SetEnvironmentVariable("CLAUDE_CODE_GIT_BASH_PATH", "C:\Program Files\Git\bin\bash.exe", "User")
Write-Host "  CLAUDE_CODE_GIT_BASH_PATH set" -ForegroundColor Green

# Refresh PATH for current session
$env:PATH = [System.Environment]::GetEnvironmentVariable("Path","User") + ";" + [System.Environment]::GetEnvironmentVariable("Path","Machine")

# Verification
Write-Host "`n=== Installation Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Verifying installations..." -ForegroundColor Yellow

# Test Git
try {
    $gitVer = & git --version 2>&1
    Write-Host "  Git: $gitVer" -ForegroundColor Green
} catch {
    Write-Host "  Git: NOT FOUND (restart PowerShell)" -ForegroundColor Red
}

# Test Node
try {
    $nodeVer = & node --version 2>&1
    $npmVer = & npm --version 2>&1
    Write-Host "  Node.js: $nodeVer" -ForegroundColor Green
    Write-Host "  npm: $npmVer" -ForegroundColor Green
} catch {
    Write-Host "  Node.js/npm: NOT FOUND (restart PowerShell)" -ForegroundColor Red
}

# Test Claude
Write-Host ""
Write-Host "Testing Claude Code CLI..." -ForegroundColor Yellow
Write-Host "  (This may take a moment...)" -ForegroundColor Gray

try {
    # Try to find claude
    $claudePath = & where.exe claude 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Claude found at: $claudePath" -ForegroundColor Green

        # Run claude doctor
        Write-Host ""
        Write-Host "Running claude doctor..." -ForegroundColor Yellow
        & claude doctor
    } else {
        Write-Host "  Claude: NOT FOUND in PATH" -ForegroundColor Red
        Write-Host "  Restart PowerShell and try: claude doctor" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  Claude: NOT FOUND (restart PowerShell)" -ForegroundColor Red
}

# Next steps
Write-Host "`n=== NEXT STEPS ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. CLOSE and RESTART PowerShell" -ForegroundColor Yellow
Write-Host "   (This is required for PATH changes to take effect)" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Verify Claude installation:" -ForegroundColor Yellow
Write-Host "     claude doctor" -ForegroundColor White
Write-Host ""
Write-Host "3. Configure Claude with your API key:" -ForegroundColor Yellow
Write-Host "     claude config" -ForegroundColor White
Write-Host "   (Get API key from: https://console.anthropic.com)" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Start using Claude:" -ForegroundColor Yellow
Write-Host "     cd your-project-folder" -ForegroundColor White
Write-Host "     claude" -ForegroundColor White
Write-Host ""

Write-Host "Installation script finished!" -ForegroundColor Green
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
