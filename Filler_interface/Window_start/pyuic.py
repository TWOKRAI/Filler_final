import subprocess

subprocess.run(['pyuic5', 'Window_start/UI_start.ui', '-o', 'Window_start/start.py'], check=True)
