import requests
import sys
import json

BASE_URL = "http://localhost:8000/api/v1"

def login(username, password):
    res = requests.post(f"{BASE_URL}/auth/login", data={"username": username, "password": password})
    if res.status_code != 200:
        print(f"Login failed for {username}: {res.text}")
        sys.exit(1)
    return res.json()["access_token"]

def test_risk_flow():
    print("--- 1. Login as Admin (acts as both Maker/Checker for test) ---")
    token = login("test_admin_auto", "password123")
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n--- 2. Create New Risk Event Request ---")
    payload = {
        "action": "create",
        "payload": {
            "reportTitle": "Test Incident 001",
            "clientCode": "CLI-TEST",
            "riskDescription": "Test Risk",
            "severity": "medium",
            "impact": "Test Impact",
            "actionTaken": "Test Action",
            "followUpPlan": "None",
            "status": "Waiting for Approval",
            "date": "2024-01-01"
        },
        "note": "Please approve this test."
    }
    
    res = requests.post(f"{BASE_URL}/risk-events/request", json=payload, headers=headers)
    if res.status_code != 200:
        print(f"Failed to create request: {res.text}")
        return
    
    req_data = res.json()
    req_id = req_data["id"]
    print(f"Request Created: {req_id}")
    
    print("\n--- 3. List Pending Approvals ---")
    res = requests.get(f"{BASE_URL}/risk-events/approvals/pending", headers=headers)
    pending = res.json()
    print(f"Pending Requests: {len(pending)}")
    found = any(r["id"] == req_id for r in pending)
    if not found:
        print("Error: Newly created request not found in pending list!")
        return
        
    print("\n--- 4. Approve Request ---")
    res = requests.post(f"{BASE_URL}/risk-events/approvals/{req_id}/approve", headers=headers)
    if res.status_code != 200:
        print(f"Approval failed: {res.text}")
        return
    print("Request Approved.")
    
    print("\n--- 5. Verify Incident Created ---")
    res = requests.get(f"{BASE_URL}/risk-events/", headers=headers)
    events = res.json()
    print(f"Total Events: {len(events)}")
    
    # Check if our event is there
    event = next((e for e in events if e["report_title"] == "Test Incident 001"), None)
    if event:
        print(f"SUCCESS: Found Created Event {event['id']}")
        if event["status"] == "Published":
             print("SUCCESS: Status is Published")
        else:
             print(f"FAILURE: Status is {event['status']} (Expected Published)")
    else:
        print("FAILURE: Event not found in list.")

if __name__ == "__main__":
    test_risk_flow()
