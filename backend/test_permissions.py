import requests
import sys
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def login(username, password):
    try:
        res = requests.post(f"{BASE_URL}/auth/login", data={"username": username, "password": password})
        if res.status_code == 200:
            return res.json()["access_token"]
    except:
        pass
    return None

def create_or_update_user(admin_token, username, role, access_list):
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Check if exists
    res = requests.get(f"{BASE_URL}/users/", params={"search": username}, headers=headers)
    if res.status_code == 200:
        users = res.json()
        target = next((u for u in users if u["username"] == username), None)
        if target:
            # Update
            payload = {
                "access": access_list,
                "role": role,
                "is_active": True
            }
            res = requests.put(f"{BASE_URL}/users/{target['id']}", json=payload, headers=headers)
            if res.status_code != 200:
                print(f"Failed to update {username}: {res.text}")
            return
            
    # Create
    payload = {
        "username": username,
        "email": f"{username}@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": role,
        "role": role,
        "access": access_list,
        "is_active": True
    }
    res = requests.post(f"{BASE_URL}/users/", json=payload, headers=headers)
    if res.status_code != 200:
        print(f"Failed to create {username}: {res.text}")

def test_permissions():
    print("--- Setup: Ensuring Admin Access ---")
    admin_token = login("test_admin_auto", "password123")
    if not admin_token:
        print("Login failed for test_admin_auto. Please create superadmin first.")
        sys.exit(1)
    
    # Update Admin to have * access
    me_res = requests.get(f"{BASE_URL}/users/me", headers={"Authorization": f"Bearer {admin_token}"})
    me_id = me_res.json()["id"]
    requests.put(f"{BASE_URL}/users/{me_id}", json={"access": ["*"]}, headers={"Authorization": f"Bearer {admin_token}"})
    
    print("--- Setup: Creating Test Users ---")
    users_config = [
        ("test_viewer", "User", ["risk_event.read"]),
        ("test_maker", "User", ["risk_event.read", "risk_event.create"]),
        ("test_checker", "User", ["risk_event.read", "risk_event.approve"]),
        ("test_noaccess", "User", []),
        ("test_real_superadmin", "Superadmin", []) # Should have access despite empty list
    ]
    
    for uname, role, access in users_config:
        create_or_update_user(admin_token, uname, role, access)
        
    print("--- Verification Steps ---")
    
    # Tokens
    tokens = {}
    for uname, _, _ in users_config:
        tokens[uname] = login(uname, "password123")
        
    if not all(tokens.values()):
        print("Failed to login test users")
        sys.exit(1)
        
    headers = {u: {"Authorization": f"Bearer {t}"} for u, t in tokens.items()}
    
    # 1. READ
    print("\n1. Testing READ Access (List Events)")
    for u in tokens.keys():
        res = requests.get(f"{BASE_URL}/risk-events/", headers=headers[u])
        expected = 200
        if u == "test_noaccess": expected = 403
        
        if res.status_code == expected:
            print(f"PASS: {u} -> {res.status_code}")
        else:
            print(f"FAIL: {u} -> Expected {expected}, Got {res.status_code} ({res.text})")
            
    # 2. CREATE (Request)
    print("\n2. Testing CREATE Access (Make Request)")
    payload = {
        "action": "create",
        "payload": {"reportTitle": "Perm Test", "clientCode": "T", "riskDescription": "D", "severity": "low", "status": "Open", "date": "2024-01-01"},
        "note": "test"
    }
    req_id = None
    
    for u in tokens.keys():
        # Clean logic: expected
        expected = 403
        if u in ["test_maker", "test_real_superadmin"]: expected = 200
        # Checker shouldn't create? Unless we give them access. Config: checker has approve only.
        
        res = requests.post(f"{BASE_URL}/risk-events/request", json=payload, headers=headers[u])
        
        if res.status_code == expected:
            print(f"PASS: {u} -> {res.status_code}")
            if res.status_code == 200:
                req_id = res.json()["id"]
        else:
            print(f"FAIL: {u} -> Expected {expected}, Got {res.status_code} ({res.text})")

    if not req_id:
        print("CRITICAL: Failed to create request for approval test.")
        # Try admin create
        res = requests.post(f"{BASE_URL}/risk-events/request", json=payload, headers={"Authorization": f"Bearer {admin_token}"})
        req_id = res.json()["id"]

    # 3. APPROVE
    print(f"\n3. Testing APPROVE Access (on {req_id})")
    for u in tokens.keys():
        expected = 403
        if u in ["test_checker", "test_real_superadmin"]: expected = 200
        
        # Note: If maker tries to approve, it might fail double: Permission AND Self-approval logic (if enabled).
        # We disabled self-approval logic in code with comment, so permission check is primary.
        
        # We can't approve same req multiple times. So we create new ones or fail expectedly.
        # Current logic: 'Request already processed' if 400. That means Permission passed.
        # If 403, permission failed.
        
        res = requests.post(f"{BASE_URL}/risk-events/approvals/{req_id}/approve", headers=headers[u], json={})
        
        if res.status_code == expected:
            print(f"PASS: {u} -> {res.status_code}")
            # If successful, we need a new request for next person? 
            # Actually only one person needs to succeed (checker).
            if expected == 200:
                 # It's approved now. Reset/Create new one for others? 
                 # Or just test others first?
                 pass
        elif res.status_code == 400 and "processed" in res.text:
             # Means permission passed but logic blocked.
             if u == "test_checker":
                 print(f"PASS: {u} -> 400 (Already processed, perm OK)")
             else:
                 print(f"FAIL: {u} -> 400 (Perm check leaked!)")
        else:
            print(f"FAIL: {u} -> Expected {expected}, Got {res.status_code} ({res.text})")

if __name__ == "__main__":
    test_permissions()
