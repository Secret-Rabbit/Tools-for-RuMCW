import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Настройки
folder = os.getcwd()
prefix = "Grid "
extension = ".png"
file_optimizer_path = r"C:\Program Files\FileOptimizer\FileOptimizer64.exe"
max_parallel = 2
optimization_level = 7


def optimize_file(filepath):
    cmd = f'"{file_optimizer_path}" /NOWINDOW /Level={optimization_level} /CheckForUpdates=0 /AllowMultipleInstances=true "{filepath}"'
    subprocess.run(cmd, shell=True)


# Найдём все подходящие файлы
all_files = [
    os.path.join(folder, f)
    for f in os.listdir(folder)
    if f.startswith(prefix) and f.endswith(extension)
]

# Проверка наличия файла FileOptimizer.ini
if os.path.isfile(f"C:\\Users\\{os.environ.get('username')}\\FileOptimizer.ini"):
    # Запускаем с ограничением на количество потоков
    with ThreadPoolExecutor(max_workers=max_parallel) as executor:
        executor.map(optimize_file, all_files)
    print("✅ Done.")
else:
    print(
        "RU: Файл конфигурации FileOptimizer не найден. Запустите FileOptimizer и сохраните настройки при закрытии.\nEN: The FileOptimizer configuration file was not found. Run FileOptimizer and save the settings when closing."
    )
