Write-Host "🐅 COMPLETE DATABASE FIX SCRIPT" -ForegroundColor Magenta

cd C:\Users\User\Downloads\wrath

Write-Host "1. Removing old database..." -ForegroundColor Yellow
Remove-Item -Path "golden_tiger.db" -ErrorAction SilentlyContinue
Remove-Item -Path "backend\golden_tiger.db" -ErrorAction SilentlyContinue

Write-Host "2. Updating models with better error handling..." -ForegroundColor Yellow

# Create the updated models.py (use the code above)

Write-Host "3. Starting premium backend..." -ForegroundColor Green
.\venv\Scripts\Activate
python backend\app.py