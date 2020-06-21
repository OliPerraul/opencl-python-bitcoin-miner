using System;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using IFT630_Project.Interfaces;

namespace IFT630_Project
{
    public class Block : IBlock
    {
        public uint TimeStamp { get; set; }
        public byte[] PreviousHash { get; set; }
        public byte[] MerkelRootHash { get; private set; }
        public uint Nonce { get; set; }
        public uint Version { get; set; }
        public int Difficulte { get; set; }
        public string Data { get; set; }

        public Block()
        {
        }

        public void ChangeGuess(byte[] latestHash, uint newNonce)
        {
            PreviousHash = latestHash;
            Nonce = newNonce;
        }

        public byte[] BlockHashFormat()
        {
            var blockBytes =  BitConverter.GetBytes(Version).Concat(PreviousHash)
                .Concat(MerkelRootHash).Concat(BitConverter.GetBytes(TimeStamp))
                .Concat(BitConverter.GetBytes(Difficulte)).Concat(BitConverter.GetBytes(Nonce)).ToArray();
            var t = blockBytes.ToHex().ToLower();
            return blockBytes;
        }

        public string BlockStringFormat()
        {
            return $"{Version}{PreviousHash.ToHex()}{MerkelRootHash.ToHex()}{TimeStamp}{Difficulte}{Nonce}";
        }

        public void SetMerkleHash(byte[] hash)
        {
            MerkelRootHash = hash;
        }
    }
}