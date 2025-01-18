using DarkScryClient.Client;
using DarkScryClient.Security.Cryptography;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DarkScryClient.tests
{
	internal class test_crypt
	{
		public static void test_rsa()
		{
			byte[] dataToSend = Encoding.UTF8.GetBytes("{\"agent_id\":\"97b4420c-7ed4-4c33-9ed3-dfb7c767b1b4\"}");

			byte[] encryptedData;
			using (AsymetricCryptography rsa = new AsymetricCryptography(Info.PublicKey))
			{

				encryptedData = rsa.Encrypt(dataToSend);
				byte[] sigend = Convert.FromBase64String("YSga2ykSgATA9JgcMAEcyAE7ARYpG0vx7XydBlKVkVlWkNTmiqEPbGk98Sjk4h0WDoBZ7RId/UIOq6tq1sy+bb8nWdPpk61yqI756utQ0wM08yCDEYAeFhsBImPqZlPiiMHSCykD16pLL113M1M3BWZhRmMj0rdXPQXZeBoA60UPE6GWmUZUPv55dBX1P+zB+Lov0dV7ZFPWIkd4OcROC6+6wFC5reQrHhdc9Pz4YCqhESqkLCYMFDdv4KUnhNhbU9I6jNoanABDgOTaZwTiYugm/sDRKosABVm46PYErX5FfJSR13e92vWqYhG+c3dDhKQCcEU+/Xvz0RNelHCTdA==");

				byte[] data = Encoding.UTF8.GetBytes("test");
				bool isValid = rsa.VerifySignature(data, sigend);
				Console.WriteLine("Signature valid? " + isValid);
			}

			// Now 'encryptedData' can be sent to the Python server
			Console.WriteLine("Encrypted data (base64): " + Convert.ToBase64String(encryptedData));
		}
	}
}
