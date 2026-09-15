import subprocess
import os
import sys
import time

# --- NEON PURPLE COLOR CODES ---
C_PURPLE = "\033[38;2;186;85;211m"   # Medium Orchid Purple
C_NEON = "\033[38;2;224;102;255m"     # Bright Neon Purple
C_CYAN = "\033[38;2;0;238;238m"       # Cyan accents for highlights
C_RED = "\033[38;2;255;64;64m"        # Red accent for warnings
C_WHITE = "\033[97m"
C_RESET = "\033[0m"

def clear_screen():
    """Clears the console for a fluid, app-like transition effect."""
    os.system('cls' if os.name == 'nt' else 'clear')

def neon_banner(text):
    """Prints a styled neon header banner."""
    print(f"{C_PURPLE}=" * 60)
    print(f" {C_NEON}{text.center(58)} ")
    print(f"{C_PURPLE}=" * 60 + f"{C_RESET}")

def scan_animation():
    """Plays a cool cybernetic scanning effect before rendering files."""
    print(f"\n{C_CYAN}[SYSTEM] Initializing secure data bridge...{C_RESET}")
    bar_width = 30
    for i in range(bar_width + 1):
        time.sleep(0.01)  
        progress = "█" * i + "░" * (bar_width - i)
        percent = int((i / bar_width) * 100)
        sys.stdout.write(f"\r{C_PURPLE}[ {progress} ] {C_NEON}{percent}% COMPLETED{C_RESET}")
        sys.stdout.flush()
    print("\n")

def get_binary_path(binary_name):
    """Locates bundled adb/fastboot binaries inside PyInstaller packages."""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_path, binary_name)
    return full_path if os.path.exists(full_path) else binary_name

