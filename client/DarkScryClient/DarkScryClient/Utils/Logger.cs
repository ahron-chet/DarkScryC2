using System;
using System.IO;
using System.Threading;

namespace DarkScryClient.Utils
{
	internal class Logger : IDisposable
	{
		private readonly string _logFilePath;
		private readonly bool _logToConsole;
		private readonly bool _logToFile;
		private StreamWriter _fileWriter;
		private static readonly SemaphoreSlim _fileLock = new SemaphoreSlim(1, 1);
		private bool _disposed = false;

		public enum LogLevel
		{
			Info,
			Debug,
			Warning,
			Error,
			Critical
		}

		public Logger(bool logToConsole = false, bool logToFile = false, string logFilePath = "log.txt")
		{
			_logToConsole = logToConsole;
			_logToFile = logToFile;
			_logFilePath = logFilePath;

			if (_logToFile)
			{
				_fileWriter = new StreamWriter(_logFilePath, append: true) { AutoFlush = true };
			}
		}

		public void Log(string message, LogLevel level = LogLevel.Info)
		{
			if (!_logToConsole && !_logToFile)
			{
				return;
			}

			string formattedMessage = FormatMessage(message, level);

			if (_logToConsole)
			{
				WriteToConsole(formattedMessage, level);
			}

			if (_logToFile)
			{
				WriteToFile(formattedMessage);
			}
		}

		private string FormatMessage(string message, LogLevel level)
		{
			return $"[{DateTime.Now:yyyy-MM-dd HH:mm:ss}] [{level}] {message}";
		}

		private void WriteToConsole(string message, LogLevel level)
		{
			switch (level)
			{
				case LogLevel.Warning:
					Console.ForegroundColor = ConsoleColor.Yellow;
					break;
				case LogLevel.Error:
				case LogLevel.Critical:
					Console.ForegroundColor = ConsoleColor.Red;
					break;
				default:
					Console.ForegroundColor = ConsoleColor.Gray;
					break;
			}
			Console.WriteLine(message);
			Console.ResetColor();
		}

		private void WriteToFile(string message)
		{
			_fileLock.Wait();
			try
			{
				_fileWriter?.WriteLine(message);
			}
			catch (Exception ex)
			{
				Console.WriteLine($"Failed to write to log file: {ex.Message}");
			}
			finally
			{
				_fileLock.Release();
			}
		}

		public void Dispose()
		{
			if (_disposed) return;

			_fileWriter?.Dispose();
			_fileWriter = null;

			_disposed = true;
		}
	}
}
