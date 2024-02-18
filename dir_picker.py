# dir_picker.py
from aiohttp import web
import tkinter as tk
import json
from tkinter import filedialog
import server
import os

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
        print("Selected folder:", folder_path)
        return folder_path or defaultPath


@server.PromptServer.instance.routes.get("/select-directory")
async def select_folder_route(request):
    load_picked_dirs()
    return await DirPicker.select_directory(request)


@server.PromptServer.instance.routes.get("/get-directory")
async def get_last_selected_directory(request):
    load_picked_dirs()
    return web.json_response({'selected_folder': picked_dirs.get(request.rel_url.query.get('id', ''))})


@server.PromptServer.instance.routes.get("/set-directory")
async def set_last_selected_directory(request):
    picked_dirs[request.rel_url.query.get(
        'id', '')] = request.rel_url.query.get('directory', '')
    save_picked_dirs()
    return web.json_response({'status': 'success'})
