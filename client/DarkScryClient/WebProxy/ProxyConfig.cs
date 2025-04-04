namespace WebProxy
{
	public class WebSocketDoubleProxyConfig
	{
		public string Name { get; set; } = "ProxyRoute";

		// Port where the BROWSER connects
		public int BrowserPort { get; set; } = 5000;

		// Port where the INTERNAL CLIENT (agent) connects
		public int ClientPort { get; set; } = 8765;
	}
}
