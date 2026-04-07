#!/data/data/com.termux/files/usr/bin/python

import os
import requests
import json
import time
import sys
import random

# --- CONFIGURATION ---
API_BASE_URL = "https://kayzennv3.squareweb.app/api"
API_KEY = "APIKEY38"
DB_FILE = os.path.expanduser("~/access_key.json")  # DB_FILE гэж зассан

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
        params = {"key": self.api_key}
        try:
            response = requests.post(url, params=params, json=data, timeout=25)
            return response.json()
        except Exception as e:
            return {"ok": False, "message": f"Server Error: {str(e)}"}

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
def clear_screen(): 
    os.system('clear' if os.name != 'nt' else 'cls')

def get_ip():
    try: 
        return requests.get('https://api.ipify.org', timeout=5).text
    except: 
        return "127.0.0.1"

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f: 
                return json.load(f)
        except: 
            return {}
    return {}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f: 
        json.dump(data, f, indent=4)

def show_header():
    header = """
====================================================

PLEASE LOGOUT FROM CPM BEFORE USING THIS TOOL

SHARING THE ACCESS KEY IS NOT ALLOWED AND WILL BE BLOCKED

Telegram: @BALDANSHOP_CHANNEL Or @BALDANSHOP_V3_BOT

====================================================="""
    print_rainbow(header)

# --- INITIAL DB SETUP (анх удаа ажиллуулахад) ---
def init_db():
    if not os.path.exists(DB_FILE):
        initial_data = {
            "USER123": {
                "key": "TESTKEY001",
                "balance": 100000,
                "unlimited": False,
                "is_blocked": False
            },
            "USER456": {
                "key": "SEREKBOL69",
                "balance": 999999999,
                "unlimited": True,
                "is_blocked": False
            }
        }
        save_db(initial_data)
        print_rainbow("[✓] Шинэ DB файл үүсгэлээ: ~/access_key.json")
        time.sleep(1)

