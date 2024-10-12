import subprocess

subprocess.run(['pyuic5', 'Window_level/UI_level.ui', '-o', 'Window_level/level.py'], check=True)
