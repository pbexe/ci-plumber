from enum import Enum


class Module_attribute(str, Enum):
    source_code = "source_code"
    builder = "builder"
    image_store = "image_store"
    consumer = "consumer"
