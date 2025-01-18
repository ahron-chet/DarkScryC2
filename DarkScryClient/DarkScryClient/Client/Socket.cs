using DarkScryClient.Security.Protocls;
using System;
using System.Net.Sockets;
using System.Reflection.Emit;
using System.Runtime.InteropServices;

namespace DarkScryClient.Client
{
	[StructLayout(LayoutKind.Sequential, Pack = 1)]
	public struct SocketMessageHeader
	{
		public DarkScryOpCode Opcode;
		public short RequestId;
		public int BodyLength;
	}

	public class SocketMessage
	{
		public DarkScryOpCode Opcode { get; set; }
		public short RequestId { get; set; }
		public int BodyLength { get; set; }
		public byte[] Body { get; set; }


		public SocketMessage(DarkScryOpCode opcode, short requestId, int bodyLength, byte[] body)
		{
			Opcode = opcode;
			RequestId = requestId;
			BodyLength = bodyLength;
			Body = body;
		}
	}

	internal class DarkScrySocket : IDisposable
	{
		private TcpClient client;
		private NetworkStream stream;
		private readonly string serverIP;
		private readonly int port;
		private bool disposed;

		public DarkScrySocket(string serverIP, int port)
		{
			this.serverIP = serverIP;
			this.port = port;
		}

		public bool Connect()
		{
			try
			{
				client = new TcpClient(serverIP, port);
				stream = client.GetStream();
				return true;
			}
			catch
			{
				return false;
			}
		}

		public void SendMessage(byte[] message, DarkScryOpCode opcode = 0, short requestId = 0, bool sendHeaders = true)
		{
			try
			{
				if (sendHeaders)
				{
					var header = new SocketMessageHeader
					{
						Opcode = opcode,
						RequestId = requestId,
						BodyLength = message.Length
					};

					var headerBytes = Tools.StructToBytes(header);
					stream.Write(headerBytes, 0, headerBytes.Length);
				}

				stream.Write(message, 0, message.Length);
			}
			catch (Exception ex)
			{
				Console.WriteLine($"Error while sending message: {ex.Message}");
			}
		}

		public SocketMessage ReceiveMessage()
		{
			try
			{
				var headerSize = Marshal.SizeOf(typeof(SocketMessageHeader));
				var headerBuffer = new byte[headerSize];
				stream.Read(headerBuffer, 0, headerSize);

				var header = Tools.BytesToStruct<SocketMessageHeader>(headerBuffer);
				var messageSize = header.BodyLength;

				var messageBuffer = new byte[messageSize];
				var bytesRead = 0;
				while (bytesRead < messageSize)
				{
					bytesRead += stream.Read(messageBuffer, bytesRead, messageSize - bytesRead);
				}

				return new SocketMessage(header.Opcode, header.RequestId, messageSize, messageBuffer);
			}
			catch (Exception ex)
			{
				Console.WriteLine($"Error while receiving message: {ex.Message}");
				return null;
			}
		}

		public void Dispose()
		{
			Dispose(true);
			GC.SuppressFinalize(this);
		}

		protected virtual void Dispose(bool disposing)
		{
			if (!disposed)
			{
				if (disposing)
				{
					try
					{
						stream?.Close();
						stream?.Dispose();
						client?.Close();
						client?.Dispose();
					}
					catch (Exception ex)
					{
						Console.WriteLine($"Error during disposal: {ex.Message}");
					}
				}
				disposed = true;
			}
		}
	}
}
