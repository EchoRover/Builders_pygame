import ctypes
import platform
# Load the shared library
if platform.system() == 'Windows':
    lib_path = './example.dll'
else:
    lib_path = './example.dylib'

example_lib = ctypes.CDLL(lib_path)

# Define function prototype
add = example_lib.add
add.argtypes = [ctypes.c_int, ctypes.c_int]
add.restype = ctypes.c_int

# Usage example
result = add(2, 3)
print("Result from C function:", result)