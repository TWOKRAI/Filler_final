import subprocess

subprocess.run(['pyuic5', f'Window_settings1/Window_pop_up/pop_up.ui', '-o', f'Window_settings1/Window_pop_up/pop_up.py'], check=True)
