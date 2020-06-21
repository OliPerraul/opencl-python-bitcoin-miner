using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using IFT630_Project.Interfaces;

namespace IFT630_Project
{
    public class Blockchain : IBlockchain
    {
        private List<IBlock> Chain { get; }
        private IDifficulty Difficulty { get; }
        public uint Version { get; }

        public Blockchain(IDifficulty difficulty)
        {
            Chain = new List<IBlock>();
            Difficulty = difficulty;
            Version = 1;

            CreateGenesisBlock();
        }

        private void CreateGenesisBlock()
        {
            var genesis = new Block()
            {
                TimeStamp = (uint) DateTimeOffset.UtcNow.Second,
                PreviousHash = new[] {Byte.MinValue},
                Data = String.Empty,
                Version = Version,
                Difficulte = Difficulty.GetDifficulty(),
                Nonce = UInt32.MinValue
            };
            genesis.SetMerkleHash(new []{Byte.MinValue});

            Chain.Add(genesis);
        }

        public int BlockChainSize()
        {
            return Chain.Count;
        }

        public IBlock GetLatestBlock()
        {
            lock (Chain)
            {
                return Chain.Last();
            }
        }

        public IDifficulty GetDifficulty()
        {
            return Difficulty;
        }


        public void AddBlockToChain(IBlock block)
        {
            lock (Chain)
            {
                Chain.Add(block);
            }
        }
    }
}