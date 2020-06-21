using System;
using System.Buffers.Text;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices.ComTypes;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using IFT630_Project.Interfaces;
using Microsoft.Extensions.DependencyInjection;

namespace IFT630_Project
{
    class Program
    {
        static void Main(string[] args)
        {
            var serviceProvider = RegisterServices();

            var difficulty = GetDifficultyFromUser();
            var difficultyService = serviceProvider.GetService<IDifficulty>();
            difficultyService.SetDifficulty(difficulty);

            var workMode = GetWorkModeFromUser();
            var workerFactory = serviceProvider.GetService<IWorkerFactory>();
            var worker = workerFactory.CreateWorker(workMode, serviceProvider);
            
            worker.Execute();
        }

        private static WorkerType GetWorkModeFromUser()
        {
            Console.WriteLine("Enter Work Mode: 1-Sequential, 2-Parallel, 3-GPU");
            var workMode = Console.ReadLine();
            var workerType = Int32.Parse(workMode);
            return (WorkerType) workerType;
        }



        private static int GetDifficultyFromUser()
        {
            Console.WriteLine("Enter Difficulty: ");
            var difficulty = Console.ReadLine();
            return Int32.Parse(difficulty);
            
        }

       
        private static ServiceProvider RegisterServices()
        {
            var services = new ServiceCollection()
                .AddTransient<IHashingService, HashingService>()
                .AddSingleton<IBlockchainService, BlockchainService>()
                .AddTransient<ITransactionService, TransactionService>()
                .AddSingleton<IWorkerFactory, WorkerFactory>()
                .AddSingleton<IDifficulty, Difficulty>()
                .BuildServiceProvider();
            return services;
        }
    }
}