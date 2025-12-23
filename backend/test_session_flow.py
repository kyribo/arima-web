import requests
from app.core.config import settings

BASE_URL = "http://localhost:8000/api/v1"
USERNAME = "admin@arima.com" # Default seeder
PASSWORD = "Admin123!"

def test_session_flow():
    # 1. Login
    print(f"Logging in as {USERNAME}...")
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    res = requests.post(f"{BASE_URL}/auth/login", data=login_data, headers=headers)
    
    if res.status_code != 200:
        print(f"Login failed: {res.text}")
        return

    data = res.json()
    token = data["access_token"]
    refresh = data.get("refresh_token")
    print(f"Login successful. Token: {token[:15]}... Refresh: {refresh[:15]}...")
    
    # 2. Get Sessions
    print("\nFetching active sessions...")
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/sessions/", headers=headers)
    
    if res.status_code != 200:
        print(f"Fetch sessions failed: {res.text}")
        return
        
    sessions = res.json()
    print(f"Found {len(sessions)} active sessions.")
    
    current_session = None
    for s in sessions:
        status = "[CURRENT]" if s["is_current"] else ""
        print(f" - ID: {s['id']} IP: {s['ip_address']} UA: {s['user_agent']} {status}")
        if s["is_current"]:
            current_session = s
            
    if not current_session:
        print("ERROR: No current session identified!")
    else:
        print("SUCCESS: Current session identified.")

    # 3. Create another session (simulate second login)
    print("\nSimulating second login...")
    res2 = requests.post(f"{BASE_URL}/auth/login", data=login_data, headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "TestScript/2.0"})
    token2 = res2.json()["access_token"]
    
    # 4. List sessions again
    print("Fetching sessions again (should be 2+)...")
    res = requests.get(f"{BASE_URL}/sessions/", headers=headers)
    sessions = res.json()
    print(f"Found {len(sessions)} active sessions.")
    for s in sessions:
        print(f" - ID: {s['id']} UA: {s['user_agent']}")

    # 5. Revoke the NEW session using the OLD token
    # We need to find the ID of the new session (where UA is TestScript/2.0)
    target_session = next((s for s in sessions if s["user_agent"] == "TestScript/2.0"), None)
    
    if target_session:
        print(f"\nRevoking session {target_session['id']}...")
        res = requests.delete(f"{BASE_URL}/sessions/{target_session['id']}", headers=headers)
        if res.status_code == 204:
            print("Revocation successful.")
        else:
            print(f"Revocation failed: {res.status_code} {res.text}")
    
    # 6. Verify revocation
    print("\nVerifying revocation...")
    res = requests.get(f"{BASE_URL}/sessions/", headers=headers)
    sessions = res.json()
    # Revoked sessions are filtered out in the API
    revoked_still_exists = any(s['id'] == target_session['id'] for s in sessions) if target_session else False
    
    if not revoked_still_exists and target_session:
        print("SUCCESS: Revoked session is no longer listed.")
    else:
        print("ERROR: Revoked session still appears!")

if __name__ == "__main__":
    test_session_flow()
