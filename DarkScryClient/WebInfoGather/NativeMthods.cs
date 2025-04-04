using System.Runtime.InteropServices;


namespace WebInfoGather
{
	internal class NativeMthods
	{

		public static class CryptographyHelper
		{
			public const uint CRYPTPROTECT_LOCAL_MACHINE = 0x4;

			[DllImport("CryptographyHelper.dll", CharSet = CharSet.Ansi, CallingConvention = CallingConvention.Cdecl)]
			private static extern IntPtr DpapiUnprotectBase64(string base64Encrypted, uint cryptProtection);

			[DllImport("CryptographyHelper.dll", CallingConvention = CallingConvention.Cdecl)]
			private static extern void current_free(IntPtr ptr);

			public static string DpapiUnprotectBase64Wrapper(string base64Encrypted, uint cryptProtection)
			{
				IntPtr nativePtr = DpapiUnprotectBase64(base64Encrypted, cryptProtection);

				if (nativePtr == IntPtr.Zero)
					throw new Exception(
						$"Failed to unprotect dpapi protcted data: {Marshal.GetLastWin32Error()}");

				try
				{
					return Marshal.PtrToStringAnsi(nativePtr);
				}
				finally
				{
					current_free(nativePtr);
				}
			}
		}
	}
}
