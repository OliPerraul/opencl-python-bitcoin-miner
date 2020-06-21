
import numpy as np
import ctypes
import time
import random
import hashlib


"""
from sys import platform as _platform

def sha256(bytes):
    return hashlib.sha256(bytes)
      
    # if running program on windows x64 used to precompile DLL
    if _platform == "win64":
        # Windows 64-bit
        dest = bytearray(32)
        # Declare buffer structure
        mytype = ctypes.c_char * len(bytes)
        source_buffer = mytype.from_buffer(bytes)
        dest_buffer = mytype.from_buffer(dest)
        lib.hash_sha256(source_buffer, dest_buffer, len(source))
        return dest
    else:
    # Othewise use the python implementation
        return hashlib.sha256(bytes)
"""
def sha256(bytes):
    return hashlib.sha256(bytes)


def block_valid(block_hash, difficulty):
    return block_hash.hexdigest().startswith('0'*difficulty)


class Blockchain:
    chain = []

    def __init__(self):
        pass

    def reset(self):
        chain = []


TransactionLength = 600
Base58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def get_pending_transaction_hash():
    sb = ''
    for k in range(TransactionLength):
        sb += random.choice(Base58)
    return sb


class GenesisBlock:
    def __init__(self):
        # Block version number
        self.version = np.uint32(4)

        # Current block timestamp as seconds since 1970-01-01T00:00 UTC
        # NOTE: A timestamp is accepted as valid if it is greater than the median timestamp of previous 11 blocks,
        # and less than the network-adjusted time + 2 hours.
        # Here we make the assumption that the median of the last blocks mined is indeed smaller than the timestamp
        # This could very well not be the could not be the case because it is permited to use future timestamp
        self.timestamp = np.uint32(int(time.time()))

        # Current target in compact format
        self.difficulty = np.uint32(self.Difficulty)

        # 32-bit number (starts at 0)
        self.nonce = np.uint32(0)

        # 256-bit hash of the previous block header
        # NOTE: This value is mocked by providing a random byte array
        self.prevHash = np.array(Block.PrevHashSize, dtype=np.uint8)

        # 256-bit hash based on all of the transactions in the block
        # NOTE: This value is mocked by providing a random byte array
        self.merkleHash = np.array(
            bytearray(np.random.bytes(self.MerkleHashSize)),
            dtype=np.uint8)


class Block:
    Version = np.uint32(4)
    PrevHashSize = np.uint32(32)
    MerkleHashSize = np.uint32(32)
    Size = np.uint32(80)
    NonceSize = np.uint(32)

    def __init__(self, difficulty):
        # Block version number
        self.version = np.uint32(4)

        # Current block timestamp as seconds since 1970-01-01T00:00 UTC
        # NOTE: A timestamp is accepted as valid if it is greater than the median timestamp of previous 11 blocks,
        # and less than the network-adjusted time + 2 hours.
        # Here we make the assumption that the median of the last blocks mined is indeed smaller than the timestamp
        # This could very well not be the could not be the case because it is permited to use future timestamp
        self.timestamp = np.uint32(int(time.time()))

        # Current target in compact format
        self.difficulty = np.uint32(difficulty)

        # 32-bit number (starts at 0)
        self.nonce = np.uint32(0)

        # 256-bit hash of the previous block header
        # NOTE: This value is mocked by providing a random byte array
        self.prevHash = np.array(
            bytearray(np.random.bytes(self.PrevHashSize)),
            dtype=np.uint8)

        # 256-bit hash based on all of the transactions in the block
        # NOTE: This value is mocked by providing a random byte array
        self.merkleHash = np.array(
            bytearray(np.random.bytes(self.MerkleHashSize)),
            dtype=np.uint8)

    def update_time_stamp(self):
        self.timestamp = np.uint32(int(time.time()), dtype=np.uint8)


def concat(block: Block, nonce):
    res = bytearray(block.version.tobytes())
    res.extend(bytearray(block.prevHash.tobytes()))
    res.extend(bytearray(block.merkleHash.tobytes()))
    res.extend(bytearray(block.timestamp.tobytes()))
    res.extend(bytearray(block.difficulty.tobytes()))
    res.extend(bytearray(nonce.to_bytes(4, byteorder='little', signed=False)))
    return res
