import subprocess
import os
import sys
import time

# --- NEON PURPLE COLOR CODES ---
C_PURPLE = "\033[38;2;186;85;211m"   # Medium Orchid Purple
C_NEON = "\033[38;2;224;102;255m"     # Bright Neon Purple
C_CYAN = "\033[38;2;0;238;238m"       # Cyan accents for highlights
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
        time.sleep(0.015)  # Fast, punchy load speed
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
        print(f"{C_CYAN}[-] System Error: {e.stderr.strip()}{C_RESET}")
        return None
    except FileNotFoundError:
        print(f"{C_CYAN}[-] Binary Missing: {binary} not found.{C_RESET}")
        return None

def check_devices():
    """Displays real-time hardware sync layout."""
    clear_screen()
    neon_banner("HARDWARE SYNC MATRIX")
    adb_out = run_command("adb.exe", ["devices"])
    fastboot_out = run_command("fastboot.exe", ["devices"])
    
    print(f"\n{C_PURPLE}[ ADB CHANNEL ]{C_RESET}")
    if adb_out and len(adb_out.split('\n')) > 1:
        print(f"{C_WHITE}{adb_out}{C_RESET}")
    else:
        print(f" ╰─ {C_CYAN}NO ACTIVE PHONE IN DEBUG MODE{C_RESET}")
        
    print(f"\n{C_PURPLE}[ FASTBOOT CHANNEL ]{C_RESET}")
    if fastboot_out:
        print(f"{C_WHITE}{fastboot_out}{C_RESET}")
    else:
        print(f" ╰─ {C_CYAN}NO ACTIVE PHONE IN BOOTLOADER MODE{C_RESET}")
    
    input(f"\n{C_NEON}Press Enter to return to Nexus...{C_RESET}")

# ================= NEON PURPLE FILE EXPLORER =================
def custom_file_viewer():
    """An interactive, styled interface to navigate and modify device internal storage."""
    current_dir = "/sdcard/"
    
    while True:
        clear_screen()
        neon_banner("CYBER FILE EXPLORER v2.0")
        
        # Feature: Live Storage Capacity Metric Widget
        storage_info = run_command("adb.exe", ["shell", "df -h /sdcard"])
        if storage_info and len(storage_info.split('\n')) > 1:
            stats = storage_info.split('\n')[1].split()
            if len(stats) >= 5:
                print(f"{C_CYAN}STORAGE METRICS: Total: {stats[1]} | Used: {stats[2]} | Free: {stats[3]} ({stats[4]} utilized){C_RESET}")
        
        print(f"{C_PURPLE}VIRTUAL PATH ➔ {C_WHITE}{current_dir}{C_RESET}")
        print(f"{C_PURPLE}-" * 60 + f"{C_RESET}")
        
        scan_animation()
        
        raw_list = run_command("adb.exe", ["shell", f"ls -pa {current_dir}"])
        if raw_list is None:
            input(f"{C_CYAN}[!] Error communicating with core interface. Press Enter...{C_RESET}")
            break
            
        items = [line for line in raw_list.split('\n') if line.strip() and line != './']
        
        # Display folder index rows with alternating neon tints
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
            run_command("adb.exe", ["shell", f"mkdir -p {current_dir}{new_folder}"])
            continue
            
        try:
            if choice.startswith('dl ') or choice.startswith('del '):
                cmd, idx_str = choice.split(' ', 1)
                idx = int(idx_str) - 1
                selected_item = items[idx]
                target_path = os.path.normpath(os.path.join(current_dir, selected_item)).replace('\\', '/')
                
                if cmd == 'dl':
                    print(f"{C_CYAN}[*] Downloading package to memory card root...{C_RESET}")
                    run_command("adb.exe", ["pull", target_path, "."])
                elif cmd == 'del':
                    confirm = input(f"{C_CYAN}[!] SAFEGUARD: Erase {selected_item}? (y/n): {C_RESET}")
                    if confirm.lower() == 'y':
                        run_command("adb.exe", ["shell", f"rm -rf \"{target_path}\""])
                continue
                
            elif choice == 'up':
                local_file = input(f"{C_CYAN}Enter absolute PC/Card filename to push: {C_RESET}")
                if os.path.exists(local_file):
                    print(f"{C_CYAN}[*] Uploading stream to device environment...{C_RESET}")
                    run_command("adb.exe", ["push", local_file, current_dir])
                else:
                    print(f"{C_CYAN}[-] File node could not be matched local side.{C_RESET}")
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
            pass # Invalid options safely refresh without locking up execution loop

def main():
    # Make sure modern Windows Console environment interprets custom color streams correctly
    os.system('') 
    
    while True:
        clear_screen()
        neon_banner("NEXUS DEVICE CONTROL HUBA")
        print(f"  {C_PURPLE}[1]{C_NEON} Scan Core Matrix Connections (ADB / Fastboot)")
        print(f"  {C_PURPLE}[2]{C_NEON} Launch Interactive Custom Neon File Explorer")
        print(f"  {C_PURPLE}[3]{C_NEON} Warm-Reboot Target Into Bootloader (Fastboot)")
        print(f"  {C_PURPLE}[4]{C_NEON} Flash Modified Image Component to 'boot' block")
        print(f"  {C_PURPLE}[5]{C_NEON} Escape Fastboot State to Operating System")
        print(f"  {C_PURPLE}[6]{C_NEON} Terminate Active Session")
        print(f"{C_PURPLE}-" * 60 + f"{C_RESET}")
        
        choice = input(f"{C_NEON}Select Terminal Route (1-6): {C_RESET}")
        
        if choice == '1':
            check_devices()
        elif choice == '2':
            custom_file_viewer()
        elif choice == '3':
            clear_screen()
            print(f"{C_CYAN}[*] Injecting hardware bootloader interrupt...{C_RESET}")
            run_command("adb.exe", ["reboot", "bootloader"])
            time.sleep(2)
        elif choice == '4':
            clear_screen()
            neon_banner("IMAGE INJECTION SEGMENT")
            img_file = input(f"{C_CYAN}Target filename located on memory card (e.g., patched_boot.img): {C_RESET}")
            if os.path.exists(img_file):
                print(f"{C_CYAN}[!] Preparing partition overrides...{C_RESET}")
                confirm = input("Type 'CONFIRM' to patch partition block: ")
                if confirm == "CONFIRM":
                    run_command("fastboot.exe", ["flash", "boot", img_file])
            else:
                print(f"{C_CYAN}[-] Target image data path empty.{C_RESET}")
                time.sleep(2)
        elif choice == '5':
            clear_screen()
            print(f"{C_CYAN}[*] Dropping system bypass loops, rebooting normal layout...{C_RESET}")
            run_command("fastboot.exe", ["reboot"])
            time.sleep(2)
        elif choice == '6':
            clear_screen()
            print(f"{C_NEON}Session safely terminated. Safe removal authorized.{C_RESET}")
            break

if __name__ == "__main__":
    main()
