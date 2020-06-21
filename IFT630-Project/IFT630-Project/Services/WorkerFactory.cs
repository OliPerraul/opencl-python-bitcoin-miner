using System;
using System.Collections.Generic;
using IFT630_Project.Interfaces;
using Microsoft.Extensions.DependencyInjection;

namespace IFT630_Project
{
    public class WorkerFactory : IWorkerFactory
    {
        public IWorker CreateWorker(WorkerType workerType, ServiceProvider serviceProvider)
        {
            var blockchainService = serviceProvider.GetService<IBlockchainService>();
            var hashingService = serviceProvider.GetService<IHashingService>();
            
            switch (workerType)
            {
                case WorkerType.Sequential:
                    return new SequentialWorker(blockchainService, hashingService, 0);
                case WorkerType.Parallel:
                    var numberOfWorkers = GetWorkersFromUser();
                    var sequentialsWorkers = new List<SequentialWorker>();
                    for (var i = 0; i < numberOfWorkers; i++)
                    {
                        sequentialsWorkers.Add(new SequentialWorker(blockchainService, hashingService, i));
                    }
                    return new ParallelWorker(blockchainService, hashingService, sequentialsWorkers);
                case WorkerType.GPU:
                    return new GpuWorker(blockchainService, hashingService);
                default:
                    throw new ArgumentOutOfRangeException(nameof(workerType), workerType, null);
            }
        }
        
        private static int GetWorkersFromUser()
        {
            Console.WriteLine("Enter number of workers: ");
            var workers = Console.ReadLine();
            return Int32.Parse(workers);
        }
    }
}