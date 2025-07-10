from colorama import init, Fore, Style
from cliColors import info, success, warning, error, prompt
from login import login_and_get_jwt, logout, load_llm_credentials, save_llm_credentials
from projects import choose_project_key
from securityHotspots import fetch_security_hotspots, fetch_security_hotspots_full
from dataexport import export_all
from llmLogic import analyze_hotspot
import os
import getpass

# Initialize colorama
init(autoreset=True)

# === CONFIGURATION ===
SONAR_URL = "http://localhost:9000"
LOGIN_URL = f"{SONAR_URL}/api/authentication/login"
CREDENTIALS_FILE = "credentials.json"
EXPORT_DIR = "exports"


if __name__ == "__main__":
    session, jwt = login_and_get_jwt(CREDENTIALS_FILE, LOGIN_URL)
    try:
        while True: 
            print("\n" + "=" * 50 + "\n")
            print("1. Export Security Hotspots")
            print("2. Use AI to Analyze Hotspots")
            print("3. Exit")
            choice = int(prompt("Choose an option:"))
            if choice == 1:
                while True:
                    print("\n" + "=" * 50 + "\n")
                    projectKey = choose_project_key(session, SONAR_URL)
                    hotspots = fetch_security_hotspots(session, projectKey, SONAR_URL)
                    export_all(hotspots, f"{projectKey}.xlsx", EXPORT_DIR)

                    cont = prompt("Do you want to export another project? (y/n):").lower()
                    if cont != 'y':
                        break
            if choice == 2:
                print("\n" + "=" * 50 + "\n")
                creds = load_llm_credentials(CREDENTIALS_FILE)
                api_key = creds.get("api_key")

                if not api_key:
                    api_key = getpass.getpass("Enter API key for Google Gemini: ")
                    creds["api_key"] = api_key
                    save_llm_credentials(creds, CREDENTIALS_FILE)

                os.environ["GOOGLE_API_KEY"] = api_key
                projectKey = choose_project_key(session, SONAR_URL)
                hotspots = fetch_security_hotspots_full(session, projectKey, SONAR_URL)
                results = []
                count = len(hotspots)
                for hotspot in hotspots:
                    print("Analyzing {} out of {} hotspots...".format(len(results) + 1, count))
                    result = analyze_hotspot(hotspot)
                    results.append({
                        "Vulnerability Name": result["Vulnerability Name"],
                        "File": hotspot["File"],
                        "Line": hotspot["Line"],
                        "Detailed Observation": result["Detailed Observation"],
                        "Impact": result["Impact"],
                        "Recommendation": result["Recommendation"],
                        "False Positive": result["False Positive"],
                    })
                export_all(results, f"{projectKey}.xlsx", EXPORT_DIR)
            if choice == 3:
                print("Exiting...")
                break
    finally:
        logout(session,SONAR_URL)