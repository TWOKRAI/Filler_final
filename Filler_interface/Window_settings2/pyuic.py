import subprocess

subprocess.run(['pyuic5', 'Window_settings2/UI_settings2.ui', '-o', 'Window_settings2/settings2.py'], check=True)
