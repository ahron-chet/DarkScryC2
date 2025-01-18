using DarkScryClient.Client;
using DarkScryClient.Moduls.Collection;
using System;
using System.Text.Json;


class Program
{

	static void Main()
	{
		// test_crypt.test_rsa();
		// socket_test.run_test();
		// test_command_manager.test_whoami();

		using (Client client = new Client())
		{
			client.Start();
		}
	}
}


