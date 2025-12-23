import requests
import pyotp
import time

BASE_URL = "http://localhost:8000/api/v1"
USERNAME = "admin@arima.com"
PASSWORD = "Admin123!"

def test_2fa_flow():
    print("=== Testing 2FA Flow ===")
    
    # 1. Login normally (2FA initially disabled)
    print("\n1. Initial Login...")
    res = requests.post(f"{BASE_URL}/auth/login", data={"username": USERNAME, "password": PASSWORD})
    if res.status_code != 200:
        print(f"FAILED: Initial login failed. {res.text}")
        return
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful.")

    # 2. Setup 2FA
    print("\n2. Setting up 2FA...")
    res = requests.post(f"{BASE_URL}/auth/2fa/setup", headers=headers)
    if res.status_code != 200:
        print(f"FAILED: Setup failed. {res.text}")
        return
    data = res.json()
    secret = data["secret"]
    print(f"Setup successful. Secret: {secret}")

    # 3. Enable 2FA
    print("\n3. Enabling 2FA...")
    totp = pyotp.TOTP(secret)
    code = totp.now()
    res = requests.post(f"{BASE_URL}/auth/2fa/enable", headers=headers, json={"token": code})
    if res.status_code == 204:
        print("Enable successful.")
    else:
        print(f"FAILED: Enable failed. {res.text}")
        return

    # 4. Try Login WITHOUT OTP (Should Fail)
    print("\n4. Testing Login WITHOUT OTP (Expect Fail)...")
    res = requests.post(f"{BASE_URL}/auth/login", data={"username": USERNAME, "password": PASSWORD})
    if res.status_code == 401 and "2FA code required" in res.text:
        print("SUCCESS: Login rejected as expected.")
    else:
        print(f"FAILED: Login should have failed but got {res.status_code} {res.text}")

    # 5. Try Login WITH OTP (Should Succeed)
    print("\n5. Testing Login WITH OTP...")
    code = totp.now()
    res = requests.post(f"{BASE_URL}/auth/login", data={"username": USERNAME, "password": PASSWORD, "otp": code})
    if res.status_code == 200:
        print("SUCCESS: Login with OTP successful.")
        token = res.json()["access_token"] # Update token for next steps
        headers = {"Authorization": f"Bearer {token}"}
    else:
        print(f"FAILED: Login with OTP failed. {res.text}")
        return

    # 6. Disable 2FA
    print("\n6. Disabling 2FA...")
    res = requests.post(f"{BASE_URL}/auth/2fa/disable", headers=headers)
    if res.status_code == 204:
        print("Disable successful.")
    else:
        print(f"FAILED: Disable failed. {res.text}")
        return

    # 7. Verify Disable (Login without OTP should work again)
    print("\n7. Verifying Disable...")
    res = requests.post(f"{BASE_URL}/auth/login", data={"username": USERNAME, "password": PASSWORD})
    if res.status_code == 200:
        print("SUCCESS: Login without OTP works again.")
    else:
        print(f"FAILED: Login failed after disable. {res.text}")

if __name__ == "__main__":
    test_2fa_flow()
