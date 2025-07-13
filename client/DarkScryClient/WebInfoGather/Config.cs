

namespace DarkScryClient
{
	enum ProxyKindOptions
	{
		WebSocketBrowser = 0,
	}
	internal class Config
	{
		public static string agent_id = "8ec24819-1c1f-4e98-95d2-f86ceaeb339f";
		public static string MainShell = "cmd.exe";
		public static bool IsMainShellRuning = false;
                public static string ServerIp = "127.0.0.1";
                public static readonly string AgentName = "DarkScry Cleint";
                public static readonly string AgnetVersion = "1.0.0";

		public static readonly bool UseProxy = false;
		public static string ProxyHost = "localhost";
		public static readonly ProxyKindOptions ProxyKind = ProxyKindOptions.WebSocketBrowser;
	}
}
