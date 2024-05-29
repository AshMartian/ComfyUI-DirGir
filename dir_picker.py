# dir_picker.py
from aiohttp import web
import json
import server
import os

try: 
    import tkinter as tk
    from tkinter import filedialog
    hasTK = True
except ImportError as e:
    hasTK = False
    print("[ComfyUI-DirGir] Could not import filedialog from tkinter, please ensure tkinter is installed (https://www.tutorialspoint.com/how-to-install-tkinter-in-python)")
    print(e)
    

picked_dirs = {}

current_path = os.path.abspath(os.path.dirname(__file__))


def save_picked_dirs():
    with open(os.path.join(current_path, 'picked_dirs.json'), 'w') as f:
        f.write(json.dumps(picked_dirs))


def load_picked_dirs():
    try:
        with open(os.path.join(current_path, 'picked_dirs.json'), 'r') as f:
            picked_dirs.update(json.loads(f.read()))
    except FileNotFoundError:
        pass


class DirPicker:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "hidden": {
                "prompt": "PROMPT",
                "id": "UNIQUE_ID",
            }
        }

    def __init__(self):
        load_picked_dirs()

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("directory",)
    OUTPUT_IS_LIST = (False,)
    OUTPUT_NODE = True

    FUNCTION = "get_last_selected_directory"

    CATEGORY = "Dir Gir"

    def get_last_selected_directory(cls, prompt, id):
        return (picked_dirs.get(id), )

    @classmethod
    async def select_directory(cls, request):
        node_id = request.rel_url.query.get('id', '')
        folder_path = cls.select_folder(node_id)
        picked_dirs[node_id] = folder_path  # Store the selected directory
        save_picked_dirs()
        return web.json_response({'selected_folder': folder_path})

    @staticmethod
    def select_folder(id):
        # This method remains synchronous
        defaultPath = picked_dirs.get(id) or "~"
        if hasTK:
            try:
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                root.lift()
                root.focus_force()
                folder_path = filedialog.askdirectory(
                    initialdir=defaultPath, title="Select a directory")
                filedialog.dialogstates = {}  # Clear the dialog state
                root.quit()
                root.destroy()
                print("[ComfyUI-DirGir] Selected folder:", folder_path)
            except Exception as e:
                print("[ComfyUI-DirGir] Could not select folder")
                print(e)
                folder_path = None
        else:
            folder_path = None
            print("[ComfyUI-DirGir] Could not import filedialog from tkinter, please ensure tkinter is installed (https://www.tutorialspoint.com/how-to-install-tkinter-in-python)")
        return folder_path or defaultPath


@server.PromptServer.instance.routes.get("/gir-dir/select-directory")
async def select_folder_route(request):
    load_picked_dirs()
    return await DirPicker.select_directory(request)


@server.PromptServer.instance.routes.get("/gir-dir/get-directory")
async def get_last_selected_directory(request):
    load_picked_dirs()
    return web.json_response({'selected_folder': picked_dirs.get(request.rel_url.query.get('id', '')), 'hasTK': hasTK})


@server.PromptServer.instance.routes.get("/gir-dir/set-directory")
async def set_last_selected_directory(request):
    picked_dirs[request.rel_url.query.get(
        'id', '')] = request.rel_url.query.get('directory', '')
    save_picked_dirs()
    return web.json_response({'status': 'success'})
