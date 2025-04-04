using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace Utils
{
	internal class NativeMethods
	{
		[DllImport("CPPUtils.dll", CharSet = CharSet.Unicode, CallingConvention = CallingConvention.Cdecl)]
		public static extern void GetUserNameByPid(uint processID, out IntPtr buffer);
	}
}
