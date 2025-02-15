using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace DarkScryClient.Models
{
	internal class WifiInfoModels
	{
		[StructLayout(LayoutKind.Sequential)]
		public struct WifiProfileNative
		{
			public IntPtr ssid;
			public IntPtr xml;
		}
		public class BasicWifiInfo
		{
			public string SSIDName { get; set; }
			public string Password { get; set; }
			public string Authentication { get; set; }
			public string Cipher { get; set; }
		}
		public class WifiFullInfo
		{
			public string SSIDName { get; set; }
			public string xml { get; set; }
		}
	}
}
