using System;
using System.Threading;
using IFT630_Project.Event;
using IFT630_Project.Interfaces;
using static System.UInt32;

namespace IFT630_Project
{
    public class SequentialWorker : AbstractWorker
    {
        private int Id { get; set; }
        private IBlock CurrentBlock { get; set; }

        public SequentialWorker(IBlockchainService blockchainService, IHashingService hashingService, int id) : base(
            blockchainService, hashingService)
        {
            Id = id;
            BlockchainService.NewBlock += OnNewBlock;
            CurrentBlock = NewGuessBlock(BlockchainService.GetLastestBlockHash());
        }

        private void OnNewBlock(object o, BlockEventArgs eventArgs)
        {
            CurrentBlock = NewGuessBlock(eventArgs.LastBlockHash);
        }


        public override void Execute()
        {
            while (true)
            {
                uint i = 0;
                CurrentBlock.TimeStamp = (uint)DateTimeOffset.UnixEpoch.Second;
                while (i < uint.MaxValue)
                {
                    CurrentBlock.Nonce = i;
                    if (BlockValid(CurrentBlock))
                    {
                        BlockchainService.AddBlock(CurrentBlock, Id);
                        Thread.Sleep(20);
                    }

                    i += 1;
                }
            }
        }
    }
}