import subprocess, os, sys, time

# --- CORES & COLORS ---
C_P, C_N, C_C, C_R, C_W, C_X = "\033[38;2;186;85;211m", "\033[38;2;224;102;255m", "\033[38;2;0;238;238m", "\033[38;2;255;64;64m", "\033[97m", "\033[0m"

def ui(banner_text=None, clear=True):
    if clear: os.system('cls' if os.name == 'nt' else 'clear')
    if banner_text:
        print(f"{C_P}=" * 60 + f"\n {C_N}{banner_text.center(58)} \n" + f"{C_P}=" * 60 + f"{C_X}")

def run_cmd(bin_name, args):
    b_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    exe = os.path.join(b_path, bin_name)
    try: return subprocess.run([exe if os.path.exists(exe) else bin_name] + args, capture_output=True, text=True, check=True).stdout.strip()
    except: return None

def scan_usb():
    adb, fb = run_cmd("adb.exe", ["devices"]), run_cmd("fastboot.exe", ["devices"])
    is_adb = any(l.strip() and 'device' in l for l in adb.split('\n')[1:]) if adb and len(adb.split('\n')) > 1 else False
    return is_adb, bool(fb and fb.strip())

def launch_visual_explorer():
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    xplorer_bin = os.path.join(base_path, "xplorer.exe")
    target_workspace = r"E:\android_manager_tool\tablet_sync"
    
    ui("SYNCING LIVE WORKSPACE")
    if not os.path.exists(target_workspace):
        os.makedirs(target_workspace)
        
    print(f"{C_C}[SYSTEM] Initializing background file channel bridges...{C_X}")
    
    # ⚡ OPTIMIZATION: Pull only high-volume folders directly to avoid system cache file lag
    # Using Popen launches these transfers quietly in the background without locking your screen!
    b_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    adb_exe = os.path.join(b_path, "adb.exe")
    adb_path = adb_exe if os.path.exists(adb_exe) else "adb.exe"
    
    subprocess.Popen([adb_path, "pull", "/sdcard/Download", target_workspace], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.Popen([adb_path, "pull", "/sdcard/DCIM", target_workspace], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.Popen([adb_path, "pull", "/sdcard/Documents", target_workspace], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.Popen([adb_path, "pull", "/sdcard/Pictures", target_workspace], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print(f"{C_N}[SYSTEM] Spawning Neon Purple GUI Environment instantly...{C_X}")
    time.sleep(1)

    if os.path.exists(xplorer_bin):
        subprocess.Popen([xplorer_bin, target_workspace])
    else:
        print(f"{C_R}[!] Internal visual package missing. Using system fallback...{C_X}")
        time.sleep(1.5)
        os.system(f"start explorer {target_workspace}")

def main():
    os.system('')
    while True:
        ui("NEXUS DEVICE CONTROL HUB")
        adb_on, fb_on = scan_usb()
        print(f"{C_P}[ HARDWARE TELEMETRY ]{C_X}")
        if adb_on:
            print(f" ╰─ LINK ACTIVE: {C_N}Target Connected (ADB Mode){C_X}")
            if run_cmd("adb.exe", ["shell", "getprop ro.boot.flash.locked"]) is None:
                print(f" ╰─ SECURE ENVIRONMENT: {C_R}[!] FASTBOOT RESTRICTED BY OEM LAYER{C_X}")
        elif fb_on: print(f" ╰─ LINK ACTIVE: {C_C}Target Connected (Fastboot Mode){C_X}")
        else: print(f" ╰─ LINK ACTIVE: {C_W}Scanning... Awaiting USB Target Link.{C_X}")
        
        print(f"\n{C_P}=" * 60 + f"\n  {C_N}1.{C_W} Launch Interactive Neon File Explorer\n  {C_N}2.{C_W} Warm-Reboot Target Into Fastboot\n  {C_N}3.{C_W} Inject Custom Image Payload to 'boot' partition\n  {C_N}4.{C_W} Force Warm-Reboot Target back to System\n  {C_N}5.{C_W} Terminate Matrix Core & Kill Server\n" + f"{C_P}-" * 60)
        
        ch = input(f"{C_N}Route selection (1-5): {C_X}").strip()
        if ch == '1' and adb_on: launch_visual_explorer()
        elif ch == '2' and adb_on: ui("INJECTING INTERRUPT"); run_cmd("adb.exe", ["reboot", "bootloader"]); time.sleep(2)
        elif ch == '3':
            ui("IMAGE INJECTION SEGMENT")
            img = input(f"{C_C}Card raw image filename (e.g., patched_boot.img): {C_X}")
            if os.path.exists(img) and input("Type 'CONFIRM' to flash block: ") == "CONFIRM": run_cmd("fastboot.exe", ["flash", "boot", img])
        elif ch == '4': ui("REBOOTING SYSTEM"); run_cmd("fastboot.exe", ["reboot"]); time.sleep(2)
        elif ch == '5': ui("TERMINATING SERVER"); run_cmd("adb.exe", ["kill-server"]); break
        elif ch in ['1', '2']: input(f"\n{C_R}[!] Error: Active ADB connection required. Press Enter...{C_X}")

if __name__ == "__main__":
    main()
