import ctypes
from platform import system
from os import path



try:
    script_dir = path.dirname(path.abspath(__file__))
except:
    script_dir = os.getcwd()

noise_dir = path.join(script_dir)
 
if system() == 'Windows':
    lib_extension = '.dll'
else:
    lib_extension = '.so'
lib_path = path.join(noise_dir,"noise" + lib_extension)



lib = ctypes.CDLL(lib_path)  


lib.init()
lib.noise.argtypes = [ctypes.c_double, ctypes.c_double,ctypes.c_double]
lib.noise.restype = ctypes.c_double
lib.fbm.argtypes = [ctypes.c_double, ctypes.c_double,ctypes.c_double,ctypes.c_int,ctypes.c_double,ctypes.c_double]
lib.fbm.restype = ctypes.c_double

fbm = lib.fbm
noise = lib.noise



if __name__ == "__main__":
    print(system())