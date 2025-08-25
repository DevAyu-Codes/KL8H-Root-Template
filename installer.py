import os
import sys
import subprocess
import time
import shutil

# --- Configuration ---
# Set the kernel/boot version once here
BOOT_VERSION = "5.15.188"
# Define the folder where your .img files are located
IMAGES_FOLDER = "images"
# -------------------

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def animated_dots(text):
    """Prints a message followed by animated dots."""
    print(f">> {text}", end="", flush=True)
    for _ in range(3):
        time.sleep(0.8)
        print(".", end="", flush=True)
    print()

def run_command(command_list):
    """Runs an external command and hides its output."""
    try:
        # Before running, check if the image file exists
        for item in command_list:
            if isinstance(item, str) and item.endswith('.img'):
                if not os.path.exists(item):
                    print(f"\n[ERROR] Image file not found: {item}")
                    print(f"Please make sure all necessary .img files are in the '{IMAGES_FOLDER}' folder.")
                    return False
        
        subprocess.run(command_list, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"\nError executing command: {' '.join(command_list)}")
        print(f"Error details: {e}")
        return False

def check_dependencies():
    """Checks if adb and fastboot are available."""
    print(">> Checking for ADB and Fastboot dependencies...")
    # shutil.which checks the system's PATH for an executable
    adb_path = shutil.which("adb")
    fastboot_path = shutil.which("fastboot")

    # On Windows, also check for a local platform-tools directory
    if os.name == 'nt':
        local_adb = os.path.join("platform-tools", "adb.exe")
        local_fastboot = os.path.join("platform-tools", "fastboot.exe")
        if os.path.exists(local_adb):
            adb_path = local_adb
        if os.path.exists(local_fastboot):
            fastboot_path = local_fastboot

    if not adb_path or not fastboot_path:
        print("\n[ERROR] ADB or Fastboot not found!")
        print("Please run the appropriate setup script for your OS first:")
        print("- On Windows: run setup.bat")
        print("- On Linux:   run setup.sh")
        input("\nPress Enter to exit...")
        sys.exit(1)
        
    print(">> Dependencies found successfully.")
    time.sleep(1)
    return adb_path, fastboot_path

def main():
    """Main function to run the installer."""
    clear_screen()
    adb, fastboot = check_dependencies()

    # Determine if sudo is needed for fastboot on Linux
    fastboot_cmd = [fastboot]
    if sys.platform.startswith('linux'):
        # Check if we can run fastboot without sudo. If not, prepend sudo.
        try:
            subprocess.run([fastboot, "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except (subprocess.CalledProcessError, PermissionError):
            print(">> Fastboot requires root privileges. Using 'sudo'.")
            fastboot_cmd.insert(0, "sudo")

    # --- Header ---
    clear_screen()
    print("====================================")
    print("   Apatch/Magisk/KSU Next Installer   ")
    print("====================================")
    print("Device: Tecno Spark 30C (KL8H)")
    print("Developer: Ayu Kashyap - @dev_ayu")
    print("\n>> Allow the ADB popup on your phone if prompted.")
    input("Press Enter to continue...")

    # --- Reboot to Fastboot ---
    print()
    animated_dots("Rebooting to Fastboot Mode")
    run_command([adb, "reboot", "fastboot"])
    time.sleep(5) # Give the device time to enter fastboot mode

    # --- Main Menu Loop ---
    while True:
        print("\nSelect boot method:")
        print("[1] Magisk")
        print("[2] Apatch")
        print("[3] KSU Next (KernelSU Next)")
        print("[4] Unroot (Stock Boot)")
        choice = input("Enter choice (1/2/3/4): ")

        if choice in ["1", "2", "3", "4"]:
            break
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

    # --- Flashing Logic ---
    if choice == "1": # Magisk
        animated_dots("Installing Magisk")
        boot_img = os.path.join(IMAGES_FOLDER, f"boot_{BOOT_VERSION}.img")
        init_boot_img = os.path.join(IMAGES_FOLDER, "init_boot_a_magisk.img")
        run_command(fastboot_cmd + ["flash", "boot", boot_img])
        run_command(fastboot_cmd + ["reboot", "bootloader"])
        run_command(fastboot_cmd + ["flash", "init_boot_a", init_boot_img])
        print(">> Magisk installed successfully.")

    elif choice == "2": # Apatch
        animated_dots("Installing Apatch")
        boot_img = os.path.join(IMAGES_FOLDER, f"boot_{BOOT_VERSION}_apatch.img")
        init_boot_img = os.path.join(IMAGES_FOLDER, "init_boot_a.img")
        run_command(fastboot_cmd + ["flash", "boot", boot_img])
        run_command(fastboot_cmd + ["reboot", "bootloader"])
        run_command(fastboot_cmd + ["flash", "init_boot_a", init_boot_img])
        print(">> Apatch installed successfully.")

    elif choice == "3": # KSU
        animated_dots("Installing KSU Next")
        boot_img = os.path.join(IMAGES_FOLDER, f"boot_{BOOT_VERSION}.img")
        init_boot_img = os.path.join(IMAGES_FOLDER, "init_boot_a_ksu.img")
        run_command(fastboot_cmd + ["flash", "boot", boot_img])
        run_command(fastboot_cmd + ["reboot", "bootloader"])
        run_command(fastboot_cmd + ["flash", "init_boot_a", init_boot_img])
        print(">> KSU Next installed successfully.")

    elif choice == "4": # Unroot
        animated_dots("Flashing stock boot (Unroot)")
        boot_img = os.path.join(IMAGES_FOLDER, f"boot_{BOOT_VERSION}.img")
        init_boot_img = os.path.join(IMAGES_FOLDER, "init_boot_a.img")
        run_command(fastboot_cmd + ["flash", "boot", boot_img])
        run_command(fastboot_cmd + ["reboot", "bootloader"])
        run_command(fastboot_cmd + ["flash", "init_boot_a", init_boot_img])
        print(">> Stock boot flashed (Unrooted).")

    # --- Final Reboot ---
    print()
    animated_dots("Rebooting device now")
    run_command(fastboot_cmd + ["reboot"])

    print("\nAll done!")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()