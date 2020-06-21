import sys
import pyopencl as cl
import numpy as np
import util

LocalSize = 1
# number of work items
GlobalSize = np.uint32(1000)


def init():
    # Create opencl context
    # On the GPU if found, CPU otherwise
    platforms = cl.get_platforms()
    gpus = platforms[0].get_devices(device_type=cl.device_type.GPU)
    context = None
    if len(gpus) == 0:
        context = cl.create_some_context()
        # On CPU local work group size mus be one
        LocalSize = np.uint32(1)
    else:
        context = cl.Context(devices=gpus)

    # Compile opencl kernel
    with open('gpu_worker.cl', 'r') as file:
        source = file.read()

    program = cl.Program(context, source).build()
    commandQueue = cl.CommandQueue(context)
    return program, context, commandQueue


def work(difficulty):
    block = util.Block(difficulty)
    program, context, commandQueue = init()

    while True:
        prevHashBuffer = cl.Buffer(
            context,
            cl.mem_flags.READ_ONLY,
            util.Block.PrevHashSize)

        merkleHashBuffer = cl.Buffer(
            context,
            cl.mem_flags.READ_ONLY,
            util.Block.MerkleHashSize)

        foundBuffer = cl.Buffer(
            context,
            cl.mem_flags.READ_WRITE,
            np.uint(32))

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
            util.Block.NonceSize)

        # Copy result from decoding buffer onto dest
        # copying data off the device
        foundBufferDest = np.array(
            bytearray(1),
            dtype=np.int32)

        # Copy result from decoding buffer onto dest
        # copying data off the device
        outputNonceBufferDest = np.array(
            bytearray(util.Block.NonceSize),
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
            np.int32(1),
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
            foundBufferDest[0] = False
            block.nonce = outputNonceBufferDest[0]
            util.Blockchain.chain.append(block)
            print(f"New Block Minned \t{outputBufferDest.tobytes().hex()}")

        block.update_time_stamp()


# Flags for metrics
INFOS = ["GPU 1080 TI ", "purple"]
