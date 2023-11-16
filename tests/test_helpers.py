from src.helpers import (load_base_image,
                         normalize_text,
                         save_tempImage,
                        )
import os
import pytest
from PIL import Image


def test_load_base_image_invalid_path():
    with pytest.raises(FileNotFoundError) as error:
        load_base_image("/invalid/path/does/not/exist/image.png")
    assert error.match("No such file or directory")


def test_normalize_text_empty_string():
    assert normalize_text("") == ""

# create test to validate save image using pytest
def test_save_tempImage():
    with pytest.raises(TypeError) as error:
        save_tempImage(Image.Image, "")
    assert error.match("missing 1 required positional argument")

