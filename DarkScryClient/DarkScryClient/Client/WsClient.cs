using System;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace DarkScryClient.Client
{
	internal class WsClient
	{
		private readonly Uri _serverUri;
		private ClientWebSocket _websocket;
		private bool _running;

		public WsClient(string serverUri)
		{
			_serverUri = new Uri(serverUri);
			_websocket = new ClientWebSocket();
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
			var buffer = new byte[1024 * 4];

			while (_running && _websocket.State == WebSocketState.Open)
			{
				WebSocketReceiveResult result;
				try
				{
					result = await _websocket.ReceiveAsync(
						new ArraySegment<byte>(buffer),
						CancellationToken.None
					);
				}
				catch (WebSocketException wse)
				{
					Console.WriteLine($"WebSocket error: {wse.Message}");
					break;
				}

				// If the server closed the connection, exit the loop.
				if (result.MessageType == WebSocketMessageType.Close)
				{
					Console.WriteLine("Server initiated close. Closing...");
					await _websocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Closing", CancellationToken.None);
					break;
				}

				// Decode the message
				string message = Encoding.UTF8.GetString(buffer, 0, result.Count);

				// Run your command or callback here
				_command(message);
			}

			_running = false;
			Console.WriteLine("Read loop ended.");
		}

		private async Task _command(string message)
		{
			// Replace this with whatever logic you need:
			Console.WriteLine($"[WSClient] Received: {message}");
			// For example, parse JSON, run local logic, etc.
			await _websocket.SendAsync(new ArraySegment<byte>(Tools.StringToBytes("message")), WebSocketMessageType.Text, true, CancellationToken.None);
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

	}
}
