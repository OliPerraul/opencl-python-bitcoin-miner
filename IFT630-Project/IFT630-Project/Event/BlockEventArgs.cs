using System;

namespace IFT630_Project.Event
{
    public class BlockEventArgs : EventArgs
    {
        public BlockEventArgs(byte[] lastBlockHash)
        {
            LastBlockHash = lastBlockHash;
        }

        public byte[] LastBlockHash { get; set; }
    }
}