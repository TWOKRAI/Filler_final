import subprocess

subprocess.run(['pyuic5', 'Window_statistic/UI.ui', '-o', 'Window_statistic/PYUI.py'], check=True)