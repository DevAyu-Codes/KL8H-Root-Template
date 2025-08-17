@echo off
title Apatch/Magisk Installer
color 0A
setlocal EnableDelayedExpansion

:: Set kernel/boot version once here
set BOOTVER=5.15.188

:: ============================
:: START
:: ============================
echo =============================
echo     Apatch/Magisk Installer
echo =============================
echo Device: Tecno Spark 30C (KL8H)
echo Developer: Ayu Kashyap - @dev_ayu
echo.
echo ^>^> Allow the ADB popup on your phone if prompted.
pause

echo.
<nul set /p=^>^> Rebooting to Fastboot Mode...
adb reboot fastboot >nul 2>&1
call :dots

:: ============================
:: Root / Unroot Selection Loop
:: ============================
:choose_root
echo.
echo Select boot method:
echo [1] Magisk
echo [2] Apatch
echo [3] Unroot (Stock Boot)
set /p choice="Enter choice (1/2/3): "

if "%choice%"=="1" goto magisk
if "%choice%"=="2" goto apatch
if "%choice%"=="3" goto unroot
echo Invalid choice. Please enter 1, 2, or 3.
goto choose_root

:magisk
echo.
<nul set /p=^>^> Installing Magisk...
fastboot flash boot boot_%BOOTVER%.img >nul 2>&1
fastboot reboot bootloader >nul 2>&1
fastboot flash init_boot_a init_boot_a_magisk.img >nul 2>&1
call :dots
echo ^>^> Magisk installed successfully.
goto reboot

:apatch
echo.
<nul set /p=^>^> Installing Apatch...
fastboot flash boot boot_%BOOTVER%_apatch.img >nul 2>&1
fastboot reboot bootloader >nul 2>&1
fastboot flash init_boot_a init_boot_a.img >nul 2>&1
call :dots
echo ^>^> Apatch installed successfully.
goto reboot

:unroot
echo.
<nul set /p=^>^> Flashing stock boot (Unroot)...
fastboot flash boot boot_%BOOTVER%.img >nul 2>&1
fastboot reboot bootloader >nul 2>&1
fastboot flash init_boot_a init_boot_a.img >nul 2>&1
call :dots
echo ^>^> Stock boot flashed (Unrooted).
goto reboot

:reboot
echo.
<nul set /p=^>^> Rebooting device now...
fastboot reboot >nul 2>&1
call :dots
echo.
pause
exit /b

:: ============================
:: Function: Animated Dots
:: ============================
:dots
for /L %%i in (1,1,3) do (
    <nul set /p=.
    timeout /nobreak /t 1 >nul
)
echo.
goto :eof
