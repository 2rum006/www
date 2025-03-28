import os
import time
import random
import requests
import getpass
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from colorama import Fore, Style, init
import pyfiglet

init(autoreset=True)

# Set your desired password here
TOOL_PASSWORD = "wew"

class CODMChecker:
    def __init__(self):
        self.valid_count = 0
        self.invalid_count = 0
        self.banned_count = 0
        self.checked_count = 0
        self.total_accounts = 0
        self.start_time = None
        self.results_dir = "results"

        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.valid_file = os.path.join(self.results_dir, f"valid_codm_{timestamp}.txt")
        self.invalid_file = os.path.join(self.results_dir, f"invalid_codm_{timestamp}.txt")
        self.banned_file = os.path.join(self.results_dir, f"banned_codm_{timestamp}.txt")

        self.user_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
            "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36"
        ]

    def verify_password(self):
        os.system("cls" if os.name == "nt" else "clear")
        title = pyfiglet.figlet_format("CODM Checker", font="slant")
        print(Fore.CYAN + title + Style.RESET_ALL)

        for _ in range(3):  # Allow up to 3 attempts
            entered_password = getpass.getpass(Fore.YELLOW + "🔐 Enter Password: " + Style.RESET_ALL)
            if entered_password == TOOL_PASSWORD:
                print(Fore.GREEN + "✅ Access Granted! Welcome to CODM Checker.\n" + Style.RESET_ALL)
                return True
            else:
                print(Fore.RED + "❌ Incorrect Password! Try again.\n" + Style.RESET_ALL)
        print(Fore.RED + "🚨 Too many failed attempts. Exiting..." + Style.RESET_ALL)
        exit()

    def print_header(self):
        os.system("cls" if os.name == "nt" else "clear")
        title = pyfiglet.figlet_format("CODM Checker", font="slant")
        print(Fore.CYAN + title + Style.RESET_ALL)
        print(Fore.YELLOW + "═════════════════════════════════════════════")
        print(Fore.GREEN + "    🔥 Created by: MrModder")
        print(Fore.BLUE + "    🚀 Fast Multi-threaded Checking")
        print(Fore.RED + "    🚨 Account Status: Active / Banned")
        print(Fore.YELLOW + "═════════════════════════════════════════════" + Style.RESET_ALL)

    def check_account(self, account):
        try:
            email, password = account.strip().split(":")
            login_url = "https://sso.garena.com/universal/login?app_id=10100&redirect_uri=https%3A%2F%2Faccount.garena.com%2F&locale=en-PH"  # Placeholder URL

            data = {
                "email": email,
                "password": password,
                "remember_me": "true"
            }

            headers = {
                "User-Agent": random.choice(self.user_agents),
                "Content-Type": "application/json"
            }

            # Simulated response (Replace with real API checking)
            login_status = random.choice(["valid", "invalid", "banned"])

            time.sleep(random.uniform(0.5, 1.5))
            self.checked_count += 1

            if login_status == "valid":
                self.valid_count += 1
                with open(self.valid_file, "a") as f:
                    f.write(f"{email}:{password} | Status: ACTIVE\n")
                return Fore.GREEN + f"✅ VALID | {email}:{password} | Status: ACTIVE" + Style.RESET_ALL

            elif login_status == "banned":
                self.banned_count += 1
                with open(self.banned_file, "a") as f:
                    f.write(f"{email}:{password} | Status: BANNED\n")
                return Fore.RED + f"🚨 BANNED | {email}:{password} | Status: BANNED" + Style.RESET_ALL

            else:
                self.invalid_count += 1
                with open(self.invalid_file, "a") as f:
                    f.write(f"{email}:{password}\n")
                return Fore.RED + f"❌ INVALID | {email}:{password}" + Style.RESET_ALL

        except Exception as e:
            self.invalid_count += 1
            return Fore.YELLOW + f"⚠️ ERROR | {account} | {str(e)}" + Style.RESET_ALL

    def print_stats(self):
        elapsed_time = time.time() - self.start_time if self.start_time else 0
        minutes, seconds = divmod(int(elapsed_time), 60)

        stats = f"""
{Fore.YELLOW}═════════════════════════════════════════════{Style.RESET_ALL}
{Fore.BLUE}  Progress: {self.checked_count}/{self.total_accounts} ({int(self.checked_count/self.total_accounts*100) if self.total_accounts else 0}%)
  ✅ Valid: {self.valid_count}  |  ❌ Invalid: {self.invalid_count}  |  🚨 Banned: {self.banned_count}
  ⏳ Time Elapsed: {minutes}m {seconds}s
{Fore.YELLOW}═════════════════════════════════════════════{Style.RESET_ALL}
"""
        print(stats)

    def run(self):
        self.verify_password()  # Require password before running
        self.print_header()

        accounts_file = input(Fore.CYAN + "📂 Enter path to accounts file (email:password format): " + Style.RESET_ALL)
        if not os.path.exists(accounts_file):
            print(Fore.RED + f"❌ File not found: {accounts_file}" + Style.RESET_ALL)
            return

        with open(accounts_file, "r") as f:
            accounts = [line.strip() for line in f if ":" in line]

        self.total_accounts = len(accounts)
        if self.total_accounts == 0:
            print(Fore.RED + "❌ No valid accounts found in the file." + Style.RESET_ALL)
            return

        try:
            threads = int(input(Fore.CYAN + f"⚡ Enter number of threads (max {min(100, self.total_accounts)}): " + Style.RESET_ALL))
            threads = min(max(1, threads), min(100, self.total_accounts))
        except:
            threads = min(5, self.total_accounts)

        print(Fore.GREEN + f"\n🚀 Starting to check {self.total_accounts} accounts with {threads} threads..." + Style.RESET_ALL)
        time.sleep(2)

        self.start_time = time.time()

        with ThreadPoolExecutor(max_workers=threads) as executor:
            for i, result in enumerate(executor.map(self.check_account, accounts)):
                if i % 5 == 0 or i == self.total_accounts - 1:
                    self.print_stats()
                print(result)
                time.sleep(0.1)

        print(Fore.YELLOW + "\n✅ Checking Completed! Results saved in the results folder.\n" + Style.RESET_ALL)

if __name__ == "__main__":
    checker = CODMChecker()
    checker.run()