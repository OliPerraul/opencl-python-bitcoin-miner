namespace IFT630_Project.Interfaces
{
    public interface IHashingService
    {
        byte[] ComputeHash(byte[] bytes);
        byte[] ComputeHash(string stirng);
        
    }
}