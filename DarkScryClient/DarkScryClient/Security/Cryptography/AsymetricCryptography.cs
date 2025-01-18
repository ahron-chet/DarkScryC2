using System;
using System.Security.Cryptography;


namespace DarkScryClient.Security.Cryptography
{
	internal class AsymetricCryptography : IDisposable
	{
		private readonly RSA _rsa;

		public AsymetricCryptography(string xmlPublicKey)
		{
			if (string.IsNullOrWhiteSpace(xmlPublicKey))
				throw new ArgumentNullException(nameof(xmlPublicKey), "Public key XML is null or empty.");

			_rsa = RSA.Create();

			_rsa.FromXmlString(xmlPublicKey);
		}

		public byte[] Encrypt(byte[] data)
		{
			if (data == null || data.Length == 0)
				throw new ArgumentNullException(nameof(data), "Data to encrypt is null or empty.");

			return _rsa.Encrypt(data, RSAEncryptionPadding.OaepSHA1);
		}

		public bool VerifySignature(byte[] data, byte[] signature)
		{
			if (data == null || data.Length == 0)
				throw new ArgumentNullException(nameof(data), "Data to verify is null or empty.");

			if (signature == null || signature.Length == 0)
				throw new ArgumentNullException(nameof(signature), "Signature is null or empty.");

			// Using SHA256 for hashing
			return _rsa.VerifyData(data, signature, HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1);
		}

		public void Dispose()
		{
			_rsa?.Dispose();
		}
	}
}
