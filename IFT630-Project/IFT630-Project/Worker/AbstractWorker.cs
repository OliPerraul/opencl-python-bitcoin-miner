using System;
using IFT630_Project.Interfaces;

namespace IFT630_Project
{
    public interface IWorker
    {
        void Execute();
    }

    public abstract class AbstractWorker : IWorker
    {
        protected AbstractWorker(IBlockchainService blockchainService, IHashingService hashingService)
        {
            BlockchainService = blockchainService;
            HashingService = hashingService;
        }

        protected IBlockchainService BlockchainService { get; }
        protected IHashingService HashingService { get; }
        
        protected bool BlockValid(IBlock block)
        {
            var difficulty = BlockchainService.GetChainFormattedDifficulty();
            var blockHash = HashingService.ComputeHash(block.BlockHashFormat());
            //TODO:CHANGE ME
            return blockHash.ToHex().StartsWith(difficulty);
        }
        
        protected Block NewGuessBlock(byte[] latestHash)
        {
            var guessBlock = new Block()
            {
                Version = BlockchainService.GetChainVersion(),
                PreviousHash = latestHash,
                Difficulte = BlockchainService.GetChainDifficulty(),
                TimeStamp = (uint)DateTimeOffset.UnixEpoch.Second
            };
            guessBlock.SetMerkleHash(BlockchainService.GetTransactionHash());
            return guessBlock;
        }

        public abstract void Execute();

    }
}