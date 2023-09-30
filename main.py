import subprocess
import platform
import requests

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

if __name__ == "__main__":
    # Welcome Message
    print("\033[1;33mLoading Script...\033[0m")

    # Check and Enable Wi-Fi
    check_and_enable_wifi()

    # Check Internet Connectivity
    timeout_value = 10
    if is_cnx_active(timeout_value):
        print("\033[0;32mInternet accessible...\033[0m")
    else:
        print("\033[0;31mInternet not accessible...\033[0m")