# --- MAIN LOGIC ---
def main():
    # Эхлээд DB үүсгэх
    init_db()
    
    client = CPMApiClient(API_BASE_URL, API_KEY)
    ip_addr = get_ip()
    last_choice = None
    last_ans = None

    while True:  # Home Loop
        auth_token = None
        user_id_ref = None
        is_unlimited = False
        email = ""
        password = ""
        access_key = ""

        # 1. LOGIN SCREEN
        while True:
            clear_screen()
            show_header()
            email = input(rainbow_text("[?] Account Email: "))
            password = input(rainbow_text("[?] Account Password: "))
            access_key = input(rainbow_text("[?] Access Key: "))

            if not email or not password or not access_key:
                print_rainbow("\n[!] Note: make sure you filled out the fields!")
                time.sleep(2)
                continue

            db = load_db()
            key_found = False

            # Verify Access Key
            if access_key == "SEREKBOL69":
                key_found = True
                user_id_ref = "ADMIN"
                is_unlimited = True
            else:
                for uid, data in db.items():
                    if data.get('key') == access_key:
                        if data.get('is_blocked'):
                            print_rainbow("\n[!] ACCESS INVALID - KEY IS BLOCKED!")
                            sys.exit()
                        user_id_ref = uid
                        is_unlimited = data.get('unlimited', False)
                        key_found = True
                        break

            if not key_found:
                print_rainbow("\n[✘] Trying to Login: TRY AGAIN.")
                time.sleep(2)
                continue

            # API Login
            res = client.make_request("account_login", {"account_email": email, "account_password": password})
            if res.get('ok') or res.get('error') == 0:
                auth_token = res.get('auth') or res.get('data', {}).get('auth')
                print_rainbow("\n[✓] Trying to Login: SUCCESSFUL")
                time.sleep(1)
                break
            else:
                print_rainbow("\n[✘] Trying to Login: TRY AGAIN.")
                print_rainbow("[!] Note: make sure you filled out the fields!")
                time.sleep(2)

        # 2. MENU SCREEN
        while True:
            clear_screen()
            show_header()
            db = load_db()
            
            # Хэрэглэгч блоклогдсон эсэх шалгах
            if user_id_ref != "ADMIN" and db.get(user_id_ref, {}).get('is_blocked'):
                print_rainbow("\n[!] Your access key has been blocked!")
                sys.exit()

            # Balance авах
            if user_id_ref == "ADMIN":
                balance = 999999999
            else:
                balance = db.get(user_id_ref, {}).get('balance', 0)

            # Мэдээлэл харуулах
            print_rainbow(f"\nEMAIL : {email}")
            print_rainbow(f"PASSWORD : {password}")
            print_rainbow(f"ACCESS KEY : {access_key}")
            print_rainbow(f"TELEGRAM ID : {user_id_ref}")
            print_rainbow(f"IP ADDRESS : {ip_addr}")
            print_rainbow(f"BALANCE : {'Unlimited ♾️' if is_unlimited else f'{balance:,}'}")
            print_rainbow("-" * 52)
            print_rainbow("1. SET RANK              30.5K")
            print_rainbow("2. CHANGE EMAIL          25.5K")
            print_rainbow("3. CHANGE PASSWORD        6K")
            print_rainbow("4. REGISTER              FREE")
            print_rainbow("5. LOGOUT FROM ACCOUNT")
            print_rainbow("6. EXIT FROM TOOL")
            print_rainbow("-" * 52)

            choice = input(rainbow_text("Select Option: "))

            if choice == "6":
                print_rainbow("\n[✓] Exit from tool. Goodbye!")
                sys.exit()

            if choice == "5":
                print_rainbow("\n[✓] Account signed out successfully!")
                time.sleep(1)
                break

            if choice in PRICES:
                cost = PRICES[choice]
                
                # Balance шалгах
                if not is_unlimited and balance < cost:
                    print_rainbow(f"\n[✘] Insufficient balance! Need {cost:,} but you have {balance:,}")
                    time.sleep(2)
                    continue

                res_act = {"ok": False}
                
                if choice == "1":  # SET RANK
                    print_rainbow("\n[%] Giving you KING RANK...")
                    res_act = client.make_request("set_rank", {"account_auth": auth_token})
                    if res_act.get('ok'):
                        print_rainbow("[✓] KING RANK - SUCCESSFUL!")
                    else:
                        print_rainbow("[✘] KING RANK - FAILED! Try again.")

                elif choice == "2":  # CHANGE EMAIL
                    print_rainbow("\n[%] Change email...")
                    new_email = input(rainbow_text("Your new email: "))
                    if new_email:
                        res_act = client.make_request("change_email", {"account_auth": auth_token, "new_email": new_email})
                        if res_act.get('ok'):
                            print_rainbow(f"[✓] Email changed to: {new_email}")
                        else:
                            print_rainbow("[✘] Change email - FAILED!")
                    else:
                        print_rainbow("[✘] Email cannot be empty!")
                        continue

                elif choice == "3":  # CHANGE PASSWORD
                    print_rainbow("\n[%] Change password...")
                    new_password = input(rainbow_text("Your new password: "))
                    if new_password:
                        res_act = client.make_request("change_password", {"account_auth": auth_token, "new_password": new_password})
                        if res_act.get('ok'):
                            print_rainbow("[✓] Password changed successfully!")
                        else:
                            print_rainbow("[✘] Change password - FAILED!")
                    else:
                        print_rainbow("[✘] Password cannot be empty!")
                        continue

                elif choice == "4":  # REGISTER
                    print_rainbow("\n[%] Register new account...")
                    reg_email = input(rainbow_text("Register Email: "))
                    reg_pass = input(rainbow_text("Register Password: "))
                    if reg_email and reg_pass:
                        res_act = client.make_request("account_register", {"account_email": reg_email, "account_password": reg_pass})
                        if res_act.get('ok') or res_act.get('error') == 0:
                            print_rainbow("[✓] Account registered successfully!")
                        else:
                            print_rainbow(f"[✘] Registration failed! Error: {res_act.get('error', 'Unknown')}")
                    else:
                        print_rainbow("[✘] Email and password cannot be empty!")
                        continue

                # Хэрэв амжилттай бол balance-с хасах
                if res_act.get('ok') and not is_unlimited and choice != "4":
                    db = load_db()
                    if user_id_ref in db:
                        db[user_id_ref]['balance'] = db[user_id_ref].get('balance', 0) - cost
                        save_db(db)
                        print_rainbow(f"\n[✓] {cost:,} deducted from your balance!")

                # Үргэлжлүүлэх эсэх
                ans = input(rainbow_text("\n[?] Do you want to exit? (y/n): ")).lower()
                if ans == 'y':
                    print_rainbow("\n[✓] Account signed out successfully!")
                    time.sleep(1)
                    break
            else:
                print_rainbow("\n[✘] Invalid option! Please select 1-6")
                time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_rainbow("\n\n[!] Exited by user. Goodbye!")
        sys.exit()
    except Exception as e:
        print_rainbow(f"\n[!] Unexpected error: {str(e)}")
        sys.exit()

