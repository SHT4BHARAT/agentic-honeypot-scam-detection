# PowerShell Test Script for Agentic Honey-Pot API
# This script tests the API with proper JSON escaping for PowerShell

Write-Host "🧪 Testing Agentic Honey-Pot API" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "Test 1: Health Check" -ForegroundColor Yellow
$response = Invoke-RestMethod -Uri "http://localhost:8000/" -Method Get
$response | ConvertTo-Json
Write-Host "✅ Health check passed!" -ForegroundColor Green
Write-Host ""

# Test 2: Bank Account Scam
Write-Host "Test 2: Bank Account Scam" -ForegroundColor Yellow
$body = @{
    sessionId = "test-bank-001"
    message = @{
        sender = "scammer"
        text = "Your bank account will be blocked. Verify immediately at http://fake-bank.com"
        timestamp = 1738637561000
    }
    conversationHistory = @()
    metadata = @{
        channel = "SMS"
        language = "English"
        locale = "IN"
    }
} | ConvertTo-Json -Depth 10

$headers = @{
    "Content-Type" = "application/json"
    "x-api-key" = "your_secret_api_key_here"
}

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/honeypot" -Method Post -Body $body -Headers $headers
    Write-Host "Response:" -ForegroundColor Green
    $response | ConvertTo-Json
    Write-Host ""
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}

# Test 3: UPI Scam
Write-Host "Test 3: UPI Scam" -ForegroundColor Yellow
$body = @{
    sessionId = "test-upi-002"
    message = @{
        sender = "scammer"
        text = "Send refund to scammer@paytm immediately for your order"
        timestamp = 1738637561000
    }
    conversationHistory = @()
    metadata = @{
        channel = "WhatsApp"
        language = "English"
        locale = "IN"
    }
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/honeypot" -Method Post -Body $body -Headers $headers
    Write-Host "Response:" -ForegroundColor Green
    $response | ConvertTo-Json
    Write-Host ""
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}

# Test 4: Prize Scam
Write-Host "Test 4: Prize/Lottery Scam" -ForegroundColor Yellow
$body = @{
    sessionId = "test-prize-003"
    message = @{
        sender = "scammer"
        text = "Congratulations! You won 10 lakh rupees. Call 9876543210 to claim your prize"
        timestamp = 1738637561000
    }
    conversationHistory = @()
    metadata = @{
        channel = "SMS"
        language = "English"
        locale = "IN"
    }
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/honeypot" -Method Post -Body $body -Headers $headers
    Write-Host "Response:" -ForegroundColor Green
    $response | ConvertTo-Json
    Write-Host ""
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}

Write-Host "🎉 Testing complete!" -ForegroundColor Cyan
