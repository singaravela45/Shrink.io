from PIL import Image
import os
def compress_image(input_path, output_path, level):
    img = Image.open(input_path)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    if level == "Extreme Compression":
        quality = 30
    elif level == "Recommended Compression":
        quality = 60
    else:
        quality = 85

    img.save(output_path, "JPEG", quality=quality, optimize=True)

    return output_path