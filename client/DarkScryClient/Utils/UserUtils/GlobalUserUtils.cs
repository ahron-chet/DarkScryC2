using Microsoft.Win32;
using System.Management;

namespace Utils.UserUtils
{
	public class GlobalUserUtils
	{
		public static string GetUserSid()
		{
			string sid;
			string query = "SELECT UserName FROM Win32_ComputerSystem";
			using (ManagementObjectSearcher searcher = new ManagementObjectSearcher(query))
			{
				var username = (string)searcher.Get().Cast<ManagementBaseObject>().First()["UserName"];

				string[] res = username.Split('\\');
				if (res.Length != 2) throw new InvalidOperationException("Invalid username format.");

				string domain = res[0];
				string name = res[1];
				query = $"SELECT Sid FROM Win32_UserAccount WHERE Domain = '{domain}' AND Name = '{name}'";
				using (ManagementObjectSearcher searcher2 = new ManagementObjectSearcher(query))
				{
					sid = (string)searcher2.Get().Cast<ManagementBaseObject>().First()["Sid"];
				}
			}
			return sid;
		}

		public static string HomePath()
		{
			using (RegistryKey key = RegistryKey.OpenBaseKey(RegistryHive.LocalMachine, RegistryView.Default))
			{
				using (RegistryKey subkey = key.OpenSubKey($"Software\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList\\{GetUserSid()}"))
				{
					object value = subkey.GetValue("ProfileImagePath");
					if (value != null)
					{
						return value.ToString();
					}
				}
			}
			return null;
		}

	}
}

