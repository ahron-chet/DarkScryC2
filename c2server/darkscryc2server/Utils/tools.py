import ctypes
import xml.etree.ElementTree as ET
from typing import Union, Dict
import json
from ..Models.protocols import SOCKET_BASE_MESSAGE_HEADER
import os


def pack_base_header(header: SOCKET_BASE_MESSAGE_HEADER) -> bytes:
    size = ctypes.sizeof(header)
    return ctypes.string_at(ctypes.addressof(header), size)

def unpack_base_header(data: bytes) -> SOCKET_BASE_MESSAGE_HEADER:
    header = SOCKET_BASE_MESSAGE_HEADER()
    size = min(len(data), ctypes.sizeof(header))
    ctypes.memmove(ctypes.addressof(header), data, size)
    return header


def hex_to_bytes(hex_string):
    """
    Convert a hexadecimal string (hex digest) back to its original byte array.
    
    :param hex_string: The hexadecimal string to convert.
    :return: A byte array representing the original data.
    """
    try:
        return bytes.fromhex(hex_string)
    except ValueError:
        raise ValueError("Invalid hexadecimal string")
    



def json_to_xml(jsn: Union[str, Dict]) -> str:
    """
    Converts a JSON string or dictionary into an XML string.
    
    Args:
        jsn (Union[str, dict]): JSON data as a string or dictionary.
    
    Returns:
        str: The equivalent XML string.
    """
    if isinstance(jsn, str):
        try:
            jsn = json.loads(jsn)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string provided: {e}")

    if not isinstance(jsn, dict):
        raise ValueError("JSON data must be a dictionary or a string that represents a dictionary.")

    return gen_xml("root", **jsn)


def gen_xml(tag: str, filter_none=False, **kwargs) -> str:
    """
    Generates an XML string for a given tag and attributes.
    
    Args:
        tag (str): The name of the XML tag.
        filter_none (bool): If True, skips None values.
        **kwargs: Key-value pairs to convert to XML elements.
    
    Returns:
        str: The generated XML string.
    """
    elem = ET.Element(tag)
    for key, val in kwargs.items():
        if filter_none and val is None:
            continue
        
        if isinstance(val, dict):
            child = ET.fromstring(gen_xml(key, filter_none=filter_none, **val))
        elif isinstance(val, list):
            for item in val:
                if isinstance(item, dict):
                    child = ET.fromstring(gen_xml(key, filter_none=filter_none, **item))
                else:
                    child = ET.Element(key)
                    child.text = str(item) if item is not None else ''
                elem.append(child)
            continue
        else:
            child = ET.Element(str(key))
            child.text = str(val) if val is not None else ''
        
        elem.append(child)
    return ET.tostring(elem, encoding='unicode')




def getenv_nonempty(key, default=None):
    """
    Works like os.getenv, but treats blank strings as missing.
    Returns `default` if the env var is unset or just blank.
    """
    value = os.getenv(key)
    return value if value and value.strip() else default
