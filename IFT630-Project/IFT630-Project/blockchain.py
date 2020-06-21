import pycuda.autoinit as cuda_autoinit
import pycuda.driver as cuda_driver
import pycuda.compiler as cuda_compiler
import pycuda.tools as cuda_tools
import numpy as np
import math
import time
import os

# Do not attempt ever single possible nonce per starting block
# Otherwise we will lose to much time waiting for thread to complete
# when solution is already found
NonceSize = 32 # 32bits
BlockSize = 512
WorkloadSize = int(math.pow(2, NonceSize))
NumNonceTrials = np.uint32(WorkloadSize//BlockSize)
GridSize = 1

print(WorkloadSize)
print(NumNonceTrials)

class Block:
    Difficulty = np.uint32(2)
    Version = np.uint32(4)
    PrevHashSize = np.uint32(32)
    MerkleHashSize = np.uint32(32)
    Size = np.uint32(80)

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
        self.prevHash = np.array(
            bytearray(np.random.bytes(self.PrevHashSize)),
            dtype=np.uint8)

        # 256-bit hash based on all of the transactions in the block
        # NOTE: This value is mocked by providing a random byte array
        self.merkleHash = np.array(
            bytearray(np.random.bytes(self.MerkleHashSize)),
            dtype=np.uint8)


if __name__ == '__main__':
    # Compile opencl kernel

    source = ''
    file = 'blockchain.cu'
    dir_path = os.path.dirname(os.path.realpath(file))
    with open(file, 'r') as file:
        source = file.read()

    module = cuda_compiler.SourceModule(source, include_dirs=[dir_path])
    kernel_function = module.get_function("compute_blockchain")

    outputBuffer = np.array(
        bytearray(Block.Size),
        dtype=np.uint8)

    blockOutputBuffer = np.array(
        bytearray(Block.Size),
        dtype=np.uint8)

    finished = True

    while True:
        # Starting block from which we iterate over potential nonce
        # Assume timestamp is valid over last blocks retrieved in a newtwork
        finished = False
        block = Block()
        found = np.zeros(1, dtype=np.bool)
        print(found)

         # In Cuda
        # Blocks are a collection of thread that can communicate
        # Grid collection of thread blocks
        kernel_function(
            NumNonceTrials,
            block.version,
            block.timestamp,
            block.difficulty,
            cuda_driver.In(block.prevHash),
            cuda_driver.In(block.merkleHash),
            cuda_driver.InOut(found),
            cuda_driver.Out(outputBuffer),
            cuda_driver.Out(blockOutputBuffer),
            block=(BlockSize, 1, 1),
            grid=(GridSize, 1, 1))

        # Outputs the same result
        if found[0] and not finished:
            finished = True
            print("Hash:")
            print(outputBuffer)
            print("Block:")
            print(blockOutputBuffer)

