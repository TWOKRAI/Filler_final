import subprocess

subprocess.run(['pyuic5', 'Window_view/UI_view.ui', '-o', 'Window_view/view.py'], check=True)
