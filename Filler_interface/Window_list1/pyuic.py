import subprocess

subprocess.run(['pyuic5', 'Window_list1/UI.ui', '-o', 'Window_list1/PYUI.py'], check=True)

