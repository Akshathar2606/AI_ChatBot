# Manual API Test Script for Backend

Write-Host "======================================"
Write-Host "Backend API Manual Tests"
Write-Host "======================================"
Write-Host ""

# Test 1: Health Check
Write-Host "Test 1: Health Check (GET /api/health)"
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method GET
    Write-Host "[PASSED] Response: $($response | ConvertTo-Json)"
} catch {
    Write-Host "[FAILED] Error: $($_.Exception.Message)"
}
Write-Host ""

# Test 2: Missing sessionId
Write-Host "Test 2: POST /api/chat with missing sessionId (should fail with 400)"
try {
    $body = @{ message = "I want to return my shoes" } | ConvertTo-Json
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/chat" -Method POST -ContentType "application/json" -Body $body
    Write-Host "[FAILED] Should have returned 400 error"
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    if ($statusCode -eq 400) {
        Write-Host "[PASSED] Correctly returned 400"
    } else {
        Write-Host "[FAILED] Expected 400, got $statusCode"
    }
}
Write-Host ""

# Test 3: Missing message
Write-Host "Test 3: POST /api/chat with missing message (should fail with 400)"
try {
    $body = @{ sessionId = "test-session-123" } | ConvertTo-Json
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/chat" -Method POST -ContentType "application/json" -Body $body
    Write-Host "[FAILED] Should have returned 400 error"
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    if ($statusCode -eq 400) {
        Write-Host "[PASSED] Correctly returned 400"
    } else {
        Write-Host "[FAILED] Expected 400, got $statusCode"
    }
}
Write-Host ""

# Test 4: Empty sessionId
Write-Host "Test 4: POST /api/chat with empty sessionId (should fail with 400)"
try {
    $body = @{ sessionId = ""; message = "test" } | ConvertTo-Json
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/chat" -Method POST -ContentType "application/json" -Body $body
    Write-Host "[FAILED] Should have returned 400 error"
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    if ($statusCode -eq 400) {
        Write-Host "[PASSED] Correctly returned 400"
    } else {
        Write-Host "[FAILED] Expected 400, got $statusCode"
    }
}
Write-Host ""

# Test 5: Valid request (will fail - AI service not available)
Write-Host "Test 5: POST /api/chat with valid data (expected to fail - Python AI service not running)"
try {
    $body = @{ sessionId = "test-session-456"; message = "I want to return my shoes" } | ConvertTo-Json
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/chat" -Method POST -ContentType "application/json" -Body $body
    Write-Host "[UNEXPECTED] Should have failed without Python service"
    Write-Host "Response: $($response | ConvertTo-Json)"
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    if ($statusCode -eq 502) {
        Write-Host "[PASSED] Correctly returned 502 (AI service unavailable)"
    } else {
        Write-Host "[INFO] Got status $statusCode (expected 502 without AI service)"
    }
}
Write-Host ""

Write-Host "======================================"
Write-Host "Test Summary:"
Write-Host "- Tests 1-4 verify input validation"
Write-Host "- Test 5 requires Python AI service on port 8000"
Write-Host "- With MongoDB running, conversations will be saved"
Write-Host "======================================"
