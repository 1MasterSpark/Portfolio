import base64
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
SCOPES = "offline_access openid sme-banking sme-company-file sme-company-settings sme-contacts-customer sme-contacts-employee sme-contacts-personal sme-contacts-supplier sme-general-ledger sme-inventory sme-payroll sme-purchases sme-sales sme-timebilling"
ENDPOINT = "https://api.myob.com/accountright/c21df0ac-098c-4da0-b6a5-5e77aaca90da/Contact/EmployeePayrollDetails"

header = "\033[95m"
blue = "\033[94m"
cyan = "\033[96m"
green = "\033[92m"
warning = "\033[93m"
fail = "\033[91m"
bold = "\033[1m"
underline = "\033[4m"
def cprint(text, color):
    print(f"{color}{text}\033[0m")

def get_refresh_token():
    REDIRECT_URI = "https://flow.proveng.com.au/users/auth/stripe_connect/callback"
    # REDIRECT_URI = "https://infra.proveng.com.au/users/auth/stripe_connect/callback"
    authorization_code = "ory_ac_AErei-oFcL2eV0kHnVdKtkc4s57gI70FDx4G65j6YJk.hxHF3WFnEs2eNTgHw8wx_xmRpQ6B-lyU3r5yCg3GfNo"

    token_url = "https://secure.myob.com/oauth2/v1/authorize"
    payload = {
        'client_id': API_KEY,
        'client_secret': API_SECRET,
        'scope': SCOPES,
        'code': authorization_code,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(token_url, headers=headers, data=payload)

    if response.status_code == 200:
        refresh_token = response.json()
        cprint("Successfully obtained refresh token!", green)
        print(json.dumps(refresh_token, indent=2))
        cprint("You can now use the main script", green)
    else:
        cprint("Error getting token", fail)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

def get_new_access_token(refresh_token):
    token_url = "https://secure.myob.com/oauth2/v1/authorize"
    payload = {
        'client_id': API_KEY,
        'client_secret': API_SECRET,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(token_url, headers=headers, data=payload)
    
    if response.status_code == 200:
        token_data = response.json()
        # print(json.dumps(token_data, indent=2))
        return token_data['access_token']
    else:
        cprint("Error refreshing token:", fail)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def validate_user(access_token):
    cprint("\nValidating user for the access token...", cyan)
    
    validate_url = "https://secure.myob.com/oauth2/v1/Validate"
    
    params = {
        'scope': SCOPES
    }

    headers = {
        'Authorization': f'Bearer {access_token}',
        'x-myobapi-key': API_KEY
    }

    response = requests.get(validate_url, headers=headers, params=params)

    if response.status_code == 200:
        cprint("Validation successful!", green)
        user_data = response.json()
        print(json.dumps(user_data, indent=2))
    else:
        cprint("Validation FAILED", fail)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

def connect_online():
    cprint("Refreshing access token...", cyan)
    access_token = get_new_access_token(REFRESH_TOKEN)

    if access_token:
        cprint(f"Successfully got new access token ({access_token})", green)
        # validate_user(access_token)

        api_headers = {
            'Authorization': f'Bearer {access_token}',
            'x-myobapi-key': API_KEY,
            'x-myobapi-version': 'v2'
        }

        cprint("Fetching company files...", cyan)
        response = requests.get(ENDPOINT, headers=api_headers)
        return response

def connect_local():
    api_base_url = "http://localhost:8080/accountright/"
    credentials = "Master Spark:password"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    api_headers = {
        'x-myobapi-cftoken': encoded_credentials,
        'x-myobapi-key': API_KEY,
        'x-myobapi-version': 'v2'
    }

    cprint("Fetching local company files...", cyan)
    response = requests.get(api_base_url, headers=api_headers)
    return response
    
def main():
    if not API_KEY or not API_SECRET or not REFRESH_TOKEN:
        cprint("API_KEY, API_SECRET, and/or REFRESH_TOKEN could not be found", fail)
        return

    response = connect_online()
    # response = connect_local()

    if response.status_code == 200:
        company_files = response.json()
        # print(json.dumps(company_files, indent=2))

        employees = company_files.get("Items", [])
        for emp in employees:
            cprint(emp["Employee"]["Name"], blue)
            entitlements = emp.get("Entitlements", [])
            personal_leave = None
            holiday_leave = None

            for e in entitlements:
                name = e.get("EntitlementCategory", {}).get("Name", "")
                if name == "Sick Leave Accrual":
                    personal_leave = e.get("Total", 0)
                elif name == "Holiday Leave Accrual":
                    holiday_leave = e.get("Total", 0)

            print(f"Personal Leave: {personal_leave if personal_leave is not None else 'N/A'}")
            print(f"Holiday Leave: {holiday_leave if holiday_leave is not None else 'N/A'}")
    else:
        cprint("Error fetching company files:", fail)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    # get_refresh_token()
    main()