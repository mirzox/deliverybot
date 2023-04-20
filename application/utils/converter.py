import os
from PIL import Image
import pyheif
from config import Config
from werkzeug.datastructures import FileStorage


def HEIC_JPG(file: str):
    # f_name = file.replace('.HEIC', ".jpg")
    f_name = f"{''.join(file.split('.')[:-1])}.jpg"
    file_path = os.path.join(Config.UPLOAD_DIRECTORY, f_name)
    heif_file = pyheif.read(file)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
        )
    image.save(file_path, "JPEG")
    return file_path

