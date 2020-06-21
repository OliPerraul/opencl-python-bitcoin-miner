using System;
using System.Linq;
using System.Text;
using IFT630_Project.Interfaces;

namespace IFT630_Project
{
    
    public class TransactionService : ITransactionService
    {   
        private Random Random { get; }
        private const string Base58Chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmopqrstuvwxyz";
        private const int TransactionsLength = 600;
        private IHashingService HashingService { get; }
        public TransactionService(IHashingService hashingService)
        {
            HashingService = hashingService;
            Random = new Random();
        }
        public byte[] PendingTransactionHash()
        {
            var sb = new StringBuilder();
            for (var i=0; i < TransactionsLength; i++)
            {
                var randIndex = Random.Next(0, Base58Chars.Length-1);
                sb.Append(Base58Chars[randIndex]);
            }
            var hashedTransaction = HashingService.ComputeHash(sb.ToString());
            return hashedTransaction;
        }
    }
}