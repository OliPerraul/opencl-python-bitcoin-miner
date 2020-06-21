using System;

namespace IFT630_Project.Interfaces
{
    public interface IBlock
    {
        uint TimeStamp { get; set; }
        byte[] PreviousHash { get; set; }
        byte[] MerkelRootHash { get; }
        uint Nonce { get; set; }
        string Data { get; set; }
        uint Version { get; set; }
        int Difficulte { get; set; }

        byte[] BlockHashFormat();
        string BlockStringFormat();
        void SetMerkleHash(byte[] hash);
        void ChangeGuess(byte[] latestHash, uint newNonce);

    }
}