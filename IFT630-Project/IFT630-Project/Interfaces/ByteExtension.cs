using System;

namespace IFT630_Project.Interfaces
{
    public static class ByteExtension
    {
        public static string ToHex(this byte[] ar)
        {
            return BitConverter.ToString(ar).Replace("-", "");
        }
    }
}