using System;
using System.Security.Cryptography;
using System.Text;

namespace DarkScryClient.Security.Cryptography
{
	internal enum HashAlgorithmType
	{
		MD5,
		SHA1,
		SHA256,
		SHA384,
		SHA512
	}

	internal class Utils
	{
		public static byte[] Gethash(HashAlgorithmType algoType, byte[] data)
		{
			HashAlgorithm hasher;

			// Traditional switch statement
			switch (algoType)
			{
				case HashAlgorithmType.MD5:
					hasher = MD5.Create();
					break;
				case HashAlgorithmType.SHA1:
					hasher = SHA1.Create();
					break;
				case HashAlgorithmType.SHA256:
					hasher = SHA256.Create();
					break;
				case HashAlgorithmType.SHA384:
					hasher = SHA384.Create();
					break;
				case HashAlgorithmType.SHA512:
					hasher = SHA512.Create();
					break;
				default:
					throw new ArgumentOutOfRangeException("Unsupported hash algorithm");
			}

			return hasher.ComputeHash(data);
		}

		public static byte[] RandomBytes(int n)
		{
			byte[] bytes = new byte[n];
			using (RandomNumberGenerator rng = RandomNumberGenerator.Create())
			{
				rng.GetBytes(bytes);
			}
			return bytes;
		}

		public static string BytesToHexDigest(byte[] hashBytes)
		{
			StringBuilder hexString = new StringBuilder(hashBytes.Length * 2);
			foreach (byte b in hashBytes)
			{
				hexString.Append(b.ToString("x2")); // Convert each byte to its hexadecimal representation
			}
			return hexString.ToString();
		}
	}
}
