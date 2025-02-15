using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;


namespace DarkScryClient.Utils
{
	public static class JsonHelper
	{
		public static string GetStringOrDefault(
			this JsonElement element,
			string propertyName,
			string defaultValue = ""
		)
		{
			if (element.TryGetProperty(propertyName, out JsonElement prop)
				&& prop.ValueKind == JsonValueKind.String)
			{
				string value = prop.GetString();

				return value;
			}
			return defaultValue;
		}
	}
}
