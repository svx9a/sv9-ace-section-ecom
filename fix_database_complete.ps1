Write-Host "Installing Flask dependencies..." -ForegroundColor Yellow

# Activate virtual environment
.\venv\Scripts\Activate

# Install all required packages
pip install flask==2.3.3 flask-cors==4.0.0 flask-sqlalchemy==3.0.5 python-dotenv==1.0.0

Write-Host "✅ Dependencies installed!" -ForegroundColor Green
Write-Host "Now run: python backend\app.py" -ForegroundColor Cyan