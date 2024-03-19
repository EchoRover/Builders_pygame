import ctypes
from platform import system

if system() == 'Windows':
    lib_path = 'noise_win.dylib'
else:
    lib_path = 'noise.so'


lib = ctypes.CDLL(lib_path)  


lib.init()
lib.noise.argtypes = [ctypes.c_double, ctypes.c_double,ctypes.c_double]
lib.noise.restype = ctypes.c_double
lib.fbm.argtypes = [ctypes.c_double, ctypes.c_double,ctypes.c_double,ctypes.c_int,ctypes.c_double,ctypes.c_double]
lib.fbm.restype = ctypes.c_double

fbm = lib.fbm
noise = lib.noise