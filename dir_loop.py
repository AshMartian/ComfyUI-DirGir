# dir_loop.py is a GirDir node that provides a function to iterate through a directory and return the files in it.
from aiohttp import web
import os
import re
import server

# Utility function for filtering files


def filter_files(directory, filter_type, filter_value):
    matched_files = []
    for file in os.listdir(directory):
        if filter_type == "regex" and re.match(filter_value, file):
            matched_files.append(file)
        elif filter_type == "extension" and file.endswith(filter_value):
            matched_files.append(file)
    return matched_files


loop_indexes = {}


class LoopyDir:
    # Increment this index each time a file is served, reset when reaching the end or on specific conditions
    file_index = 0
    matched_files = []

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory": ("STRING", {"forceInput": True, "default": "", "dynamicPrompts": False}),
                # Dropdown for regex or extension
                "filter_type": (["regex", "extension"], {"default": "extension"}),
                # Input for regex pattern or file extension
                "filter_value": ("STRING", {"default": "", "dynamicPrompts": False}),
                "loop_index": ("INT", {"default": 0}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "id": "UNIQUE_ID",
            }
        }

    # Outputs the index and filename
    RETURN_TYPES = ("INT", "INT", "STRING", "STRING", "COMBO")
    RETURN_NAMES = ("file_count", "current_index",
                    "current_file", "current_file_path", "all_files")

    OUTPUT_NODE = True

    FUNCTION = "iterate_directory"
    CATEGORY = "Dir Gir"

    def iterate_directory(cls, directory, filter_type, filter_value, loop_index, prompt, id):
        # Load or refresh the list of matched files
        cls.matched_files = filter_files(directory, filter_type, filter_value)

        if len(cls.matched_files) == 0:
            # No files found, reset index
            loop_indexes[id] = 0
            print("[ComfyUI-DirGir] No files found in directory" + directory)
            return (0, 0, "", "", [])

        # Ensure loop_index is within bounds
        loop_index = loop_indexes.get(id, 0)

        if loop_index >= len(cls.matched_files):
            # If the external loop index is beyond the available files, reset to 0
            loop_indexes[id] = 0

        # Serve the file at the current loop index
        current_file = cls.matched_files[loop_index]

        # Prepare outputs
        output = (len(cls.matched_files), loop_index, current_file,
                  os.path.join(directory, current_file), cls.matched_files)

        # Increment the external loop index or reset if at the end
        loop_indexes[id] = (loop_index + 1) % len(cls.matched_files)

        return output


@server.PromptServer.instance.routes.get("/gir-dir/loop-index")
async def get_last_index(request):
    return web.json_response({'loop_index': loop_indexes.get(request.rel_url.query.get('id', '')) or 0})
