import ctypes
from . import lib


def read_memory(pid, remote_address, length):
    buffer = ctypes.create_string_buffer(length)
    bytes_read = lib.read_process_memory(pid, buffer, ctypes.c_void_p(remote_address), length, 1)

    if bytes_read == -1:
        raise Exception("ReadProcessMemory failed")
    
    return buffer.raw[:bytes_read]