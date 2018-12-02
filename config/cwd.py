import os, sys
#Determines the system type
if sys.platform == "linux":
    cwdmain = os.getenv('PWD')
    cwd = os.path.dirname(os.getcwd())
elif sys.platform == "win32":
    cwdmain = os.getcwd()
    cwd = os.path.abspath(os.path.join(cwdmain, os.pardir))
