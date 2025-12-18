import subprocess
import sys
import importlib.util
import os

def check_and_install_package(package_import_name, pip_install_name):
    if importlib.util.find_spec(package_import_name) is None:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_install_name])
        except subprocess.CalledProcessError:
            sys.exit(1)

def check_and_install_tkinter_linux():
    if sys.platform.startswith("linux"):
        try:
            import tkinter
        except ImportError:
            try:
                subprocess.check_call(['sudo', 'apt-get', 'update'])
                subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'python3-tk'])
            except subprocess.CalledProcessError:
                sys.exit(1)

def build_app():
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "UVM_Variant7",
        "gui.py"
    ]
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError:
        sys.exit(1)

if __name__ == "__main__":
    check_and_install_package("yaml", "PyYAML")
    check_and_install_package("PyInstaller", "pyinstaller")
    check_and_install_tkinter_linux()
    build_app()
    