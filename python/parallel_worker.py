
import multiprocessing as mp
import util


NonceSize = 32  # 32bits
NumThreads = mp.cpu_count()
WorkloadSize = 1000
NumNonceTrials = WorkloadSize//NumThreads


class Worker(mp.Process):
    def __init__(self, threadid, difficulty, chain):
        mp.Process.__init__(self)
        self.threadid = threadid
        self.difficulty = difficulty
        self.chain = chain

    def run(self):
        while True:
            self.target = util.Block(self.difficulty)
            for i in range(NumNonceTrials):
                nonce = self.threadid * NumNonceTrials + i
                block_bytes = util.concat(self.target, nonce)
                hash = util.sha256(block_bytes)
                if util.block_valid(hash, self.difficulty):
                    self.target.nonce = nonce
                    self.chain.append(block_bytes)
                    print(f"New Block Minned \t{hash.hexdigest()}")
                    # will create a new bloc
                    break


def work(difficulty):
    with mp.Manager() as manager:
        blockchain = manager.list()
        workers = [Worker(i, difficulty, blockchain)
                   for i in range(NumThreads)]
        [c.start() for c in workers]
        # Blocking call
        for w in workers:
            w.join()


# Flags for metrics
INFOS = ["Parallel 7700K ", "red"]
