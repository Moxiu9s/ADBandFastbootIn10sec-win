import os
import subprocess
import sys
import zipfile
import requests
import time
import ctypes
from colorama import init, Fore, Style

# Initialize Colorama
init(autoreset=True)

# Constants
INSTALL_DIR = r"C:\ADBandFastbootIn10sec-win"  # Installation directory
PLATFORM_TOOLS_ZIP_URL = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"  # URL for platform-tools zip
PLATFORM_TOOLS_ZIP_PATH = os.path.join(INSTALL_DIR, "platform-tools.zip")

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Relaunch the script with administrative privileges."""
    if not is_admin():
        print("Relaunching with administrative privileges...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
        sys.exit(0)

def display_header():
    """Display a header with the title and GitHub link."""
    header = f"""
###############################
#                             #
#  ADBandFastbootIn10sec      #
#                             #
#    by @Moxiu9s              #
#  on GitHub:                 #
# https://github.com/Moxiu9s  #
#                             #
###############################"""
    print(Fore.GREEN + header)  # Make the header green
    time.sleep(2)  # Shortened wait for visibility

def download_platform_tools():
    """Download the platform-tools zip file."""
    print("Downloading platform-tools...")
    response = requests.get(PLATFORM_TOOLS_ZIP_URL)
    if response.status_code == 200:
        with open(PLATFORM_TOOLS_ZIP_PATH, "wb") as f:
            f.write(response.content)
        print(Fore.GREEN + "Download completed!")
        return True  # Indicate successful download
    else:
        print(Fore.RED + "Failed to download platform-tools. Please check your internet connection.")
        return False  # Indicate failed download

def extract_zip(zip_path, extract_to):
    """Extract the zip file to the specified directory."""
    print(f"Extracting {zip_path}...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    print(Fore.GREEN + "Extraction completed!")

def add_to_path(directory):
    """Add the specified directory to the system PATH."""
    try:
        current_path = os.environ.get("PATH")
        if directory not in current_path:
            new_path = current_path + os.pathsep + directory
            subprocess.call(['setx', 'PATH', new_path], shell=True)  # Update the PATH variable
            print(Fore.GREEN + f"Successfully added {directory} to PATH.")
            return True  # Return True if addition was successful
        else:
            print(Fore.GREEN + f"{directory} is already in PATH.")
            return True  # Return True if already in PATH
    except Exception as e:
        print(Fore.RED + f"Error adding {directory} to PATH: {e}")
        return False  # Return False if there was an error

def main():
    # Check if the script is running with admin privileges
    run_as_admin()

    # Create the installation directory if it doesn't exist
    if not os.path.exists(INSTALL_DIR):
        os.makedirs(INSTALL_DIR)

    # Display the header
    display_header()

    # Ask the user if they want to install ADB and Fastboot
    install_response = input("Do you want to install ADB and Fastboot? (1 for Yes, 0 for No): ")
    while install_response not in ['0', '1']:
        install_response = input(Fore.RED + "Invalid input. Please enter 1 for Yes or 0 for No: ")

    if install_response == '0':
        print(Fore.RED + "Installation aborted.")
        return

    # Download and extract platform-tools
    download_success = download_platform_tools()
    if download_success:
        extract_zip(PLATFORM_TOOLS_ZIP_PATH, INSTALL_DIR)

        # Ask the user if they want to add the directory to PATH
        path_response = input("Do you want to add ADB and Fastboot to the PATH? (1 for Yes, 0 for No): ")
        while path_response not in ['0', '1']:
            path_response = input(Fore.RED + "Invalid input. Please enter 1 for Yes or 0 for No: ")

        if path_response == '1':
            path_success = add_to_path(INSTALL_DIR)
            if path_success:
                print(Fore.GREEN + "Installation completed successfully! Press 1 to exit.")
            else:
                print(Fore.RED + "Installation failed while adding to PATH. Press 0 to exit.")
        else:
            print(Fore.GREEN + "Installation completed without adding to PATH. Press 1 to exit.")
    else:
        print(Fore.RED + "Installation failed. Please try again. Press 0 to exit.")

if __name__ == "__main__":
    main()
