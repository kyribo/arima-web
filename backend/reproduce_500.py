import requests

BASE_URL = "http://localhost:8000/api/v1"
USERNAME = "admin@arima.com"
PASSWORD = "Admin123!"

def test_login():
    print("Testing Login scenarios...")

    # 1. Normal Login (No OTP) - Expect 401 if 2FA enabled
    try:
        res = requests.post(f"{BASE_URL}/auth/login", data={"username": USERNAME, "password": PASSWORD})
        print(f"1. No OTP: {res.status_code} {res.text}")
    except Exception as e:
        print(f"1. Error: {e}")

    # 2. Empty OTP - Expect 401
    try:
        res = requests.post(f"{BASE_URL}/auth/login", data={"username": USERNAME, "password": PASSWORD, "otp": ""})
        print(f"2. Empty OTP: {res.status_code} {res.text}")
    except Exception as e:
        print(f"2. Error: {e}")

    # 3. Invalid OTP - Expect 401
    try:
        res = requests.post(f"{BASE_URL}/auth/login", data={"username": USERNAME, "password": PASSWORD, "otp": "123456"})
        print(f"3. Invalid OTP: {res.status_code} {res.text}")
    except Exception as e:
        print(f"3. Error: {e}")

    # 4. Bad Password - Expect 401
    try:
        res = requests.post(f"{BASE_URL}/auth/login", data={"username": USERNAME, "password": "WrongPassword"})
        print(f"4. Bad Pass: {res.status_code} {res.text}")
    except Exception as e:
        print(f"4. Error: {e}")

if __name__ == "__main__":
    test_login()
