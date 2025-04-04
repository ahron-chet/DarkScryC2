using System.Runtime.Serialization;


namespace DarkScryClient.Models
{
	[DataContract]
	public class AgentConnection
	{
		[DataMember(Name = "agent_id")]
		public string AgentId { get; set; }
		[DataMember(Name = "key")]
		public string Key { get; set; }
	}
}
