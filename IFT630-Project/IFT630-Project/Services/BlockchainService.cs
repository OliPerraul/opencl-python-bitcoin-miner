using System;
using System.Linq;
using System.Text;
using System.Threading;
using IFT630_Project.Event;
using IFT630_Project.Interfaces;

namespace IFT630_Project
{
    public class BlockchainService : IBlockchainService
    {
        private IBlockchain Blockchain { get; }
        private IHashingService HashingService { get; }
        private ITransactionService TransactionService { get; }
        private readonly object ValidateBlockMutex = new Object();

        public delegate void BlockchainServiceEventHandler(object src, BlockEventArgs args);

        public byte[] GetTransactionHash()
        {
            return HashingService.ComputeHash(TransactionService.PendingTransactionHash());
        }

        public event BlockchainServiceEventHandler NewBlock;
        
        public BlockchainService(IHashingService hashingService, ITransactionService transactionService, IDifficulty difficulty)
        {
            HashingService = hashingService;
            TransactionService = transactionService;
            Blockchain = new Blockchain(difficulty);
        }


        public int GetChainDifficulty()
        {
            return Blockchain.GetDifficulty().GetDifficulty();
        }

        public uint GetChainVersion()
        {
            return Blockchain.Version;
        }

        public IBlock GetLatestBlock()
        {
            return Blockchain.GetLatestBlock();
        }


        public bool ValidateBlock(IBlock blockToValidate)
        {
            var latestBlockHash = HashingService.ComputeHash(Blockchain.GetLatestBlock().BlockHashFormat());
            if (!latestBlockHash.SequenceEqual(blockToValidate.PreviousHash)) return false;

            var target = GetChainFormattedDifficulty();

            var hashedBlock = HashingService.ComputeHash(blockToValidate.BlockHashFormat());
            var blockHex = hashedBlock.ToHex();
            return hashedBlock.ToHex().StartsWith(target);
        }

        public string GetChainFormattedDifficulty()
        {
            var chainDifficuty = Blockchain.GetDifficulty();
            var target = chainDifficuty.TranslateDifficulty();
            return target;
        }

        public byte[] GetLastestBlockHash()
        {
            var latestBlock = GetLatestBlock();
            var lastBlockHash = HashingService.ComputeHash(latestBlock.BlockHashFormat());
            return lastBlockHash;
        }

        public bool AddBlock(IBlock block, int workerId)
        {
            lock (ValidateBlockMutex)
            {
                if (!ValidateBlock(block)) return false;

                Blockchain.AddBlockToChain(block);
                OnNewBlock(GetLastestBlockHash());
                Console.WriteLine($"Worker {workerId} just minned bloc {Blockchain.BlockChainSize()} Nonce: {block.Nonce}");
                Console.WriteLine("\t"+block.BlockStringFormat());
            }

            return true;
        }

        protected virtual void OnNewBlock(byte[] blochHash)
        {
            NewBlock?.Invoke(this, new BlockEventArgs(blochHash));
        }
    }
}