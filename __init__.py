# __init__.py

from .dir_picker import DirPicker
from .dir_loop import LoopyDir
import importlib.util


def install_tkinter():
    # Helper function to install the tkinter module if not already installed
    try:
        importlib.import_module('tkinter')
    except ImportError:
        import pip
        pip.main(['install', 'tkinter'])
        # If macOS, attempt to install via brew
        import platform
        if platform.system() == 'Darwin':
            try:
                import subprocess
                subprocess.run(['brew', 'install', 'python-tk'])
            except FileNotFoundError:
                pass


install_tkinter()

WEB_DIRECTORY = "./web"

NODE_CLASS_MAPPINGS = {
    "Dir_Gir_Picker": DirPicker,
    "Dir_Gir_Looper": LoopyDir,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Dir_Gir_Picker": "GIR Dir Picker",
    "Dir_Gir_Looper": "GIR Loopy Dir",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
