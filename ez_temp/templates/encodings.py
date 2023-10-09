import codecs
import os
from pathlib import Path

import magic


def check_encoding(file):
    with open(file, "rb") as reader:
        blob = reader.read()
        encoding_obj = magic.Magic(mime_encoding=True)
        encoding = encoding_obj.from_buffer(blob)
        return encoding


def change_encoding(file, encoding):
    with codecs.open(file, "r", encoding) as source_file:
        temp_file = f"{str(file)}.utf8"
        with codecs.open(temp_file, "w", "utf-8") as out_file:
            while True:
                contents = source_file.read(1024)
                if not contents:
                    break
                out_file.write(contents)

        with Path(temp_file).open("r") as reader:
            contents = reader.read()

        with Path(file).open("w", encoding="utf-8") as writer:
            writer.write(contents)

        Path(temp_file).unlink()



