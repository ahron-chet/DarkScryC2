using System;
using System.Security.Cryptography;


namespace DarkScryClient.Security.Protocls
{
	public class DSMessage
	{
		public DarkScryOpCode OpCode { get; set; }
		public short RequestId { get; set; }
		public byte[] Body { get; set; }

		public DSMessage(DarkScryOpCode op, short req, byte[] body)
		{
			OpCode = op;
			RequestId = req;
			Body = body ?? System.Array.Empty<byte>();
		}
	}
	public enum DarkScryOpCode : byte
	{
		None = 0,
		KeepAlive = 1,
		CmdRequest = 3,
		CmdResponse = 4
	}
	internal class ACProtocol
	{

		public const int PaddedSum = 16; 
		public const int SizeOfPadding = 4;
		private const int sumPadding = PaddedSum - SizeOfPadding;
		private static readonly uint[] Crc32Table = InitializeCrc32Table();

		public static byte[] ComputeHeaderChecksum(DarkScryOpCode opcode, short requestId, bool _padd = true)
		{
			byte[] buffer = new byte[3];
			buffer[0] = (byte)opcode;
			BitConverter.GetBytes(requestId).CopyTo(buffer, 1);

			uint crc32 = ComputeCrc32(buffer);

			byte[] crcBytes = BitConverter.GetBytes(crc32);
			if (!_padd)
			{
				return crcBytes;
			}

			byte[] randomPadding = new byte[sumPadding];
			using (var rng = RandomNumberGenerator.Create())
			{
				rng.GetBytes(randomPadding);
			}

			byte[] result = new byte[crcBytes.Length + sumPadding];
			Array.Copy(crcBytes, result, crcBytes.Length);
			Array.Copy(randomPadding, 0, result, crcBytes.Length, sumPadding);

			return result;
		}

		private static uint ComputeCrc32(byte[] data)
		{
			uint crc = 0xFFFFFFFF;

			foreach (byte b in data)
			{
				uint tableIndex = (crc ^ b) & 0xFF;
				crc = (crc >> 8) ^ Crc32Table[tableIndex];
			}

			return ~crc;
		}

		private static uint[] InitializeCrc32Table()
		{
			const uint Polynomial = 0xEDB88320;
			uint[] table = new uint[256];

			for (uint i = 0; i < 256; i++)
			{
				uint crc = i;
				for (int j = 8; j > 0; j--)
				{
					if ((crc & 1) == 1)
					{
						crc = (crc >> 1) ^ Polynomial;
					}
					else
					{
						crc >>= 1;
					}
				}
				table[i] = crc;
			}

			return table;
		}
	}
}
