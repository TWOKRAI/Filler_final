import subprocess

subprocess.run(['pyuic5', 'Window_prepare/UI_prepare.ui', '-o', 'Window_prepare/prepare.py'], check=True)
