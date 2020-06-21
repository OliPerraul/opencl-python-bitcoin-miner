using System;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.IO.Compression;
using IFT630_Project.Interfaces;

namespace IFT630_Project
{
    public class GpuWorker : AbstractWorker
    {
        private ProcessStartInfo PythonProcess { get; set; }
        private int Id { get; set; }

        public GpuWorker(IBlockchainService blockchainService, IHashingService hashingService)
            : base(blockchainService,
                hashingService)
        {
            Id = 1;

            PythonProcess = ConfigurePythonProcess();
        }

        public override void Execute()
        {
            while (true)
            {
                var blockTemplate = NewGuessBlock(BlockchainService.GetLastestBlockHash());

                PythonProcess.Arguments =
                    $"blockchain.opencl.py {blockTemplate.Version} {blockTemplate.PreviousHash.ToHex()} {blockTemplate.MerkelRootHash.ToHex()} {blockTemplate.Difficulte}";
                using (var process = Process.Start(PythonProcess))
                {
                    using (var sr = process.StandardOutput)
                    {
                        var stderr = process.StandardError.ReadToEnd();
                        if (stderr != "")
                        {
                            Console.WriteLine(stderr);
                        }

                        var prevccc = blockTemplate.PreviousHash.ToHex();
                        var t = sr.ReadToEnd();
                        var result = t.Split("\r\n")[2].Split(";");
                        // var result = sr.ReadToEnd().Split(";");
                        var time = uint.Parse(result[0]);
                        var nonce = Convert.ToUInt32(result[1], 16);

                        blockTemplate.TimeStamp = time;
                        blockTemplate.Nonce = nonce;
                        BlockchainService.AddBlock(blockTemplate, Id);
                    }
                }
            }
        }

        private static ProcessStartInfo ConfigurePythonProcess()
        {
            var pythonProcess = new ProcessStartInfo();
            pythonProcess.FileName = Environment.GetEnvironmentVariable("python") ??
                                     throw new Exception("You need to set an environment variable named 'python'");

            pythonProcess.UseShellExecute = false;
            pythonProcess.CreateNoWindow = false;
            pythonProcess.RedirectStandardError = true;
            pythonProcess.RedirectStandardOutput = true;
            return pythonProcess;
        }
    }
}