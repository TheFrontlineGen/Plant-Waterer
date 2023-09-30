import requests
import os
import subprocess
import platform

print("\033[1;33mLoading Script Updater...\033[0m")

# Check and Enable Wi-Fi
def check_and_enable_wifi():
    system = platform.system()

    if system == 'Linux':
        # Check if Wi-Fi is enabled on Linux
        result = subprocess.run(['nmcli', 'radio', 'wifi'], capture_output=True, text=True)
        if 'enabled' not in result.stdout.lower():
            # Enable Wi-Fi on Linux
            subprocess.run(['nmcli', 'radio', 'wifi', 'on'])
            print("\033[0;32mWi-Fi enabled...\033[0m")
        else:
            print("\033[0;32mWi-Fi is enabled...\033[0m")

    elif system == 'Windows':
        # Check if Wi-Fi is enabled on Windows
        result = subprocess.run(['netsh', 'interface', 'show', 'interface'], capture_output=True, text=True)
        if 'Wireless Network Connection' in result.stdout and 'enabled' not in result.stdout:
            # Enable Wi-Fi on Windows
            subprocess.run(['netsh', 'interface', 'set', 'interface', 'name="Wireless Network Connection"', 'admin=enabled'])
            print("\033[0;32mWi-Fi enabled...\033[0m")
        else:
            print("\033[0;32mWi-Fi is enabled...\033[0m")

    else:
        print("Unsupported operating system.")

# Check Internet Connectivity
def is_cnx_active(timeout):
    sites = ["https://www.google.com", "https://www.gstatic.com", "https://www.microsoft.com", "https://vercel.com", "https://apple.com", "https://cloudflare.com", "https://amazon.com", "https://spotify.com"]
    for site in sites:
        try:
            requests.head(site, timeout=timeout)
            return True
        except requests.ConnectionError:
            continue
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            continue
    return False

# Define the URL to the raw file on GitHub and the local file path
github_url = "https://raw.githubusercontent.com/TheFrontlineGen/Plant-Waterer/main/main.py"
local_file_path = "main.py"

# Check and enable Wi-Fi
check_and_enable_wifi()

# Check Internet connectivity
if is_cnx_active(timeout=5):
    print("\033[0;32mInternet accessible...\033[0m")
    # Fetch the content of the remote file
    response = requests.get(github_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        remote_content = response.text

        # Read the content of the local file
        with open(local_file_path, 'r') as local_file:
            local_content = local_file.read()

        # Compare the remote and local content
        if remote_content != local_content:
            # If they differ, save the remote content to the local file
            with open(local_file_path, 'w') as local_file:
                local_file.write(remote_content)
            
            print("Successfully updated main.py from GitHub.")
        else:
            print("\033[0;32mScript is up-to-date...\033[0m")
    else:
        print("Failed to fetch the remote file from GitHub.")

# Run the local main.py
try:
    subprocess.run(["python", local_file_path], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running main.py: {e}")
