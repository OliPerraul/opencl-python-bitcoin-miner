namespace IFT630_Project.Interfaces
{
    public interface IDifficulty
    {
        void IncreaseDifficulty(int increaseAmount);
        void LowerDifficulty(int lowerAmount);
        int GetDifficulty();
        string TranslateDifficulty();
        void SetDifficulty(int difficulty);
    }
}