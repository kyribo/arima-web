import requests
from sqlalchemy import create_engine, text
import sys
import os

# Add backend directory to sys.path to ensure imports work if needed, 
# but relying on direct requests here.

DATABASE_URL = "postgresql://arimadev:rizkytampan@localhost:5432/arimadev"
BASE_URL = "http://localhost:8000/api/v1"

def test_crud():
    username = "test_admin_auto"
    password = "password123"

    print(f"Using Test Admin: {username}")
    
    token = None
    try:
        res = requests.post(f"{BASE_URL}/auth/login", data={"username": username, "password": password})
        if res.status_code == 200:
            print(f"Login successful")
            token = res.json()["access_token"]
        else:
            print(f"Login failed: {res.text}")
            return
    except Exception as e:
        print(f"Connection error: {e}")
        return

    if not token:
        print("Failed to login with common passwords.")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create User
    new_user = {
        "username": "testuser_api",
        "email": "testapi@example.com",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User",
        "role": "User",
        "access": ["dashboard.view"]
    }
    
    # Cleanup first if exists
    # We can't delete by username directly via API without ID, so we might fail create if exists.
    # But checking list first.
    
    print("Creating user...")
    res = requests.post(f"{BASE_URL}/users/", json=new_user, headers=headers)
    if res.status_code == 200:
        created_user = res.json()
        print("User created:", created_user["id"])
    elif res.status_code == 400 and "exists" in res.text:
        print("User already exists, finding it...")
        # List users to find ID
        res = requests.get(f"{BASE_URL}/users/", headers=headers, params={"search": "testuser_api"})
        users = res.json()
        if users:
            created_user = users[0]
            print("Found existing user:", created_user["id"])
        else:
            print("Could not find existing user??")
            return
    else:
        print("Failed to create user:", res.status_code, res.text)
        return

    user_id = created_user["id"]

    # 2. Update User
    print("Updating user...")
    update_data = {"first_name": "Updated API"}
    res = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data, headers=headers)
    if res.status_code == 200:
        print("User updated:", res.json()["first_name"])
    else:
        print("Update failed:", res.status_code, res.text)

    # 3. List Users
    print("Listing users...")
    res = requests.get(f"{BASE_URL}/users/", headers=headers)
    if res.status_code == 200:
        users = res.json()
        print(f"Total users: {len(users)}")
    else:
        print("List failed:", res.status_code, res.text)

    # 4. Delete User
    print("Deleting user...")
    res = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
    if res.status_code == 204:
        print("User deleted successfully.")
    else:
        print("Delete failed:", res.status_code, res.text)

if __name__ == "__main__":
    test_crud()
