using System;
using System.Security.Cryptography;
using System.Text;
using IFT630_Project.Interfaces;

namespace IFT630_Project
{
    public class HashingService : IHashingService
    {
        private SHA256 Hasher { get; }

        public HashingService()
        {
            Hasher = SHA256.Create();    
        }
        public byte[] ComputeHash(byte[] bytes)
        {
            var hash =  Hasher.ComputeHash(bytes);
            return hash;
        }

        public byte[] ComputeHash(string stirng)
        {
            var bytes = Encoding.UTF8.GetBytes(stirng);
            return ComputeHash(bytes);
        }
    }
}