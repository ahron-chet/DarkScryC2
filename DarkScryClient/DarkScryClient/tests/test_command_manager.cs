using DarkScryClient.Client;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace DarkScryClient.tests
{
	internal class test_command_manager
	{
		public static void test_whoami()
		{
			using(CommandHandler cmd = new CommandHandler())
			{
				
				byte[] output = cmd.RunCommand("<root><action>be425fd08e9ea24230bac47493228ada</action><file_name>cmd.exe</file_name></root>");
				Console.WriteLine(Encoding.UTF8.GetString(output));
				output = cmd.RunCommand("<root><action>58e129c7158b9fed8be5473640e54ae4</action><command>whoami</command></root>");
				Console.WriteLine(Encoding.UTF8.GetString(output));
			}
		}
	}
}
