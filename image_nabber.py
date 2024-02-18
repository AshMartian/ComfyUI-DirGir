import os
from PIL import Image, ImageOps
import torch
import numpy as np


class ImageNabber:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # Single file path input
                "file_path": ("STRING", {"forceInput": True, "default": "", "dynamicPrompts": False}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)

    FUNCTION = "process"
    CATEGORY = "image"
    OUTPUT_IS_LIST = (False,)
    OUTPUT_NODE = True  # Indicates that this node directly outputs to the workflow

    def process(cls, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' cannot be found.")

        # Load the image, ensuring orientation is correct and converting to tensor
        i = Image.open(file_path)
        i = ImageOps.exif_transpose(i)
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        return (image, )
