using System;
using IFT630_Project.Interfaces;

namespace IFT630_Project.Interfaces
{
    public interface IBlockchainService
    {
        bool ValidateBlock(IBlock blockToValidate);
        int GetChainDifficulty();
        uint GetChainVersion();
        byte[] GetLastestBlockHash();
        string GetChainFormattedDifficulty();
        bool AddBlock(IBlock block, int workerId);
        byte[] GetTransactionHash();
        event BlockchainService.BlockchainServiceEventHandler NewBlock;
    }
       
    

    public interface IBlockchain
    {
        uint Version { get; }
        int BlockChainSize();
        IBlock GetLatestBlock();
        IDifficulty GetDifficulty();
        void AddBlockToChain(IBlock block);
    }
}