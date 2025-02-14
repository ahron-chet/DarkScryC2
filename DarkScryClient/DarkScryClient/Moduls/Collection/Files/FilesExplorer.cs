using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Text.Json;

namespace DarkScryClient.Moduls.Collection.Files
{
	public class FileEntry
	{
		public string Name { get; set; }
		public string Icon { get; set; }
		public long Size { get; set; }
		public string LastWriteTimeUtc { get; set; }
		public string CreationTimeUtc { get; set; }
		public string Path { get; set; }
	}

	public class DirectoryList
	{
		public string[] Items { get; set; }
		public DirectoryList(string path)
		{
			Items = Directory.GetDirectories(path);
		}
	}

	public class ExplorerResult
	{
		public FileEntry[] Files { get; set; }
		public DirectoryList Directories { get; set; }
		public string RootPath { get; set; }

		public ExplorerResult(FileEntry[] files, DirectoryList directories, string path)
		{
			Files = files;
			Directories = directories;
			RootPath = path;
		}
	}

	public static class FilesExplorer
	{
		private static readonly ConcurrentDictionary<string, string> IconsByExtension =
			new ConcurrentDictionary<string, string>(StringComparer.OrdinalIgnoreCase);

		private static string GetIconBase64(string filePath)
		{
			var ext = Path.GetExtension(filePath);
			if (string.IsNullOrEmpty(ext)) ext = ".none";

			if (IconsByExtension.TryGetValue(ext, out var cached))
				return cached;

			try
			{
				using (Icon icon = Icon.ExtractAssociatedIcon(filePath))
				{
					if (icon == null)
					{
						IconsByExtension[ext] = "Default";
						return "Default";
					}

					using (Bitmap bmp = icon.ToBitmap())
					{
						using (var ms = new MemoryStream())
						{
							bmp.Save(ms, System.Drawing.Imaging.ImageFormat.Png);
							var base64 = Convert.ToBase64String(ms.ToArray());
							IconsByExtension[ext] = base64;
							return base64;
						}
					}
				}
			}
			catch
			{
				IconsByExtension[ext] = "Default";
				return "Default";
			}
		}

		public static string GetFilesAndDirectories(string path)
		{
			var dirs = new DirectoryList(path);
			var fileEntries = new List<FileEntry>();

			foreach (var file in Directory.EnumerateFiles(path))
			{
				try
				{
					var info = new FileInfo(file);
					fileEntries.Add(new FileEntry
					{
						Path = file,
						Name = info.Name,
						CreationTimeUtc = info.CreationTimeUtc.ToString("O"),
						LastWriteTimeUtc = info.LastWriteTimeUtc.ToString("O"),
						Size = info.Length,
						Icon = GetIconBase64(file)
					});
				}
				catch
				{
					// Could log the error
				}
			}

			var result = new ExplorerResult(fileEntries.ToArray(), dirs, path);
			return JsonSerializer.Serialize(result);
		}
	}
}
