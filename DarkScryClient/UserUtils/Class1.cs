using Microsoft.Win32;
using System.Security.Principal;

namespace UserUtils
{

	public class UserUtils
	{
		public static string GetUserSid()
		{
			return "";
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
		public static bool IsAdministrator()
		{
			WindowsIdentity identity = WindowsIdentity.GetCurrent();
			WindowsPrincipal principal = new WindowsPrincipal(identity);
			return principal.IsInRole(WindowsBuiltInRole.Administrator);
		}

		public static bool IsSystemUser()
		{
			var localSystemSid = new SecurityIdentifier(WellKnownSidType.LocalSystemSid, null);

			using (var identity = WindowsIdentity.GetCurrent())
			{
				return identity.User != null && identity.User.Equals(localSystemSid);
			}
		}
	}
	
}
