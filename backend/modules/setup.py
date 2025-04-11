import os
import requests
import platform
import subprocess
import sys
import os
import shutil


def setup_vlc():
    """Automatically install VLC and configure environment if missing"""
    try:
        import vlc
        return True
    except (ImportError, OSError):
        print("VLC not found. Starting automatic installation...")
        
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-vlc"])
        
        system = platform.system()
        if system == "Windows":
            vlc_install_path = r"C:\Program Files\VideoLAN\VLC"
            installer_url = "https://get.videolan.org/vlc/3.0.20/win64/vlc-3.0.20-win64.exe"
            
            print("Downloading VLC...")
            response = requests.get(installer_url, stream=True)
            with open("vlc_installer.exe", "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print("Installing VLC...")
            try:
                # Elevate privileges using PowerShell
                subprocess.run(
                    [
                        "powershell",
                        "-Command",
                        "Start-Process vlc_installer.exe -ArgumentList '/L=1033 /S' -Verb RunAs -Wait"
                    ],
                    check=True
                )
            except subprocess.CalledProcessError as e:
                print(f"Installation failed: {e}")
                os.remove("vlc_installer.exe")
                return False
                
            os.remove("vlc_installer.exe")
            
            os.environ['PATH'] += os.pathsep + vlc_install_path
            os.add_dll_directory(vlc_install_path)
            
        elif system == "Darwin":
            subprocess.run(
                ["brew", "install", "vlc"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            subprocess.run(
                ["sudo", "apt-get", "install", "-y", "vlc"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
        print("VLC installation completed successfully!")
        return True
    except Exception as e:
        print(f"Automatic installation failed: {e}")
        return False


