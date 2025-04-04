using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Text;
using System.Threading.Tasks;

namespace DarkScryClient.Models
{

	[DataContract]
	public class CommandOutput
	{
		[DataMember(Name = "type")]
		public string type { get; set; }
		[DataMember(Name = "output")]
		public string output { get; set; }
		[DataMember(Name = "status")]
		public int status { get; set; }
	}
}

