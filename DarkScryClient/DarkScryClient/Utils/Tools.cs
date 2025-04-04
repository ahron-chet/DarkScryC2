using System.IO;
using System.Runtime.InteropServices;
using System.Runtime.Serialization.Json;
using System.Text;
using System;



public class Tools
{
	public static byte[] StructToBytes<T>(T data) where T : struct
	{
		var size = Marshal.SizeOf(typeof(T));
		var buffer = new byte[size];
		var ptr = Marshal.AllocHGlobal(size);
		try
		{
			Marshal.StructureToPtr(data, ptr, false);
			Marshal.Copy(ptr, buffer, 0, size);
		}
		finally
		{
			Marshal.FreeHGlobal(ptr);
		}
		return buffer;
	}

	public static T BytesToStruct<T>(byte[] data) where T : struct
	{
		var size = Marshal.SizeOf(typeof(T));
		var ptr = Marshal.AllocHGlobal(size);
		try
		{
			Marshal.Copy(data, 0, ptr, size);
			return (T)Marshal.PtrToStructure(ptr, typeof(T));
		}
		finally
		{
			Marshal.FreeHGlobal(ptr);
		}
	}

	public static byte[] SerializeToJson<T>(T obj)
	{
		using (MemoryStream ms = new MemoryStream())
		{
			DataContractJsonSerializer serializer = new DataContractJsonSerializer(typeof(T));
			serializer.WriteObject(ms, obj);
			return ms.ToArray();
		}
	}

	/// <summary>
	/// Default encoding is Encoding.UTF8
	/// </summary>
	public static byte[] StringToBytes(string input, Encoding encoding = null)
	{
		if (input == null) throw new ArgumentNullException(nameof(input));

		encoding = encoding ?? Encoding.UTF8;

		return encoding.GetBytes(input);
	}

	public static bool ArraysEqual<T>(T[] array1, T[] array2)
	{
		// Check if both arrays are null or reference the same instance
		if (ReferenceEquals(array1, array2))
			return true;

		// If one array is null but the other is not, return false
		if (array1 == null || array2 == null)
			return false;

		// If lengths are not equal, arrays cannot be equal
		if (array1.Length != array2.Length)
			return false;

		// Compare elements one by one
		for (int i = 0; i < array1.Length; i++)
		{
			if (!Equals(array1[i], array2[i]))
				return false;
		}

		return true;
	}

}

