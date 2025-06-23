Write-Host "Starting Aura Vision Assistant..." -ForegroundColor Green
Write-Host ""

# Step 1: Install frontend dependencies
Write-Host "Step 1: Installing frontend dependencies..." -ForegroundColor Yellow
Set-Location frontend
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error installing frontend dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 2: Build React app
Write-Host "Step 2: Building React app..." -ForegroundColor Yellow
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error building React app" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 3: Install backend dependencies
Write-Host "Step 3: Installing backend dependencies..." -ForegroundColor Yellow
Set-Location ../backend
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error installing backend dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 4: Start Python backend
Write-Host "Step 4: Starting Python AI backend..." -ForegroundColor Yellow
Set-Location ..
Start-Process powershell -ArgumentList "-NoExit", "-Command", "uvicorn main_voice_simple:app --reload --port 8001" -WindowStyle Normal

# Step 5: Start Node.js frontend
Write-Host "Step 5: Starting Node.js frontend server..." -ForegroundColor Yellow
Set-Location backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm start" -WindowStyle Normal

Write-Host ""
Write-Host "Aura Vision Assistant is starting..." -ForegroundColor Green
Write-Host ""
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Python API: http://localhost:8001" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to exit this script" 