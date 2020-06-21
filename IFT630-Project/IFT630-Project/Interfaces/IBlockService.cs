using System;

namespace IFT630_Project.Interfaces
{
    public interface IBlockService
    {
        IBlock Createblock(DateTime timeSpan, string previousHash, string data, int version, int difficulte);
    }
}