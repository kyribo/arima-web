import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"

def debug_api():
    # Login as admin
    res = requests.post(f"{BASE_URL}/auth/login", data={"username": "test_admin_auto", "password": "password123"})
    if res.status_code != 200:
        print("Login failed")
        return
    token = res.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n--- Listing Risk Events ---")
    res = requests.get(f"{BASE_URL}/risk-events/", headers=headers)
    print(f"Status: {res.status_code}")
    if res.status_code == 200:
        data = res.json()
        print(f"Count: {len(data)}")
        for item in data:
            print(f"ID: {item['id']}, Title: {item['report_title']}, Status: {item['status']}")
    else:
        print(res.text)

if __name__ == "__main__":
    debug_api()
