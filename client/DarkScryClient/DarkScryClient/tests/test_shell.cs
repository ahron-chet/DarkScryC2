using DarkScryClient.NativeMethods;
using DarkScryClient.Utils;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DarkScryClient.tests
{
	internal class test_shell
	{
		void test_current_user()
		{

			Logger logger = new Logger();

			var shellPtr = ShellService.CreateShellInstanceBySid("CURRENT_USER");
			if (shellPtr == IntPtr.Zero)
			{
				logger.Log("Failed to create shell instance.", Logger.LogLevel.Error);
				return;
			}

			// Keep the delegate in a variable so GC won't collect it
			ShellService.ShellOutputCallback callback = (output) =>
			{
				Console.Write(output);
			};

			// Start the shell reading
			ShellService.StartShell(shellPtr, callback);

			logger.Log("Type commands. Type 'exit' to quit.");
			while (true)
			{
				string cmd = Console.ReadLine();
				if (cmd == null || cmd.Equals("exit", StringComparison.OrdinalIgnoreCase))
					break;

				ShellService.SendShellCommand(shellPtr, cmd);
			}

			// Stop & cleanup
			ShellService.StopShell(shellPtr);
			ShellService.DestroyShellInstance(shellPtr);

			logger.Log("Shell terminated. Press any key to exit.");
			Console.ReadKey();
		}

		public static void test_system()
		{

			Logger logger = new Logger();

			var shellPtr = ShellService.CreateShellInstanceBySid("S-1-5-18");
			if (shellPtr == IntPtr.Zero)
			{
				logger.Log("Failed to create shell instance.", Logger.LogLevel.Error);
				return;
			}

			// Keep the delegate in a variable so GC won't collect it
			ShellService.ShellOutputCallback callback = (output) =>
			{
				Console.Write(output);
			};

			// Start the shell reading
			ShellService.StartShell(shellPtr, callback);

			logger.Log("Type commands. Type 'exit' to quit.");
			while (true)
			{
				string cmd = Console.ReadLine();
				if (cmd == null || cmd.Equals("exit", StringComparison.OrdinalIgnoreCase))
					break;

				ShellService.SendShellCommand(shellPtr, cmd);
			}

			// Stop & cleanup
			ShellService.StopShell(shellPtr);
			ShellService.DestroyShellInstance(shellPtr);

			logger.Log("Shell terminated. Press any key to exit.");
			Console.ReadKey();
		}
	}
}
