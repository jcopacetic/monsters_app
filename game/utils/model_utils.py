from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage
from PIL import Image


def handle_model_image(obj_img):
    if obj_img:
        square_size = 300
        if settings.DEBUG:
            # Image processing for DEBUG mode
            image = Image.open(obj_img.path)
            if image.mode in ("RGBA", "p"):
                image = image.convert("RGB")

            output_size = (square_size, square_size)
            image.thumbnail(output_size)
            image.save(obj_img.path)
        else:
            # Image processing for production (DEBUG=False) mode
            image = Image.open(obj_img)
            if image.mode in ("RGBA", "p"):
                image = image.convert("RGB")
            if image.height > square_size or image.width > square_size:
                output_size = (square_size, square_size)
            image.thumbnail(output_size)
            # Save the processed image to storage
            temp_buffer = BytesIO()
            image.save(temp_buffer, format="PNG")
            temp_buffer.seek(0)
            storage.save(obj_img.name, ContentFile(temp_buffer.read()))
