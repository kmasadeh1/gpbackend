
import os
import django
import sys
import json

# Setup Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), 'fortigrc_backend'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fortigrc_backend.settings")
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()
client = APIClient()

def test_auth_flow():
    print("Starting Authentication Flow Test...")
    
    # 1. Cleanup
    email = "testuser@example.com"
    password = "strongpassword123"
    if User.objects.filter(email=email).exists():
        print(f"Cleaning up existing user {email}...")
        User.objects.filter(email=email).delete()

    # 2. Register
    register_url = "/api/auth/register/"
    register_data = {
        "email": email,
        "password": password,
        "first_name": "Test",
        "last_name": "User"
    }

    print(f"\n1. Testing Registration ({register_url})...")
    response = client.post(register_url, register_data, format='json')
    
    if response.status_code == 201:
        print("✅ Registration Successful!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Registration Failed: {response.status_code}")
        try:
            print(response.data)
        except AttributeError:
            with open("error.html", "wb") as f:
                f.write(response.content)
            print("Saved error content to error.html")
        return False

    # 3. Login
    login_url = "/api/auth/login/"
    login_data = {
        "username": email,
        "password": password
    }

    print(f"\n2. Testing Login ({login_url})...")
    response = client.post(login_url, login_data, format='json')

    if response.status_code == 200:
        print("✅ Login Successful!")
        tokens = response.json()
        print(json.dumps(tokens, indent=2))
        
        if 'access' in tokens and 'refresh' in tokens:
            print("✅ Tokens received correctly!")
            
            # 4. Verify Role in Token response (if implemented) or decode token
            if 'role' in tokens:
                 print(f"✅ Role found in response: {tokens['role']}")
            
            return True
        else:
            print("❌ Tokens missing in response.")
            return False
    else:
        print(f"❌ Login Failed: {response.status_code}")
        print(response.data)
        return False

if __name__ == "__main__":
    success = test_auth_flow()
    if success:
        print("\n🎉 All authentication tests passed!")
    else:
        print("\n⚠️ Authentication tests failed.")
