using IFT630_Project.Interfaces;

namespace IFT630_Project
{
    public class Difficulty : IDifficulty
    {   
        public int DifficultyLevel { get; private set; }

        public Difficulty(int difficultyLevel = 1)
        {
            DifficultyLevel = difficultyLevel;
        }
        public void IncreaseDifficulty(int increaseAmount)
        {
            DifficultyLevel += increaseAmount;
        }

        public void LowerDifficulty(int lowerAmount)
        {
            DifficultyLevel = DifficultyLevel - lowerAmount <= 0 ? 1 : DifficultyLevel - lowerAmount;
        }

        public int GetDifficulty()
        {
            return DifficultyLevel;
        }

        public string TranslateDifficulty()
        {
            return new string('0', DifficultyLevel);
        }

        public void SetDifficulty(int difficulty)
        {
            DifficultyLevel = difficulty;
        }
    }
}