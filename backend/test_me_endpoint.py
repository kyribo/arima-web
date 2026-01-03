import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"

def test_me():
    username = "test_admin_auto"
    password = "password123"

    print(f"Logging in as {username}...")
    try:
        res = requests.post(f"{BASE_URL}/auth/login", data={"username": username, "password": password})
        if res.status_code != 200:
            print(f"Login failed: {res.text}")
            return
        
        token = res.json()["access_token"]
        print("Login successful. Token acquired.")
        
        headers = {"Authorization": f"Bearer {token}"}
        print("Fetching /users/me...")
        me_res = requests.get(f"{BASE_URL}/users/me", headers=headers)
        
        if me_res.status_code == 200:
            print(f"Success! Data: {me_res.json()}")
        else:
            print(f"Failed to fetch /me. Status: {me_res.status_code}")
            print(f"Response: {me_res.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_me()
