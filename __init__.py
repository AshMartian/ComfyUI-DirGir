# __init__.py

from .dir_picker import DirPicker
import importlib.util


def install_tkinter():
    # Helper function to install the tkinter module if not already installed
    try:
        importlib.import_module('tkinter')
    except ImportError:
        import pip
        pip.main(['install', 'tkinter'])


install_tkinter()

WEB_DIRECTORY = "./web"

NODE_CLASS_MAPPINGS = {
    "Dir_Gir_DirPicker": DirPicker,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Dir_Gir_DirPicker": "GIR Directory Picker",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
