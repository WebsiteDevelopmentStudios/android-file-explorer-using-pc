import subprocess
import os
import sys

def get_binary_path(binary_name):
    """Locates the bundled executable inside the PyInstaller temporary directory or local folder."""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_path, binary_name)
    return full_path if os.path.exists(full_path) else binary_name

def run_command(binary, args):
    """Helper to safely run adb or fastboot commands."""
    exe_path = get_binary_path(binary)
    try:
        result = subprocess.run([exe_path] + args, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[-] Error executing {binary}: {e.stderr.strip()}")
        return None
    except FileNotFoundError:
        print(f"[-] Error: {binary} not found.")
        return None

def check_fastboot_devices():
    """Checks if a device is connected in Bootloader/Fastboot mode."""
    print("[*] Checking for devices in Fastboot mode...")
    output = run_command("fastboot.exe", ["devices"])
    if output:
        print(f"[+] Fastboot device detected:\n{output}")
        return True
    print("[-] No devices found in Fastboot mode.")
    return False

def flash_boot_partition(local_img_name):
    """Flashes a custom boot image to the device via Fastboot."""
    if not os.path.exists(local_img_name):
        print(f"[-] Error: Local file '{local_img_name}' not found on your PC.")
        return
        
    print(f"[!] WARNING: You are about to flash {local_img_name} to the BOOT partition.")
    confirm = input("Type 'CONFIRM' to proceed: ")
    if confirm == "CONFIRM":
        print("[*] Flashing boot partition... Do not unplug your device.")
        output = run_command("fastboot.exe", ["flash", "boot", local_img_name])
        if output is not None:
            print("[+] Boot partition successfully flashed!")
    else:
        print("[-] Operation canceled.")

def main():
    while True:
        print("\n--- Portable ADB & Fastboot Manager ---")
        print("1. Reboot device from ADB into Bootloader (Fastboot)")
        print("2. Check for connected Fastboot devices")
        print("3. Flash a custom boot.img (Must be in Fastboot mode)")
        print("4. Reboot device from Fastboot back to Android System")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ")
        
        if choice == '1':
            print("[*] Sending reboot command via ADB...")
            run_command("adb.exe", ["reboot", "bootloader"])
            print("[+] Check your device screen. It should be switching modes.")
        elif choice == '2':
            check_fastboot_devices()
        elif choice == '3':
            img_file = input("Enter the filename of the image on your PC/Card (e.g., patched_boot.img): ")
            flash_boot_partition(img_file)
        elif choice == '4':
            print("[*] Rebooting device normally...")
            run_command("fastboot.exe", ["reboot"])
        elif choice == '5':
            break

if __name__ == "__main__":
    main()
