using System;
using System.IO;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace DarkScryClient.Client
{
	internal class WsClient : IDisposable
	{
		private readonly Uri _serverUri;
		private ClientWebSocket _websocket;
		private bool _running;
		private readonly CommandHandler _command;

		public WsClient(string serverUri)
		{
			_serverUri = new Uri(serverUri);
			_websocket = new ClientWebSocket();
			_command = new CommandHandler();
		}

		public async Task StartAsync()
		{
			Console.WriteLine($"Connecting to {_serverUri}...");
			await _websocket.ConnectAsync(_serverUri, CancellationToken.None);
			Console.WriteLine("Connected!");

			_running = true;
			await ReadLoopAsync();
		}

		private async Task ReadLoopAsync()
		{
			while (_running && _websocket.State == WebSocketState.Open)
			{
				string message;
				try
				{
					message = await ReadFullMessageAsync();
					if (message == null) break;
				}
				catch (WebSocketException wse)
				{
					Console.WriteLine($"WebSocket error: {wse.Message}");
					break;
				}

				await _command_handlar(message);
			}

			_running = false;
			Console.WriteLine("Read loop ended.");
		}

		private async Task<string> ReadFullMessageAsync()
		{
			var buffer = new byte[1024 * 4];
			var ms = new MemoryStream();

			while (true)
			{
				WebSocketReceiveResult result = await _websocket.ReceiveAsync(
					new ArraySegment<byte>(buffer),
					CancellationToken.None
				);

				if (result.MessageType == WebSocketMessageType.Close)
				{
					Console.WriteLine("Server initiated close. Closing...");
					await _websocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Closing", CancellationToken.None);
					return null;
				}

				ms.Write(buffer, 0, result.Count);

				if (result.EndOfMessage)
					break;
			}

			return Encoding.UTF8.GetString(ms.ToArray());
		}

		private async Task _command_handlar(string message)
		{
			Console.WriteLine($"[WSClient] Received: {message}");
			ArraySegment<byte> res = new ArraySegment<byte>(_command.RunCommand(message));
			await _websocket.SendAsync(res, WebSocketMessageType.Text, true, CancellationToken.None);
		}

		public async Task StopAsync()
		{
			_running = false;
			if (_websocket != null && _websocket.State == WebSocketState.Open)
			{
				Console.WriteLine("Closing WebSocket...");
				await _websocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Client closing", CancellationToken.None);
			}
			_websocket.Dispose();
			Console.WriteLine("WebSocket closed.");
		}

		public void Dispose()
		{
			_websocket?.Dispose();
		}
	}
}
