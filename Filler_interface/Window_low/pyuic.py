import subprocess

subprocess.run(['pyuic5', 'Window_low/UI_main_low.ui', '-o', 'Window_low/main_low.py'], check=True)