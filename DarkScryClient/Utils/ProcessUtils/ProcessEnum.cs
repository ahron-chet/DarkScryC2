using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Security.Cryptography;


namespace Utils
{
	public class ProcessEnum
	{
		public static List<Dictionary<string, object>> EnumProcesses()
		{
			var sortedProcesses = Process.GetProcesses().OrderBy(p => p.ProcessName);
			var result = new List<Dictionary<string, object>>();

			foreach (Process process in sortedProcesses)
			{
				string identifier;
				try
				{
					identifier = GenIdentifier(process);
				}
				catch
				{
					continue;
				}

				var processInfo = new Dictionary<string, object>
				{
					["ProcessName"] = process.ProcessName,
					["ProcessId"] = process.Id,
					["MemoryUsage"] = process.WorkingSet64,
					["Owner"] = GetOwnerByPid((uint)process.Id),
					["WasInjected"] = WasInjected(identifier)
				};

				result.Add(processInfo);
			}

			return result;
		}

		public static string GetOwnerByPid(uint processId)
		{
			NativeMethods.GetUserNameByPid(processId, out IntPtr buffer);
			if (buffer == IntPtr.Zero) {
				return "Unknow";
			}
			string result = Marshal.PtrToStringUni(buffer);
			Marshal.FreeHGlobal(buffer);
			if (result != null && result.Length > 0)
			{
				return result;
			}
			return "Unknow";
		}

		private static bool WasInjected(string identifier)
		{
			return false;//Info.InjectedProcess.Contains(identifier);
		}

		public static string GenIdentifier(Process process)
		{
			string identifier = $"{process.Id}:{process.StartTime}";
			return Convert.ToBase64String(MD5.Create().ComputeHash(System.Text.Encoding.ASCII.GetBytes(identifier)));
		}
	}
}

