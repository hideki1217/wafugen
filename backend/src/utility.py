from typing import Callable


def snake2camel(s):
    segments = s.split("_")
    return segments[0] + "".join([seg[0].upper() + seg[1:] for seg in segments[1:]])

def convert_key(d: dict, convert: Callable[[str], str]):
    def _convert(d):
        return (
            convert_key(d, convert)
            if isinstance(d, dict) else
            d
        )
    
    return {convert(key): _convert(d[key]) for key in d.keys()}

    