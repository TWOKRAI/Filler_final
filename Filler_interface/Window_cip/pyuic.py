import subprocess

subprocess.run(['pyuic5', 'Window_cip/UI_cip.ui', '-o', 'Window_cip/cip.py'], check=True)
