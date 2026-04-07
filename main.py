import os
import requests
import json
import time
import sys
import random

# --- CONFIGURATION ---
API_BASE_URL = "https://kayzennv3.squareweb.app/api"
API_KEY = "APIKEY38"
DB_FILE = os.path.expanduser("~/access_key.json")

PRICES = {
    "1": 30500,  # SET RANK
    "2": 25500,  # CHANGE EMAIL
    "3": 6000,   # CHANGE PASSWORD
    "4": 0       # REGISTER FREE
}

# --- API CLIENT ---
class CPMApiClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def make_request(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        params = {"api_key": self.api_key}
        try:
            response = requests.post(url, params=params, json=data, timeout=25)
            return response.json()
        except:
            return {"ok": False, "message": "Server Connection Error"}

# --- RAINBOW UI ---
def rainbow_text(text):
    colors = [
        "\033[38;5;196m", "\033[38;5;202m", "\033[38;5;208m", "\033[38;5;214m",
        "\033[38;5;220m", "\033[38;5;226m", "\033[38;5;190m", "\033[38;5;154m",
        "\033[38;5;118m", "\033[38;5;82m", "\033[38;5;46m", "\033[38;5;47m",
        "\033[38;5;48m", "\033[38;5;49m", "\033[38;5;50m", "\033[38;5;51m",
        "\033[38;5;45m", "\033[38;5;39m", "\033[38;5;33m", "\033[38;5;27m"
    ]
    return "".join([random.choice(colors) + char for char in text]) + "\033[0m"

def print_rainbow(text):
    print(rainbow_text(text))

# --- HELPERS ---
def clear(): os.system('clear')

def get_ip():
    try: return requests.get('https://api.ipify.org', timeout=5).text
    except: return "127.0.0.1"

def load_db():
    if os.path.exists(db_FILE):
        try:
            with open(db_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}

def save_db(data):
    with open(db_FILE, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)

def show_header():
    header = """====================================================

PLEASE LOGOUT FROM CPM BEFORE USING THIS TOOL

SHARING THE ACCESS KEY IS NOT ALLOWED AND WILL BE BLOCKED

Telegram: @BALDANSHOP_CHANNEL Or @BALDANSHOP_V3_BOT Chat

===================================================="""
    print_rainbow(header)

# --- MAIN LOGIC ---
def main():
    client = CPMApiClient(API_BASE_URL, API_KEY)
    ip_addr = get_ip()

    while True: # Home Loop
        auth_token = None
        user_id_ref = None
        is_unlimited = False

        # 1. LOGIN SCREEN
        while True:
            clear()
            show_header()
            email = input(rainbow_text("[?] Account Email: "))
            password = input(rainbow_text("[?] Account Password: "))
            access_key = input(rainbow_text("[?] Access Key: "))

            if not email or not password or not access_key:
                print_rainbow("\n[!] Note: make sure you filled out the fields !")
                time.sleep(2); continue

            db = load_db()
            key_found = False

            # Verify Access Key
            if access_key == "SEREKBOL69":
                key_found = True; user_id_ref = "ADMIN"; is_unlimited = True
            else:
                for uid, data in db.items():
                    if data.get('key') == access_key:
                        if data.get('is_blocked'):
                            print_rainbow("\nACCESS INVALID АРИЛ СДА МИНЬ !"); sys.exit()
                        user_id_ref = uid; is_unlimited = data.get('unlimited', False); key_found = True; break

            if not key_found:
                print_rainbow("\n[✘] Trying to Login: TRY AGAIN.")
                time.sleep(2); continue

            # API Login
            res = client.make_request("account_login", {"account_email": email, "account_password": password})
            if res.get('ok') or res.get('error') == 0:
                auth_token = res.get('auth') or res.get('data', {}).get('auth')
                print_rainbow("\n{%} Trying to Login: SUCCESSFUL")
                time.sleep(1); break
            else:
                print_rainbow("\n[✘] Trying to Login: TRY AGAIN.")
                print_rainbow("[!] Note: make sure you filled out the fields !")
                time.sleep(2)

        # 2. MENU SCREEN
        while True:
            clear()
            show_header()
            db = load_db()
            if user_id_ref != "ADMIN" and db.get(user_id_ref, {}).get('is_blocked'): sys.exit()

            balance = 999999999 if is_unlimited else db[user_id_ref]['balance']

            print_rainbow(f"EMAIL : {email}")
            print_rainbow(f"PASSWORD : {password}")
            print_rainbow(f"ACCESS KEY : {access_key}")
            print_rainbow(f"telegram id : {user_id_ref}")
            print_rainbow(f"IP ADRESS {ip_addr}")
            print_rainbow(f"BALANCE : {'Unlimited ♾️' if is_unlimited else f'{balance:,}'}")
            print_rainbow("-" * 52)
            print_rainbow("1. SET RANK               30.5K")
            print_rainbow("2. CHANGE EMAIL         25.5K")
            print_rainbow("3. CHANGE PASSWORD           6K")
            print_rainbow("4. REGISTER                           FREE")
            print_rainbow("5. LOGOUT FROM ACCOUNT")
            print_rainbow("6. EXIT FROM TOOL")
            print_rainbow("-" * 52)

            choice = input(rainbow_text("Select Option: "))

            if choice == "6":
                print_rainbow("\nexit from tool you"); sys.exit()

            if choice == "5":
                print_rainbow("\n{ You account sign out} successful"); time.sleep(1); break

            if choice in PRICES:
                cost = PRICES[choice]
                if balance < cost:
                    print_rainbow("\n[×] Insufficient balance!"); time.sleep(2); continue

                res_act = {"ok": False}
                if choice == "1":
                    print_rainbow("{%} GIVING YOU KING RANK ..")
                    res_act = client.make_request("set_rank", {"account_auth": auth_token})
                    if res_act.get('ok'): print_rainbow("{%} GIVING YOU KING RANK .. SUCCESSFUL")
                    else: print_rainbow("[×] giving you king rank ... Again")

                elif choice == "2":
                    print_rainbow("{%} cpm your email new email change")
                    new_e = input(rainbow_text("your new email: "))
                    res_act = client.make_request("change_email", {"account_auth": auth_token, "new_email": new_e})
                    if res_act.get('ok'): print_rainbow("(%) Change email.. Successfu")
                    else: print_rainbow("[×} change email ... Again")

                elif choice == "3":
                    print_rainbow("{%} cpm your password new password change")
                    new_p = input(rainbow_text("your new password: "))
                    res_act = client.make_request("change_password", {"account_auth": auth_token, "new_password": new_p})
                    if res_act.get('ok'): print_rainbow("{√} Password change ..... Successful")
                    else: print_rainbow("{×} password change .... Again")

                elif choice == "4":
                    re = input(rainbow_text("Reg Email: "))
                    rp = input(rainbow_text("Reg Pass: "))
                    print_rainbow("{ You new account register}")
                    res_act = client.make_request("account_register", {"account_email": re, "account_password": rp})
                    if res_act.get('ok'): print_rainbow("{√} register... register successfully")
                    else: print_rainbow("{x} register... Register again")

                if res_act.get('ok') and not is_unlimited:
                    db = load_db(); db[user_id_ref]['balance'] -= cost; save_db(db)

                ans = input(rainbow_text("\n{ Do you want exit } y/n (n): ")).lower()
                if ans == 'y':
                    print_rainbow("{ You account sign out} successful"); time.sleep(1); break

        # Logout logic
        if choice == "5" or (choice in PRICES and ans == 'y'):
            continue

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print_rainbow("\nexit from tool you"); sys.exit()

