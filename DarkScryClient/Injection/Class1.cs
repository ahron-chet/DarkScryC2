using System.Runtime.InteropServices;


namespace Injection
{
	public class RemoteThreadInjections
	{
		internal class NativeMethods
		{
			[DllImport("Injections.dll", CallingConvention = CallingConvention.Cdecl, SetLastError = true)]
			public static extern int remote_thread_shellcode_injection(int proc_id, byte[] shellcode, UIntPtr shellcode_size);
		}

		public static bool RemoteThreadShellcode(int proc_id, byte[] shellcode)
		{
			return NativeMethods.remote_thread_shellcode_injection(proc_id, shellcode, (UIntPtr)shellcode.Length) == 0;
		}
	}
}


