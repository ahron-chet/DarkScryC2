

namespace WebProxy
{
	public class WebSocketProxyManager : IDisposable
	{
		private readonly List<WebSocketDoubleProxy> _proxies = new();

		public void AddProxy(WebSocketDoubleProxyConfig config)
		{
			_proxies.Add(new WebSocketDoubleProxy(config));
		}

		public async Task StartAllAsync()
		{
			// Start all proxies in parallel
			var tasks = new List<Task>();
			foreach (var proxy in _proxies)
			{
				tasks.Add(proxy.StartAsync());
			}

			// We do not await them here, because they run indefinitely
			// or until disposal. If you do want to wait, you could do:
			await Task.WhenAll(tasks);
		}

		public void Dispose()
		{
			foreach (var proxy in _proxies)
			{
				proxy.Dispose();
			}
			_proxies.Clear();
		}
	}
}
