import sys
import pyopencl as cl
import numpy as np
import time
import base64
# Do not attempt ever single possible nonce per starting block
# Otherwise we will lose to much time waiting for thread to complete
# when solution is already found

LocalSize = 1
# number of work items
NumNonceBits = 14
GlobalSize = np.uint32(10240)
NumNonceTrials = np.int32(1024)


class Block:
    #    Difficulty = np.uint32(2)
    Version = np.uint32(4)
    PrevHashSize = np.uint32(32)
    MerkleHashSize = np.uint32(32)
    Size = np.uint32(80)
    NonceSize = np.uint32(4)

    def __init__(self, version, prevHash, merkleHash, difficulty):
        # Block version number
        self.version = np.uint32(version)

        # Current block timestamp as seconds since 1970-01-01T00:00 UTC
        # NOTE: A timestamp is accepted as valid if it is greater than the median timestamp of previous 11 blocks,
        # and less than the network-adjusted time + 2 hours.
        # Here we make the assumption that the median of the last blocks mined is indeed smaller than the timestamp
        # This could very well not be the could not be the case because it is permited to use future timestamp
        self.timestamp = np.uint32(int(time.time()), dtype=np.uint8)

        # Current target in compact format
        self.difficulty = np.uint32(difficulty)

        # 32-bit number (starts at 0)
        self.nonce = np.uint32(0)

        # 256-bit hash of the previous block header
        # NOTE: This value is mocked by providing a random byte array
        self.prevHashAr = bytearray().fromhex(prevHash)
        self.prevHash = np.array(self.prevHashAr,
                                 dtype=np.uint8)
        
        # 256-bit hash based on all of the transactions in the block
        # NOTE: This value is mocked by providing a random byte array
        self.merkleHashAr = bytearray().fromhex(merkleHash)
        self.merkleHash = np.array(
            self.merkleHashAr, dtype=np.uint8)

    def update_time_stamp(self):
        self.timestamp = np.uint32(int(time.time()), dtype=np.uint8)

    def ouput_format(self, nonce):
        return f"{self.timestamp};{nonce}"
    

if __name__ == '__main__':
    # Getting inputs from Node
    version = int(sys.argv[1])
    prevHash = sys.argv[2]
    merkleHash = sys.argv[3]
    difficulty = int(sys.argv[4])
    block = Block(version, prevHash, merkleHash, difficulty)
    
    # Create opencl context
    # On the GPU if found, CPU otherwise
    platforms = cl.get_platforms()
    gpus = platforms[0].get_devices(device_type=cl.device_type.GPU)
    context = None
    found = False
    if len(gpus) == 0:
        context = cl.create_some_context()
        # On CPU local work group size mus be one
        LocalSize = np.uint32(1)
    else:
        context = cl.Context(devices=gpus)

    # Compile opencl kernel
    with open('blockchain.cl', 'r') as file:
        source = file.read()

    program = cl.Program(context, source).build()
    commandQueue = cl.CommandQueue(context)
    while not found:
        prevHashBuffer = cl.Buffer(
            context,
            cl.mem_flags.READ_ONLY,
            Block.PrevHashSize)

        merkleHashBuffer = cl.Buffer(
            context,
            cl.mem_flags.READ_ONLY,
            Block.MerkleHashSize)

        foundBuffer = cl.Buffer(
            context,
            cl.mem_flags.READ_WRITE,
            1)
        
        outputBuffer = cl.Buffer(
            context,
            cl.mem_flags.READ_WRITE,
            np.uint8(32))

        blockBuffer = cl.Buffer(
            context,
            cl.mem_flags.READ_WRITE,
            np.uint8(80))

        outputNonceBuffer = cl.Buffer(
            context,
            cl.mem_flags.READ_WRITE,
            Block.NonceSize)
        
        # Copy result from decoding buffer onto dest
        # copying data off the device
        foundBufferDest = np.array(
            bytearray(1),
            dtype=np.bool)

        # Copy result from decoding buffer onto dest
        # copying data off the device
        outputNonceBufferDest = np.array(
            bytearray(Block.NonceSize),
            dtype=np.uint8)

        outputBufferDest = np.array(
            bytearray(np.uint32(32)),
            dtype=np.uint8)
        
        blockBufferDest = np.array(
            bytearray(np.uint32(80)),
            dtype=np.uint8)

        foundBufferDest[0] = False
        # Add copy operations to the command queue
        # copying data onto the device

        cl.enqueue_copy(
            commandQueue,
            src=block.prevHash,
            dest=prevHashBuffer)

        # Add run operation to command queue
        cl.enqueue_copy(
            commandQueue,
            src=block.merkleHash,
            dest=merkleHashBuffer)


        # Set found to false
        cl.enqueue_copy(
            commandQueue,
            src=foundBufferDest,
            dest=foundBuffer)

        evt = program.compute_blockchain(
            commandQueue,
            (GlobalSize,),
            (LocalSize,),
            GlobalSize,
            NumNonceTrials,
            block.version,
            block.timestamp,
            block.difficulty,
            prevHashBuffer,
            merkleHashBuffer,
            foundBuffer,
            outputNonceBuffer,
            outputBuffer,
            blockBuffer)

        cl.enqueue_copy(
            commandQueue,
            src=outputNonceBuffer,
            dest=outputNonceBufferDest)

        cl.enqueue_copy(
            commandQueue,
            src=foundBuffer,
            dest=foundBufferDest)

        cl.enqueue_copy(
            commandQueue,
            src=outputBuffer,
            dest=outputBufferDest)

        cl.enqueue_copy(
            commandQueue,
            src=blockBuffer,
            dest=blockBufferDest)

        # Waiting for everything to finish
        evt.wait()

        if foundBufferDest[0]:
            print(blockBufferDest.tobytes().hex())
            print(outputBufferDest.tobytes().hex())

            print(block.ouput_format(outputNonceBufferDest.tobytes().hex()))
            break
    block.update_time_stamp()
