

import os
import sys
import ctypes
import numpy as np

lib = ctypes.cdll.LoadLibrary('./sha256/x64/Debug/sha256.dll')

if __name__ == '__main__':

    source = bytearray(b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') # What i want to hash
    dest = bytearray(32)
    # Declare buffer structure
    mytype = ctypes.c_char * len(source)
    source_buffer = mytype.from_buffer(source)
    dest_buffer = mytype.from_buffer(dest)
    lib.hash_sha256(source_buffer, dest_buffer, len(source))
    print(dest)
