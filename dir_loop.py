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

    RETURN_TYPES = ("INT", "INT", "STRING")  # Outputs the index and filename
    RETURN_NAMES = ("file_count", "current_index", "current_file")

    OUTPUT_NODE = True

    FUNCTION = "iterate_directory"
    CATEGORY = "Dir Gir"

    def iterate_directory(cls, directory, filter_type, filter_value, loop_index, prompt, id):
        # Load or refresh the list of matched files
        cls.matched_files = filter_files(directory, filter_type, filter_value)

        if len(cls.matched_files) == 0:
            # No files found, reset index
            cls.file_index = 0
            loop_indexes[id] = 0
            print("No files found in directory" + directory)
            return (0, 0, "")

        # If the loop index is not the same as the cls index + 1, set the cls index to the loop index
        if loop_index != cls.file_index + 1 and loop_index < len(cls.matched_files):
            cls.file_index = loop_index
            loop_indexes[id] = cls.file_index

        print(f"Loop index: {loop_index}, cls index: {cls.file_index}")

        # Serve the next file in the list
        current_file = cls.matched_files[cls.file_index]

        # Prepare outputs
        output = (len(cls.matched_files), cls.file_index, current_file)

        # Increment index or reset if at the end
        cls.file_index = (cls.file_index + 1) % len(cls.matched_files)
        loop_indexes[id] = cls.file_index

        return output


@server.PromptServer.instance.routes.get("/gir-dir/loop-index")
async def get_last_index(request):
    return web.json_response({'loop_index': loop_indexes.get(request.rel_url.query.get('id', '')) or 0})
