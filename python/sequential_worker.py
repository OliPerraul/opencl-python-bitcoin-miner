import util


NonceSize = 32  # 32bits
NumNonceTrials = 10000


def work(difficulty):
    while True:
        block = util.Block(difficulty)
        for nonce in range(NumNonceTrials):
            block_bytes = util.concat(block, nonce)
            hash = util.sha256(block_bytes)
            if util.block_valid(hash, block.difficulty):
                block.nonce = nonce
                util.Blockchain.chain.append(block)
                print(f"New Block Minned \t{hash.hexdigest()}")

                # Create a new  block
                break


# Flags for metrics
INFOS = ["Sequential ", "blue"]
