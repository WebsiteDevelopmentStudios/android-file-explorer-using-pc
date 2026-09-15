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

def custom_file_viewer():
    path = "/sdcard/"
    while True:
        ui("CYBER FILE EXPLORER v2.2")
        print(f"{C_P}VIRTUAL PATH ➔ {C_W}{path}\n" + f"{C_P}-" * 60 + f"\n{C_C}[SYSTEM] Mapping bridge topology...{C_X}")
        for i in range(31):
            time.sleep(0.005)
            sys.stdout.write(f"\r{C_P}[ {'█'*i + '░'*(30-i)} ] {C_N}{int((i/30)*100)}% COMPLETED{C_X}")
        
        raw = run_cmd("adb.exe", ["shell", f"ls -pa {path}"])
        if raw is None:
            input(f"\n{C_R}[!] Bridge link failed. Press Enter...{C_X}"); break
        items = [l for l in raw.split('\n') if l.strip() and l != './']
        
        print("\n")
        for idx, item in enumerate(items, 1):
            print(f"  {C_P}[{idx:02d}]{C_N if item.endswith('/') else C_W} {item}{C_X}")
        print(f"{C_P}-" * 60 + f"\n{C_C}SHORTCUTS:{C_X} [num] Dive | '..' Back | 'dl [num]' Pull | 'del [num]' Wipe | 'up' Push | 'exit' Close")
        
        cmd = input(f"\n{C_N}NEXUS-SHELL> {C_X}").strip()
        if cmd.lower() == 'exit': break
        elif cmd == '..': path = (os.path.dirname(path.rstrip('/')) + '/').replace('//', '/')
        try:
            if cmd.startswith(('dl ', 'del ')):
                action, idx = cmd.split(' ')
                target = os.path.normpath(os.path.join(path, items[int(idx)-1])).replace('\\', '/')
                if action == 'dl': run_cmd("adb.exe", ["pull", f"\"{target}\"", "."])
                elif action == 'del' and input(f"{C_R}Erase {items[int(idx)-1]}? (y/n): {C_X}").lower() == 'y':
                    run_cmd("adb.exe", ["shell", f"rm -rf \"{target}\""])
            elif cmd == 'up':
                f = input(f"{C_C}Local file name to push: {C_X}")
                if os.path.exists(f): run_cmd("adb.exe", ["push", f"\"{f}\"", f"\"{path}\""])
            else:
                sel = items[int(cmd)-1]
                if sel.endswith('/'): path = os.path.normpath(os.path.join(path, sel)).replace('\\', '/') + '/'
                else:
                    ui(f"VIEWING: {sel}")
                    cat_cmd = 'cat "' + path + sel + '"'
                    file_data = run_cmd('adb.exe', ['shell', cat_cmd]) or '[Binary Data]'
                    print(f"{C_W}{file_data}{C_X}\n" + f"{C_P}=" * 60)
                    input(f"\n{C_N}Press Enter to return...{C_X}")
        except: pass

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
        if ch == '1' and adb_on: custom_file_viewer()
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
