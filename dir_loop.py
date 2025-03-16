# dir_loop.py is a GirDir node that provides a function to iterate through a directory and return the files in it.
from aiohttp import web
import os
import re
import server
import random

# Utility function for filtering files


def filter_files(directory, filter_type, filter_value, sort_by="name", sort_order="asc"):
    matched_files = []
    files = os.listdir(directory)
    if sort_by == "name":
        files.sort()
    elif sort_by == "date_modified":
        files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))
    elif sort_by == "date_created":
        files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)))
    if sort_order == "desc":
        files.reverse()
    if sort_order == "random":
        random.shuffle(files)

    for file in files:
        if filter_type == "regex" and re.match(filter_value, file):
            matched_files.append(file)
        elif filter_type == "extension" and file.endswith(filter_value):
            matched_files.append(file)
    return matched_files


loop_indexes = {}


class LoopyDir:
    # Increment this index each time a file is served, reset when reaching the end or on specific conditions
    file_index = 0

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory": ("STRING", {"forceInput": True, "default": "", "dynamicPrompts": False}),
                # Dropdown for regex or extension
                "filter_type": (["regex", "extension"], {"default": "extension"}),
                # Input for regex pattern or file extension
                "filter_value": ("STRING", {"default": "", "dynamicPrompts": False}),
                # Dropdown for sorting by name or date (modified/created)
                "sort_by": (["name", "date_modified", "date_created"], {"default": "name"}),
                # Dropdown for ascending or descending
                "sort_order": (["asc", "desc", "random"], {"default": "asc"}),
                # External loop index
                "loop_index": ("INT", {"default": 0}),
                # Pause looping
                "pause_loop": ("BOOLEAN", {"default": False}),
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

    def iterate_directory(cls, directory, filter_type, filter_value, sort_by, sort_order, loop_index, pause_loop, prompt, id):
        # Always refresh the list of matched files to catch any new files
        matched_files = filter_files(directory, filter_type, filter_value, sort_by, sort_order)

        if len(matched_files) == 0:
            # No files found, reset index
            loop_indexes[id] = 0
            print("[ComfyUI-DirGir] No files found in directory" + directory)
            return (0, 0, "", "", [])

        # Use the provided loop_index if it's within bounds, otherwise use stored index
        if loop_index >= 0 and loop_index < len(matched_files):
            current_index = loop_index
            loop_indexes[id] = loop_index  # Update stored index to match input
        else:
            current_index = loop_indexes.get(id, 0)
            if current_index >= len(matched_files):
                current_index = 0
                loop_indexes[id] = 0

        # Serve the file at the current index
        current_file = matched_files[current_index]

        # Prepare outputs
        output = (len(matched_files), current_index, current_file,
                  os.path.join(directory, current_file), matched_files)

        # Only increment if not paused
        if not pause_loop:
            loop_indexes[id] = (current_index + 1) % len(matched_files)

        return output


@server.PromptServer.instance.routes.get("/gir-dir/loop-index")
async def get_last_index(request):
    return web.json_response({'loop_index': loop_indexes.get(request.rel_url.query.get('id', '')) or 0})

@server.PromptServer.instance.routes.get("/gir-dir/set-loop-index")
async def set_last_index(request):
    loop_indexes[request.rel_url.query.get('id', '')] = int(request.rel_url.query.get('index', 0))
    return web.json_response({'success': True})