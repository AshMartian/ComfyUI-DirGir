# __init__.py
import importlib.util
import sys


def install_tkinter():
    try:
        importlib.import_module('tkinter')
    except ImportError:
        print("[ComfyUI-DirGir] Attempting to install tkinter")
        try:
            import subprocess
            import platform
            system = platform.system()
            if system == 'Darwin':
                result = subprocess.run(['brew', 'install', 'python-tk'], check=True)
                if result.returncode != 0:
                    raise Exception("Brew installation failed, ensure you have brew installed (https://brew.sh/)")
            elif system == 'Linux':
                result = subprocess.run(['sudo', 'apt', '-y', 'install', 'python3-tk'], check=True)
                if result.returncode != 0:
                    raise Exception("Apt installation failed")
            else:
                result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'tk'], check=True)
                if result.returncode != 0:
                    raise Exception("Pip installation failed")
        except Exception as e:
            print("[ComfyUI-DirGir] Could not install tkinter, try setting TCL_LIBRARY and TK_LIBRARY environment variables to the location of your tcl and tk libraries (https://www.magicsplat.com/tcl-installer/index.html#downloads)")
            print(e)


install_tkinter()

from .dir_picker import DirPicker
from .dir_loop import LoopyDir
from .image_nabber import ImageNabber

WEB_DIRECTORY = "./web"

NODE_CLASS_MAPPINGS = {
    "Dir_Gir_Picker": DirPicker,
    "Dir_Gir_Looper": LoopyDir,
    "Gir_Image_Nabber": ImageNabber,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Dir_Gir_Picker": "GIR Dir Picker",
    "Dir_Gir_Looper": "GIR Loopy Dir",
    "Gir_Image_Nabber": "GIR Image (Path) Nabber",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
