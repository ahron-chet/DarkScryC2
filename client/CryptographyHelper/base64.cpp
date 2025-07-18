#include "pch.h"


std::vector<BYTE> Base64Decode(const std::string& base64String) {
    DWORD decodedSize = 0;
    if (!CryptStringToBinaryA(base64String.c_str(), 0, CRYPT_STRING_BASE64, NULL, &decodedSize, NULL, NULL)) {
        throw std::runtime_error("CryptStringToBinaryA (get size) failed.");
    }
    std::vector<BYTE> decodedData(decodedSize);
    if (!CryptStringToBinaryA(base64String.c_str(), 0, CRYPT_STRING_BASE64, decodedData.data(), &decodedSize, NULL, NULL)) {
        throw std::runtime_error("CryptStringToBinaryA (decode) failed.");
    }
    decodedData.resize(decodedSize);
    return decodedData;
}

std::string Base64Encode(const std::vector<BYTE>& data) {
    DWORD encodedSize = 0;
    if (!CryptBinaryToStringA(data.data(), static_cast<DWORD>(data.size()), CRYPT_STRING_BASE64 | CRYPT_STRING_NOCRLF, NULL, &encodedSize)) {
        throw std::runtime_error("CryptBinaryToStringA (get size) failed.");
    }
    std::string encoded(encodedSize, '\0');
    if (!CryptBinaryToStringA(data.data(), static_cast<DWORD>(data.size()), CRYPT_STRING_BASE64 | CRYPT_STRING_NOCRLF, &encoded[0], &encodedSize)) {
        throw std::runtime_error("CryptBinaryToStringA (encode) failed.");
    }
    while (!encoded.empty() && (encoded.back() == '\0' || encoded.back() == '\n' || encoded.back() == '\r')) {
        encoded.pop_back();
    }
    return encoded;
}