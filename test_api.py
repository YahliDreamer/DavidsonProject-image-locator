import requests

# 1. Login
login_data = {
    "email": "a",   # 🔁 Replace with real user email
    "password": "a"   # 🔁 Replace with the password
}

response = requests.post("http://localhost:5000/auth/login", json=login_data)
if response.status_code != 200:
    print("❌ Login failed:", response.text)
    exit()

data = response.json()
token = data["access_token"]

print(f"✅ Logged in! Token: {token}")

# 2. Use the token to fetch detections
headers = {"Authorization": f"Bearer {token}"}
detections_response = requests.get("http://localhost:5000/user/detections?limit=50", headers=headers)

print("\n📦 Detections Response:")
print(detections_response.json())
