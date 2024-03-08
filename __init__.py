# __init__.py

from .dir_picker import DirPicker
from .dir_loop import LoopyDir
from .image_nabber import ImageNabber
import importlib.util


def install_tkinter():
    # Helper function to install the tkinter module if not already installed
    try:
        importlib.import_module('tkinter')
    except ImportError:
        try:
            import pip
            pip.main(['install', 'tk'])
            # If macOS, attempt to install via brew
            import platform
            if platform.system() == 'Darwin':
                try:
                    import subprocess
                    subprocess.run(['brew', 'install', 'python-tk'])
                except FileNotFoundError:
                    pass
        except:
            print("Could not install tkinter")


install_tkinter()

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
