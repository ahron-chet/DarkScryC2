using System.Text.Json;

namespace Utils
{
	public static class JsonHelper
	{
		public static string GetStringOrDefault(
			this JsonElement element,
			string propertyName,
			string defaultValue = "")
		{
			if (element.TryGetProperty(propertyName, out var prop)
				&& prop.ValueKind == JsonValueKind.String)
			{
				return prop.GetString() ?? defaultValue;
			}
			return defaultValue;
		}
	}
}