def run_command(binary, args):
    """Executes backend system commands via ADB or Fastboot."""
    exe_path = get_binary_path(binary)
    try:
        result = subprocess.run([exe_path] + args, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return None
    except FileNotFoundError:
        return None

def scan_usb_hardware():
    """Scans and filters active USB paths for device telemetry mapping."""
    adb_out = run_command("adb.exe", ["devices"])
    fastboot_out = run_command("fastboot.exe", ["devices"])
    
    adb_connected = False
    fastboot_connected = False
    
    if adb_out and len(adb_out.split('\n')) > 1:
        # Check if the output actually contains a device ID line
        lines = adb_out.split('\n')[1:]
        if any(line.strip() and 'device' in line for line in lines):
            adb_connected = True
            
    if fastboot_out and fastboot_out.strip():
        fastboot_connected = True
        
    return adb_connected, fastboot_connected

# ================= NEON PURPLE FILE EXPLORER =================
def custom_file_viewer():
    """An interactive, styled interface to navigate and modify device internal storage."""
    current_dir = "/sdcard/"
    
    while True:
        clear_screen()
        neon_banner("CYBER FILE EXPLORER v2.1")
        
        print(f"{C_PURPLE}VIRTUAL PATH ➔ {C_WHITE}{current_dir}{C_RESET}")
        print(f"{C_PURPLE}-" * 60 + f"{C_RESET}")
        
        scan_animation()
        
        raw_list = run_command("adb.exe", ["shell", f"ls -pa {current_dir}"])
        if raw_list is None:
            input(f"{C_RED}[!] Error communicating with file architecture. Ensure USB Debugging is allowed. Press Enter...{C_RESET}")
            break
            
        items = [line for line in raw_list.split('\n') if line.strip() and line != './']
        
        for idx, item in enumerate(items, 1):
            color = C_NEON if item.endswith('/') else C_WHITE
            print(f"  {C_PURPLE}[{idx:02d}]{color} {item}{C_RESET}")
            
        print(f"{C_PURPLE}-" * 60 + f"{C_RESET}")
        print(f"{C_CYAN}CONTROLS:{C_RESET} [num] Dive In | '..' Back | 'dl [num]' Fetch | 'del [num]' Wipe")
        print(f"          'up' Push Payload | 'mkdir [name]' Forge Folder | 'exit' Close Explorer")
        
        choice = input(f"\n{C_NEON}NEXUS-SHELL Custom-File-Explorer> {C_RESET}").strip()
        
        if choice.lower() == 'exit':
            break
        elif choice == '..':
            if current_dir != "/":
                current_dir = os.path.dirname(current_dir.rstrip('/')) + '/'
                if current_dir == '//': current_dir = '/'
            continue
        elif choice.startswith('mkdir '):
            new_folder = choice.split(' ', 1)[1]
            run_command("adb.exe", ["shell", f"mkdir -p \"{current_dir}{new_folder}\""])
            continue
            
        try:
            if choice.startswith('dl ') or choice.startswith('del '):
                cmd, idx_str = choice.split(' ', 1)
                idx = int(idx_str) - 1
                selected_item = items[idx]
                target_path = os.path.normpath(os.path.join(current_dir, selected_item)).replace('\\', '/')
                
                if cmd == 'dl':
                    print(f"{C_CYAN}[*] Downloading package to memory card root...{C_RESET}")
                    run_command("adb.exe", ["pull", f"\"{target_path}\"", "."])
                elif cmd == 'del':
                    confirm = input(f"{C_RED}[!] SAFEGUARD: Erase {selected_item}? (y/n): {C_RESET}")
                    if confirm.lower() == 'y':
                        run_command("adb.exe", ["shell", f"rm -rf \"{target_path}\""])
                continue
                
            elif choice == 'up':
                local_file = input(f"{C_CYAN}Enter absolute PC/Card filename to push: {C_RESET}")
                if os.path.exists(local_file):
                    print(f"{C_CYAN}[*] Uploading stream to device environment...{C_RESET}")
                    run_command("adb.exe", ["push", f"\"{local_file}\"", f"\"{current_dir}\""])
                else:
                    print(f"{C_RED}[-] File node could not be matched local side.{C_RESET}")
                    time.sleep(1.5)
                continue
                
            else:
                idx = int(choice) - 1
                selected_item = items[idx]
                
                if selected_item.endswith('/'):
                    current_dir = os.path.normpath(os.path.join(current_dir, selected_item)).replace('\\', '/') + '/'
                else:
                    clear_screen()
                    neon_banner(f"FILE DATA: {selected_item}")
                    file_content = run_command("adb.exe", ["shell", f"cat \"{current_dir}{selected_item}\""])
                    print(f"{C_WHITE}{file_content if file_content else '[Empty or Untranslatable Binary Core]'}{C_RESET}")
                    print(f"{C_PURPLE}=" * 60 + f"{C_RESET}")
                    input(f"\n{C_NEON}Press Enter to reset visual environment...{C_RESET}")
                    
        except (ValueError, IndexError):
            pass

def main():
    os.system('') # Initialize ANSI colors for legacy Windows Command Prompts
    
    while True:
        clear_screen()
        neon_banner("NEXUS DEVICE CONTROL HUB")
        
        # Real-time Auto USB Scanner Engine
        adb_active, fastboot_active = scan_usb_hardware()
        
        print(f"{C_PURPLE}[ HARDWARE TELEMETRY ]{C_RESET}")
        if adb_active:
            print(f" ╰─ LINK ACTIVE: {C_NEON}Android Device Detected (ADB Mode){C_RESET}")
            fb_check = run_command("adb.exe", ["shell", "getprop ro.boot.flash.locked"])
            if fb_check is None:
                print(f" ╰─ DEVICE CAPABILITY: {C_RED}[!] FASTBOOT PROTOCOL UNSUPPORTED / LOCKED BY OEM (File Browsing Still Accessible){C_RESET}")
        elif fastboot_active:
            print(f" ╰─ LINK ACTIVE: {C_CYAN}Android Device Detected (Fastboot Mode){C_RESET}")
        else:
            print(f" ╰─ LINK ACTIVE: {C_WHITE}Scanning... No USB Debugging Target Connected.{C_RESET}")
            
        print(f"\n{C_PURPLE}=" * 60 + f"{C_RESET}")
        print(f"  {C_NEON}1.{C_WHITE} Launch Interactive Custom Neon File Explorer")
        print(f"  {C_NEON}2.{C_WHITE} Warm-Reboot Target Into Bootloader (Fastboot)")
        print(f"  {C_NEON}3.{C_WHITE} Flash Modified Image Component to 'boot' block")
        print(f"  {C_NEON}4.{C_WHITE} Escape Fastboot State to Operating System")
        print(f"  {C_NEON}5.{C_WHITE} Terminate Active Session & Kill Server")
        print(f"{C_PURPLE}-" * 60 + f"{C_RESET}")
        
       choice = input(f"{C_NEON}Select Terminal Route (1-5): {C_RESET}").strip()
        
        if choice == '1':
            if adb_active:
                custom_file_viewer()
            else:
                input(f"\n{C_RED}[!] Error: File explorer requires an active ADB USB connection. Press Enter...{C_RESET}")
        elif choice == '2':
            if adb_active:
                clear_screen()
                print(f"{C_CYAN}[*] Injecting hardware bootloader interrupt...{C_RESET}")
                run_command("adb.exe", ["reboot", "bootloader"])
                time.sleep(2)
            else:
                input(f"\n{C_RED}[!] Error: No active ADB device found to send reboot command. Press Enter...{C_RESET}")
        elif choice == '3':
            clear_screen()
            neon_banner("IMAGE INJECTION SEGMENT")
            img_file = input(f"{C_CYAN}Target filename located on memory card (e.g., patched_boot.img): {C_RESET}")
            if os.path.exists(img_file):
                print(f"{C_CYAN}[!] Preparing partition overrides...{C_RESET}")
                confirm = input("Type 'CONFIRM' to patch partition block: ")
                if confirm == "CONFIRM":
                    run_command("fastboot.exe", ["flash", "boot", img_file])
            else:
                print(f"{C_RED}[-] Target image data path empty.{C_RESET}")
                time.sleep(2)
        elif choice == '4':
            clear_screen()
            print(f"{C_CYAN}[*] Dropping system bypass loops, rebooting normal layout...{C_RESET}")
            run_command("fastboot.exe", ["reboot"])
            time.sleep(2)
        elif choice == '5':
            clear_screen()
            print(f"{C_CYAN}[*] Shutting down background ADB server subsystems...{C_RESET}")
            run_command("adb.exe", ["kill-server"])
            print(f"{C_NEON}Session safely terminated. Safe removal authorized.{C_RESET}")
            break

if __name__ == "__main__":
    main()
