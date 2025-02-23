using System;
using System.Net;
using System.Net.WebSockets;
using System.Threading;
using System.Threading.Tasks;

namespace WebProxy
{
	public class WebSocketDoubleProxy : IDisposable
	{
		private readonly WebSocketDoubleProxyConfig _config;

		private HttpListener _browserListener;
		private HttpListener _clientListener;

		private WebSocket _browserWs;
		private WebSocket _clientWs;

		private bool _disposed;
		private Task _browserTask;
		private Task _clientTask;

		private readonly object _lock = new object();

		public WebSocketDoubleProxy(WebSocketDoubleProxyConfig config)
		{
			_config = config;
		}

		/// <summary>
		/// Starts listening on two ports in parallel:
		///  - BrowserPort for the browser
		///  - ClientPort for the internal client
		/// </summary>
		public async Task StartAsync()
		{
			if (_disposed)
				throw new ObjectDisposedException(nameof(WebSocketDoubleProxy));

			// 1) Prepare HttpListener for browser side
			_browserListener = new HttpListener();
			_browserListener.Prefixes.Add($"http://localhost:{_config.BrowserPort}/");
			_browserListener.Start();
		
			Console.WriteLine($"[{_config.Name}] Browser listener started on port {_config.BrowserPort}.");

			// 2) Prepare HttpListener for client side
			_clientListener = new HttpListener();
			_clientListener.Prefixes.Add($"http://localhost:{_config.ClientPort}/");
			_clientListener.Start();
			Console.WriteLine($"[{_config.Name}] Client listener started on port {_config.ClientPort}.");

			// 3) Run loops in background tasks
			_browserTask = AcceptBrowserLoopAsync();
			_clientTask = AcceptClientLoopAsync();

			// Wait for either to end (e.g., if disposed or an error occurs)
			await Task.WhenAny(_browserTask, _clientTask);

			Console.WriteLine($"[{_config.Name}] One of the listener loops ended.");
		}

		private async Task AcceptBrowserLoopAsync()
		{
			try
			{
				while (!_disposed)
				{
					var context = await _browserListener.GetContextAsync();
					if (!context.Request.IsWebSocketRequest)
					{
						context.Response.StatusCode = 400;
						context.Response.Close();
						continue;
					}

					var wsContext = await context.AcceptWebSocketAsync(null);
					var ws = wsContext.WebSocket;
					Console.WriteLine($"[{_config.Name}] Browser connected.");

					lock (_lock)
					{
						if (_browserWs != null && _browserWs.State == WebSocketState.Open)
						{
							_browserWs.CloseAsync(
								WebSocketCloseStatus.NormalClosure,
								"Replacing existing browser socket",
								CancellationToken.None
							).Wait();
						}
						_browserWs = ws;
						TryPairAndRelay();
					}
				}
			}
			catch (HttpListenerException ex)
			{
				Console.WriteLine($"[{_config.Name}] BrowserLoop HttpListenerException: {ex.Message}");
			}
			catch (ObjectDisposedException)
			{
				// Expected on dispose
			}
			catch (Exception ex)
			{
				Console.WriteLine($"[{_config.Name}] BrowserLoop Exception: {ex}");
			}

			Console.WriteLine($"[{_config.Name}] AcceptBrowserLoop ended.");
		}

		private async Task AcceptClientLoopAsync()
		{
			try
			{
				while (!_disposed)
				{
					var context = await _clientListener.GetContextAsync();
					if (!context.Request.IsWebSocketRequest)
					{
						context.Response.StatusCode = 400;
						context.Response.Close();
						continue;
					}

					var wsContext = await context.AcceptWebSocketAsync(null);
					var ws = wsContext.WebSocket;
					Console.WriteLine($"[{_config.Name}] Client connected.");

					lock (_lock)
					{
						if (_clientWs != null && _clientWs.State == WebSocketState.Open)
						{
							_clientWs.CloseAsync(
								WebSocketCloseStatus.NormalClosure,
								"Replacing existing client socket",
								CancellationToken.None
							).Wait();
						}
						_clientWs = ws;
						TryPairAndRelay();
					}
				}
			}
			catch (HttpListenerException ex)
			{
				Console.WriteLine($"[{_config.Name}] ClientLoop HttpListenerException: {ex.Message}");
			}
			catch (ObjectDisposedException)
			{
				// Expected on dispose
			}
			catch (Exception ex)
			{
				Console.WriteLine($"[{_config.Name}] ClientLoop Exception: {ex}");
			}

			Console.WriteLine($"[{_config.Name}] AcceptClientLoop ended.");
		}

		/// <summary>
		/// If both browser and client have unpaired sockets, form a pair and relay traffic.
		/// </summary>
		private void TryPairAndRelay()
		{
			if (_browserWs != null && _clientWs != null)
			{
				var bws = _browserWs;
				var cws = _clientWs;

				// Clear out so we can accept new pairs
				_browserWs = null;
				_clientWs = null;

				Console.WriteLine($"[{_config.Name}] Formed a pair, starting relay...");
				Task.Run(() => RelayPairAsync(bws, cws));
			}
		}

		private static async Task RelayPairAsync(WebSocket browserWs, WebSocket clientWs)
		{
			var forwardBtoC = ForwardTraffic(browserWs, clientWs);
			var forwardCtoB = ForwardTraffic(clientWs, browserWs);

			await Task.WhenAny(forwardBtoC, forwardCtoB);

			if (browserWs?.State == WebSocketState.Open)
			{
				try { await browserWs.CloseAsync(WebSocketCloseStatus.NormalClosure, "Relay closing", CancellationToken.None); }
				catch { /* ignore */ }
			}
			if (clientWs?.State == WebSocketState.Open)
			{
				try { await clientWs.CloseAsync(WebSocketCloseStatus.NormalClosure, "Relay closing", CancellationToken.None); }
				catch { /* ignore */ }
			}
		}

		/// <summary>
		/// Forward traffic from inputWs to outputWs until the input closes or error occurs.
		/// </summary>
		private static async Task ForwardTraffic(WebSocket inputWs, WebSocket outputWs)
		{
			var buffer = new byte[8192];
			try
			{
				while (true)
				{
					var result = await inputWs.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);
					if (result.MessageType == WebSocketMessageType.Close)
					{
						break;
					}

					await outputWs.SendAsync(
						new ArraySegment<byte>(buffer, 0, result.Count),
						result.MessageType,
						result.EndOfMessage,
						CancellationToken.None
					);
				}
			}
			catch
			{
				// Typically ignore or log if needed
			}
		}

		public void Dispose()
		{
			if (_disposed) return;
			_disposed = true;

			_browserListener?.Stop();
			_browserListener?.Close();

			_clientListener?.Stop();
			_clientListener?.Close();
		}
	}
}
