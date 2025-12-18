import subprocess
import sys
import os

def install_pyinstaller():
    print("Проверка наличия PyInstaller...")
    try:
        import PyInstaller
        print("PyInstaller уже установлен.")
    except ImportError:
        print("Установка PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_app():
    print(f"Начинаю сборку для платформы: {sys.platform}")
    
    # Команда для PyInstaller
    # --onefile: собрать в один файл
    # --windowed: без консольного окна (для GUI)
    # --name: имя выходного файла
    # --add-data: (не нужно, так как мы импортируем python файлы как модули)
    
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "UVM_Variant7",
        "gui.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*40)
        print("СБОРКА ЗАВЕРШЕНА УСПЕШНО!")
        print("="*40)
        
        dist_folder = os.path.join(os.getcwd(), "dist")
        print(f"Исполняемый файл находится в папке: {dist_folder}")
        
    except subprocess.CalledProcessError:
        print("Ошибка при сборке!")
        sys.exit(1)

if __name__ == "__main__":
    install_pyinstaller()
    build_app()

    