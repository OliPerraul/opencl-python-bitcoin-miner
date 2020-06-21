using Microsoft.Extensions.DependencyInjection;

namespace IFT630_Project.Interfaces
{
    public interface IWorkerFactory
    {
        IWorker CreateWorker(WorkerType workerType, ServiceProvider serviceProvider);
    }
}