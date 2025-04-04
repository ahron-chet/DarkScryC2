using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DarkScryClient.Moduls.Collection.Schemas
{
	internal class MachineSchema
	{
		public class BasicMachineInfo
		{
			public string HostName { get; set; }
			public string OperatingSystem { get; set; }
			public string OSVersionDetail { get; set; }
			public string CPU { get; set; }
			public string RAM { get; set; }
			public string Disk { get; set; }
			public string PrimaryIP { get; set; }
			public string GPU { get; set; }
			public string AgentStatus { get; set; }
			public string LastLogin { get; set; }
			public string[] LogedInSessions { get; set; }
		}
	}
}
