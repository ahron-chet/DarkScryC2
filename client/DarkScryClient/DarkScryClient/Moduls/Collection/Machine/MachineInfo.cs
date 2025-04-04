using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.NetworkInformation;
using System.Runtime.InteropServices;


namespace DarkScryClient.Moduls.Collection
{
	

	internal class MachineInfo
	{

		internal static class BasicMachineInfoRetriever
		{
			#region Interop and Helpers

			// For retrieving total system memory:
			[StructLayout(LayoutKind.Sequential, CharSet = CharSet.Auto)]
			private class MEMORYSTATUSEX
			{
				public uint dwLength;
				public ulong ullTotalPhys;
				public ulong ullAvailPhys;
				public ulong ullTotalPageFile;
				public ulong ullAvailPageFile;
				public ulong ullTotalVirtual;
				public ulong ullAvailVirtual;
				public ulong ullAvailExtendedVirtual;

				public MEMORYSTATUSEX()
				{
					this.dwLength = (uint)Marshal.SizeOf(typeof(MEMORYSTATUSEX));
				}
			}

			[DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
			private static extern bool GlobalMemoryStatusEx([In, Out] MEMORYSTATUSEX lpBuffer);

			private static ulong GetTotalPhysicalMemoryBytes()
			{
				var memStatus = new MEMORYSTATUSEX();
				if (!GlobalMemoryStatusEx(memStatus))
					throw new System.ComponentModel.Win32Exception();

				return memStatus.ullTotalPhys;
			}

			// For enumerating GPU(s) / display adapters:
			[DllImport("user32.dll", CharSet = CharSet.Auto)]
			private static extern bool EnumDisplayDevices(
				string lpDevice,
				uint iDevNum,
				ref DISPLAY_DEVICE lpDisplayDevice,
				uint dwFlags
			);

			[StructLayout(LayoutKind.Sequential, CharSet = CharSet.Auto)]
			private struct DISPLAY_DEVICE
			{
				public int cb;
				[MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
				public string DeviceName;
				[MarshalAs(UnmanagedType.ByValTStr, SizeConst = 128)]
				public string DeviceString;
				public int StateFlags;
				[MarshalAs(UnmanagedType.ByValTStr, SizeConst = 128)]
				public string DeviceID;
				[MarshalAs(UnmanagedType.ByValTStr, SizeConst = 128)]
				public string DeviceKey;
			}

			private static List<string> GetAllGraphicsAdapters()
			{
				var gpus = new List<string>();
				var dd = new DISPLAY_DEVICE();
				dd.cb = Marshal.SizeOf(dd);

				uint id = 0;
				while (EnumDisplayDevices(null, id, ref dd, 0))
				{
					// "DeviceString" is typically the GPU name
					// You can also check dd.StateFlags to filter.
					if (!string.IsNullOrEmpty(dd.DeviceString))
					{
						gpus.Add(dd.DeviceString.Trim());
					}
					id++;
					dd.cb = Marshal.SizeOf(dd); // must reset before each call
				}

				return gpus;
			}

			#endregion
			public static Schemas.MachineSchema.BasicMachineInfo GetBasicMachineInfo()
			{
				var info = new Schemas.MachineSchema.BasicMachineInfo
				{
					HostName = Environment.MachineName,
					PrimaryIP = GetPrimaryIPv4(),
					AgentStatus = "Active and Monitoring",
					LastLogin = UsersInfo.GetCurrentUser(),
				};

				// 1. Get OS info from registry
				var osName = Registry.GetValue(
					@"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion",
					"ProductName",
					null) as string ?? "Unknown OS";

				// Additional OS details, if desired:
				var releaseId = Registry.GetValue(
					@"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion",
					"ReleaseId",
					null) as string ?? "UnknownReleaseId";

				var displayVersion = Registry.GetValue(
					@"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion",
					"DisplayVersion",
					null) as string ?? "UnknownDisplayVersion";

				info.OperatingSystem = osName;
				info.OSVersionDetail = $"ReleaseId={releaseId}, DisplayVersion={displayVersion}";

				// 2. CPU name from registry
				var cpuName = Registry.GetValue(
					@"HKEY_LOCAL_MACHINE\HARDWARE\DESCRIPTION\System\CentralProcessor\0",
					"ProcessorNameString",
					null) as string ?? "Unknown CPU";
				info.CPU = cpuName.Trim();

				// 3. Total RAM via GlobalMemoryStatusEx
				ulong totalMemBytes = GetTotalPhysicalMemoryBytes();
				double totalMemGB = totalMemBytes / (1024.0 * 1024.0 * 1024.0);
				info.RAM = $"{totalMemGB:F2} GB";

				// 4. Disk size (for C: drive or system drive)
				DriveInfo systemDrive = DriveInfo.GetDrives()
					.FirstOrDefault(d => d.Name.Equals(@"C:\", StringComparison.OrdinalIgnoreCase) && d.IsReady);

				if (systemDrive != null)
				{
					double diskSizeGB = systemDrive.TotalSize / (1024.0 * 1024.0 * 1024.0);
					info.Disk = $"{diskSizeGB:F0} GB {systemDrive.DriveFormat}";
				}
				else
				{
					info.Disk = "Unknown Disk";
				}

				// 5. GPU (Enumerate all display devices, pick first or join them)
				var allGpus = GetAllGraphicsAdapters();
				info.GPU = allGpus.Count > 0
					? string.Join(", ", allGpus.Distinct())
					: "Unknown GPU";

				info.LogedInSessions = UsersInfo.GetAllActiveUserSessions().Values.ToArray();

				return info;
			}

			private static string GetPrimaryIPv4()
			{
				// You can also do DNS: 
				// var host = Dns.GetHostName();
				// var ip = Dns.GetHostEntry(host).AddressList.FirstOrDefault(...);
				// But let's show a NetworkInterface approach:

				foreach (var ni in NetworkInterface.GetAllNetworkInterfaces())
				{
					if (ni.OperationalStatus == OperationalStatus.Up &&
						ni.NetworkInterfaceType != NetworkInterfaceType.Loopback &&
						ni.NetworkInterfaceType != NetworkInterfaceType.Tunnel)
					{
						var ipProps = ni.GetIPProperties();
						foreach (var ua in ipProps.UnicastAddresses)
						{
							if (ua.Address.AddressFamily == System.Net.Sockets.AddressFamily.InterNetwork)
							{
								return ua.Address.ToString();
							}
						}
					}
				}

				return "N/A";
			}
		}
	}
}
