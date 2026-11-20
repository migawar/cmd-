import platform
import subprocess
import re


def get_wifi_status():
    os_name = platform.system()
    print(f"Operating System detected: {os_name}")
    print("-" * 40)

    try:
        if os_name == "Windows":
            # Use netsh to retrieve Wi-Fi interface details
            output = subprocess.check_output(
                ["netsh", "wlan", "show", "interfaces"],
                encoding="utf-8",
                errors="ignore"
            )

            # Match key fields (works for both EN and NL Windows versions)
            state = re.search(r"(?:State|Status)\s*:\s*(.+)", output)
            ssid = re.search(r"\bSSID\s*:\s*(.+)", output)
            signal = re.search(r"(?:Signal|Signaal)\s*:\s*(.+)", output)

            if state and ("connected" in state.group(1).lower() or "verbonden" in state.group(1).lower()):
                print("Status          : Connected")
                print(f"Network (SSID)  : {ssid.group(1).strip() if ssid else 'Unknown'}")
                print(f"Signal Strength : {signal.group(1).strip() if signal else 'Unknown'}")
            else:
                print("Status          : Not connected to Wi-Fi")

        elif os_name == "Linux":
            # Use nmcli (NetworkManager)
            output = subprocess.check_output(
                ["nmcli", "-t", "-f", "ACTIVE,SSID,SIGNAL", "dev", "wifi"],
                encoding="utf-8"
            )
            connected = False
            for line in output.splitlines():
                if line.startswith("yes:") or line.startswith("ja:"):
                    parts = line.split(":")
                    print("Status          : Connected")
                    print(f"Network (SSID)  : {parts[1]}")
                    print(f"Signal Strength : {parts[2]}%")
                    connected = True
                    break
            if not connected:
                print("Status          : Not connected to Wi-Fi")

        elif os_name == "Darwin":  # macOS
            # Use networksetup on macOS
            output = subprocess.check_output(
                ["networksetup", "-getairportnetwork", "en0"],
                encoding="utf-8"
            )
            if "Current Wi-Fi Network:" in output:
                ssid = output.split(":")[1].strip()
                print("Status          : Connected")
                print(f"Network (SSID)  : {ssid}")
            else:
                print("Status          : Not connected to Wi-Fi")

        else:
            print(f"Operating system '{os_name}' is not supported.")

    except FileNotFoundError:
        print("Error: Required system Wi-Fi tool not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    get_wifi_status()
