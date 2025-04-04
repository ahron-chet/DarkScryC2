using System;
using System.Runtime.InteropServices;


namespace DarkScryClient.NativeMethods
{
	internal class ShellService
	{
		[UnmanagedFunctionPointer(CallingConvention.StdCall)]
		public delegate void ShellOutputCallback(string text);

		// P/Invoke the exported functions from your DLL
		[DllImport("C:\\Users\\aharon\\Desktop\\DevTests\\DarkScryClient\\DarkScryClient\\x64\\Release\\shell.dll", CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Unicode)]
		public static extern IntPtr CreateShellInstanceBySid(string sidString);

		[DllImport("C:\\Users\\aharon\\Desktop\\DevTests\\DarkScryClient\\DarkScryClient\\x64\\Release\\shell.dll", CallingConvention = CallingConvention.Cdecl)]
		public static extern void DestroyShellInstance(IntPtr shell);

		[DllImport("C:\\Users\\aharon\\Desktop\\DevTests\\DarkScryClient\\DarkScryClient\\x64\\Release\\shell.dll", CallingConvention = CallingConvention.Cdecl)]
		public static extern void StartShell(IntPtr shell, ShellOutputCallback cb);

		[DllImport("C:\\Users\\aharon\\Desktop\\DevTests\\DarkScryClient\\DarkScryClient\\x64\\Release\\shell.dll", CallingConvention = CallingConvention.Cdecl)]
		public static extern void SendShellCommand(IntPtr shell, string command);

		[DllImport("C:\\Users\\aharon\\Desktop\\DevTests\\DarkScryClient\\DarkScryClient\\x64\\Release\\shell.dll", CallingConvention = CallingConvention.Cdecl)]
		public static extern void StopShell(IntPtr shell);
	}
}
