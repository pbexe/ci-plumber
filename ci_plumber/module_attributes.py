from enum import Enum


class Module_attribute(str, Enum):
    """The attributes that a plugin can have. A valid pipeline must have one
    and only one.

    Args:
        str: This is a string enum.
        Enum: This is an enum.
    """

    source_code = "source_code"
    builder = "builder"
    image_store = "image_store"
    consumer = "consumer"
