using System.Collections.Generic;
using System.Threading.Tasks;
using IFT630_Project.Interfaces;

namespace IFT630_Project
{
    public class ParallelWorker : AbstractWorker
    {
        private List<SequentialWorker> Workers { get; set; }
        public ParallelWorker(IBlockchainService blockchainService, IHashingService hashingService, List<SequentialWorker> workers) : base(blockchainService, hashingService)
        {
            Workers = workers;
        }

        public override void Execute()
        {
            Parallel.ForEach(Workers, w => w.Execute());
        }
    }
}