using DarkScryClient;
using DarkScryClient.Client;
using System;
using System.Text.Json;
using System.Threading.Tasks;
using WebProxy;

class Program
{
	static async Task Main()
	{

		WsClient wsclient;
		if (Config.UseProxy)
		{
			switch (Config.ProxyKind)
			{
				case ProxyKindOptions.WebSocketBrowser:

					var manager = new WebSocketProxyManager();

					// Route #1
					manager.AddProxy(new WebSocketDoubleProxyConfig
					{
						Name = "ProxyRoute-A",
						BrowserPort = 5000,
						ClientPort = 8765
					});

					wsclient = new WsClient($"ws://localhost:8765/{Config.agent_id}");

					Task[] tasks = { manager.StartAllAsync(), wsclient.StartAsync() };
					await Task.WhenAll(tasks);
					return;
					// legacy acp protocol
					using (Client client = new Client())
					{
						client.Start();
					}
				default:
					throw new Exception("Unknow Proxy kind");
			}

		}
		else
		{
			wsclient = new WsClient($"ws://{Config.ServerIp}:876/{Config.agent_id}");
			await wsclient.StartAsync();
		}
	}
}


