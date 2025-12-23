import requests

def test_profile_flow():
    # 1. Login
    login_url = "http://localhost:8000/api/v1/auth/login"
    login_data = {"username": "admin@arima.com", "password": "Admin123!"}
    
    print(f"Logging in to {login_url}...")
    resp = requests.post(login_url, data=login_data)
    
    if resp.status_code != 200:
        print(f"Login Failed: {resp.text}")
        return
        
    token = resp.json()["access_token"]
    print("Login Success. Token received.")
    
    # 2. Get Profile
    profile_url = "http://localhost:8000/api/v1/users/me"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"Fetching profile from {profile_url}...")
    resp = requests.get(profile_url, headers=headers)
    
    if resp.status_code == 200:
        print("Profile Fetch Success!")
        print(resp.json())
    else:
        print(f"Profile Fetch Failed: {resp.text}")

    # 3. Update Profile (Test)
    print("Updating profile bio...")
    update_data = {"bio": "Updated via Automated Test"}
    resp = requests.put(profile_url, headers=headers, json=update_data)
    
    if resp.status_code == 200:
        print("Profile Update Success!")
        print(resp.json())
    else:
        print(f"Profile Update Failed: {resp.text}")

if __name__ == "__main__":
    test_profile_flow()
