import subprocess

subprocess.run(['pyuic5', 'Window_settings1/UI_settings.ui', '-o', 'Window_settings1/settings.py'], check=True)
