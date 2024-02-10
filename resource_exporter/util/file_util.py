import math


def convert_file_size(size_bytes, size=1024):
    if size_bytes == "" or size_bytes is None:
        return ""
    if isinstance(size_bytes, str):
        size_bytes = int(size_bytes)
    if size_bytes == 0:
        return "0"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, size)))
    p = math.pow(size, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])
