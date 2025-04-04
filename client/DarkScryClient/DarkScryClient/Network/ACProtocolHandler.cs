using System;
using DarkScryClient.Utils;
using DarkScryClient.Security.Cryptography;
using DarkScryClient.Client;
using DarkScryClient.Models;
using DarkScryClient.Security.Protocls;
using System.Linq;
using System.Text;

namespace DarkScryClient.Security.Protocols
{
	internal class ACProtocolHandler : IDisposable
	{
		private readonly string _serverIp;
		private readonly int _serverPort;
		private readonly Logger _logger;

		private DarkScrySocket _socket;
		private AESCyrpto _aes;

		private bool _disposed;

		public ACProtocolHandler(string serverIp, int serverPort, Logger logger)
		{
			_serverIp = serverIp;
			_serverPort = serverPort;
			_logger = logger;
		}

		public bool ConnectAndHandshake()
		{
			// 1) connect socket
			_socket = new DarkScrySocket(_serverIp, _serverPort);
			if (!_socket.Connect())
			{
				_logger.Log("Failed to connect to server", Logger.LogLevel.Error);
				return false;
			}

			// 2) create random AES key
			var key = AESCyrpto.RandomKey();
			var iv = AESCyrpto.randomIV(key);
			_aes = new AESCyrpto(key, iv);

			// 3) build handshake object
			var agent = new AgentConnection
			{
				AgentId = Config.agent_id,
				Key = Security.Cryptography.Utils.BytesToHexDigest(key)
			};

			// 4) RSA encrypt
			var rsa = new AsymetricCryptography(Config.PublicKey);
			var serialized = Tools.SerializeToJson(agent);
			var encrypted = rsa.Encrypt(serialized);

			// 5) send raw => no header
			_socket.SendMessage(encrypted, sendHeaders: false);
			return true;
		}

		public DSMessage ReceiveMessage()
		{
			SocketMessage rawMsg = null;
			DarkScryOpCode op = DarkScryOpCode.KeepAlive; 
			while (op == DarkScryOpCode.KeepAlive)
			{
				rawMsg = _socket.ReceiveMessage();
				if (rawMsg == null)
				{
					return null;
				}
				op = rawMsg.Opcode;

			}

			try
			{
				byte[] plain = _aes.Decrypt(rawMsg.Body);
				if (plain.Length < ACProtocol.PaddedSum)
				{
					_logger.Log("Plaintext too short for sum/padding => ignoring", Logger.LogLevel.Error);
					return null;
				}

				// first 4 => sum, skip remainder up to 16 => rest is real body
				byte[] actualSum = new byte[4];
				Buffer.BlockCopy(plain, 0, actualSum, 0, 4);
				Console.WriteLine(string.Join(", ", actualSum));
				int bodyLen = plain.Length - ACProtocol.PaddedSum;
				byte[] realBody = new byte[bodyLen];
				Buffer.BlockCopy(plain, ACProtocol.PaddedSum, realBody, 0, bodyLen);

				// compute expected sum => no random pad
				Console.WriteLine($"Recived message {rawMsg.Opcode} req_id:{(int)rawMsg.RequestId}");
				byte[] expectedSum = ACProtocol.ComputeHeaderChecksum(rawMsg.Opcode, rawMsg.RequestId, false);

				if (!Tools.ArraysEqual(actualSum, expectedSum))
				{
					_logger.Log("Checksum mismatch => ignoring message", Logger.LogLevel.Error);
					// return null;
				}

				_logger.Log($"body: {rawMsg.Opcode}, req_id:${rawMsg.RequestId}, body:{System.Text.Encoding.UTF8.GetString(realBody)}");
				return new DSMessage(rawMsg.Opcode, rawMsg.RequestId, realBody);
			}
			catch (Exception ex)
			{
				_logger.Log($"ReceiveMessage decrypt error: {ex.Message}", Logger.LogLevel.Error);
				return null;
			}
		}

		public void SendDSMessage(DSMessage dsMsg)
		{
			Console.WriteLine($"Sending message: {dsMsg.OpCode}, req_id:{(int)dsMsg.RequestId}");
			// if keepalive => no encryption => bodyLen=0
			if (dsMsg.OpCode == DarkScryOpCode.KeepAlive && dsMsg.Body?.Length == 0)
			{
				_socket.SendMessage(Array.Empty<byte>(), dsMsg.OpCode, dsMsg.RequestId);
				return;
			}

			// otherwise => compute sum + random pad => then encrypt
			byte[] sum = ACProtocol.ComputeHeaderChecksum(dsMsg.OpCode, dsMsg.RequestId, true);
			byte[] plain = new byte[sum.Length + dsMsg.Body.Length];

			Buffer.BlockCopy(sum, 0, plain, 0, sum.Length);
			Buffer.BlockCopy(dsMsg.Body, 0, plain, sum.Length, dsMsg.Body.Length);

			byte[] cipher = _aes.Encrypt(plain);
			_socket.SendMessage(cipher, dsMsg.OpCode, dsMsg.RequestId);
		}

		public void Dispose()
		{
			if (!_disposed)
			{
				_socket?.Dispose();
				_disposed = true;
			}
		}
	}
}
