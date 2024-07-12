import ctypes
import os


cwd = os.path.dirname(os.path.realpath(__file__))
os.system(f"gcc {cwd}/memory.c -shared -fpic -o {cwd}/bin/libmemory.so")

lib = ctypes.CDLL(f"{cwd}/bin/libmemory.so")
lib.read_process_memory.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_size_t]
lib.read_process_memory.restype = ctypes.c_size_t

__all__ = ["lib"]