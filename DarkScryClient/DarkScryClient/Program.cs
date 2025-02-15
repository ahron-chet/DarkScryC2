using DarkScryClient;
using DarkScryClient.Client;
using DarkScryClient.Moduls.Collection;
using DarkScryClient.Moduls.Collection.Files;
using DarkScryClient.tests;
using System.IO;
using System.Text.Json;
using System.Threading.Tasks;


class Program
{

	static async Task Main()
	{
		
		WsClient wsclient = new WsClient($"ws://127.0.0.1:8765/{Config.agent_id}");
		await wsclient.StartAsync();
		return;
		
		// legacy acp protocol
		using (Client client = new Client())
		{
			client.Start();
		}
	}
}


