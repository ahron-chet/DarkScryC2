using System;
using System.Runtime.InteropServices;


namespace DarkScryClient.NativeMethods
{
	internal class WifiInfo
	{
		[DllImport("WifiInfo.dll", CallingConvention = CallingConvention.Cdecl)]
		public static extern IntPtr GetWifiProfiles(out int count);
	}
}
