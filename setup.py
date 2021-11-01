import sys
from cx_Freeze import setup, Executable

exe = Executable(
      script="app.py",
      base="Win32GUI",
      targetName="AutoClicker.exe"
     )
setup(
      name="AutoClicker.exe",
      version="1.0",
      author="Kanchan Sapkota",
      description="Simple interface to auto click mouse",
      executables=[exe],
      scripts=[
               'ui.py'
               ]
      )
