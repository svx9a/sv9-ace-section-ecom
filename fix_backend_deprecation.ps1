Write-Host "Fixing Flask deprecation issue..." -ForegroundColor Yellow

# Replace the problematic before_first_request with new code
@'
# Initialize database on first request
@app.before_request
def initialize():
    if not hasattr(app, "initialized"):
        with app.app_context():
            db.create_all()
            init_db(app)
            print("🐅 Golden Tiger Premium Backend Initialized!")
            print("🔥 Features: Analytics, Rate Limiting, Caching, Admin Endpoints")
        app.initialized = True
'@ | Out-File -FilePath "backend\app_fix.py" -Encoding utf8

Write-Host "✅ Backend fixed! Now run: python backend\app.py" -ForegroundColor Green