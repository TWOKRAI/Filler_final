import subprocess

subprocess.run(['pyuic5', 'Window_main/UI_main_filler.ui', '-o', 'Window_main/main_filler.py'], check=True)
