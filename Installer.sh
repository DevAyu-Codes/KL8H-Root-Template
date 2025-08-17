#!/bin/bash
# ============================
# Apatch/Magisk Installer (Linux)
# ============================

BOOTVER="5.15.188"

# ============================
# Function: Animated Dots
# ============================
sleep_dots() {
    for i in 1 2 3; do
        echo -n "."
        sleep 1
    done
    echo
}

echo "============================="
echo "     Apatch/Magisk Installer "
echo "============================="
echo "Device: Tecno Spark 30C (KL8H)"
echo "Developer: Ayu Kashyap - @dev_ayu"
echo
echo ">> Allow the ADB popup on your phone if prompted."
read -rp "Press Enter to continue..."

echo
echo -n ">> Rebooting to Fastboot Mode..."
adb reboot fastboot >/dev/null 2>&1
sleep_dots

# ============================
# Ask for root/unroot choice
# ============================
while true; do
    echo
    echo "Select boot method:"
    echo "1) Magisk"
    echo "2) Apatch"
    echo "3) Unroot (Stock Boot)"
    read -rp "Enter choice (1/2/3): " choice

    case "$choice" in
        1)
            echo
            echo -n ">> Installing Magisk..."
            sudo fastboot flash boot "boot_${BOOTVER}.img" >/dev/null 2>&1
            sudo fastboot reboot bootloader >/dev/null 2>&1
            sudo fastboot flash init_boot_a init_boot_a_magisk.img >/dev/null 2>&1
            sleep_dots
            echo ">> Magisk installed successfully."
            break
            ;;
        2)
            echo
            echo -n ">> Installing Apatch..."
            sudo fastboot flash boot "boot_${BOOTVER}_apatch.img" >/dev/null 2>&1
            sudo fastboot reboot bootloader >/dev/null 2>&1
            sudo fastboot flash init_boot_a init_boot_a.img >/dev/null 2>&1
            sleep_dots
            echo ">> Apatch installed successfully."
            break
            ;;
        3)
            echo
            echo -n ">> Flashing stock boot (Unroot)..."
            sudo fastboot flash boot "boot_${BOOTVER}.img" >/dev/null 2>&1
            sudo fastboot reboot bootloader >/dev/null 2>&1
            sudo fastboot flash init_boot_a init_boot_a.img >/dev/null 2>&1
            sleep_dots
            echo ">> Stock boot flashed (Unrooted)."
            break
            ;;
        *)
            echo "Invalid choice. Please enter 1, 2, or 3."
            ;;
    esac
done

# ============================
# Final reboot
# ============================
echo
echo -n ">> Rebooting device now..."
sudo fastboot reboot >/dev/null 2>&1
sleep_dots
echo
read -rp "Press Enter to exit..."
