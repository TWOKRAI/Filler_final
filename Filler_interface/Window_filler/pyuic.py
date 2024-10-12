import subprocess

subprocess.run(['pyuic5', 'Window_filler/UI_filler.ui', '-o', 'Window_filler/filler.py'], check=True)
