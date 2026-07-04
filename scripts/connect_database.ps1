# Real PostgreSQL database connect karein (Supabase / Vercel Postgres)
#
# Usage:
#   .\scripts\connect_database.ps1
#
# Ya manually:
#   Copy .env.example to .env, DATABASE_URL fill karein, phir:
#   python manage.py setup_production --username Kunalsingh86 --email you@email.com --demo

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectRoot

Write-Host ""
Write-Host "=== EduVerse - Real Database Setup ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: .env file
$envFile = Join-Path $ProjectRoot ".env"
if (-not (Test-Path $envFile)) {
    Copy-Item (Join-Path $ProjectRoot ".env.example") $envFile
    Write-Host "[1/4] .env file created from .env.example" -ForegroundColor Green
} else {
    Write-Host "[1/4] .env file already exists" -ForegroundColor Yellow
}

# Step 2: Ask for DATABASE_URL if empty
$envContent = Get-Content $envFile -Raw
if ($envContent -match 'DATABASE_URL=\s*$' -or $envContent -match 'DATABASE_URL=\r?\n') {
    Write-Host ""
    Write-Host "Supabase connection string chahiye:" -ForegroundColor White
    Write-Host "  supabase.com -> Project Settings -> Database -> URI (Session pooler)" -ForegroundColor Gray
    Write-Host ""
    $dbUrl = Read-Host "DATABASE_URL paste karein"
    if ($dbUrl) {
        $envContent = $envContent -replace 'DATABASE_URL=.*', "DATABASE_URL=$dbUrl"
        Set-Content $envFile $envContent -NoNewline
        Write-Host "[2/4] DATABASE_URL saved to .env" -ForegroundColor Green
    } else {
        Write-Host "[2/4] DATABASE_URL empty — Supabase se string le kar .env mein daalein" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[2/4] DATABASE_URL already set in .env" -ForegroundColor Green
}

# Step 3: Ask for admin password if needed
if ($envContent -notmatch 'ADMIN_PASSWORD=.+') {
    $pass = Read-Host "ADMIN_PASSWORD (login password) enter karein" -AsSecureString
    $passPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($pass)
    )
    Add-Content $envFile "ADMIN_PASSWORD=$passPlain"
    Write-Host "[3/4] ADMIN_PASSWORD saved" -ForegroundColor Green
} else {
    Write-Host "[3/4] ADMIN_PASSWORD already set" -ForegroundColor Green
}

# Step 4: Run Django setup
Write-Host ""
Write-Host "[4/4] Database connect ho raha hai..." -ForegroundColor Cyan

# Load .env into current session
Get-Content $envFile | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
        [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), 'Process')
    }
}

python manage.py check_database
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$username = $env:ADMIN_USERNAME
if (-not $username) { $username = "Kunalsingh86" }
$email = $env:ADMIN_EMAIL
if (-not $email) { $email = "kunalsinghk2003@gmail.com" }

python manage.py setup_production --username $username --email $email --demo

Write-Host ""
Write-Host "=== Local setup complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Ab Vercel par bhi same variables add karein:" -ForegroundColor Yellow
Write-Host "  vercel.com -> Your Project -> Settings -> Environment Variables" -ForegroundColor Gray
Write-Host ""
Write-Host "  DATABASE_URL     = (same Supabase string)" -ForegroundColor White
Write-Host "  ADMIN_USERNAME   = $username" -ForegroundColor White
Write-Host "  ADMIN_PASSWORD   = (your password)" -ForegroundColor White
Write-Host "  ADMIN_EMAIL      = $email" -ForegroundColor White
Write-Host "  SECRET_KEY       = (random long string)" -ForegroundColor White
Write-Host "  DEBUG            = False" -ForegroundColor White
Write-Host ""
Write-Host "Phir Deployments -> Redeploy karein. Demo mode hat jayega." -ForegroundColor Cyan
Write-Host ""
