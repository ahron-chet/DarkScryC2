#include "pch.h"


extern "C" __declspec(dllexport)
char* DpapiUnprotectBase64(const char* base64Encrypted, DWORD cryptProtection)
{
    std::vector<BYTE> decoded = Base64Decode(base64Encrypted);

    if (decoded.size() < 5) {
        throw std::runtime_error("Encrypted data is too small to skip 5 bytes.");
    }
    std::vector<BYTE> toUnprotect(decoded.begin() + 5, decoded.end());

    DATA_BLOB inputBlob = { 0 };
    inputBlob.pbData = toUnprotect.data();
    inputBlob.cbData = static_cast<DWORD>(toUnprotect.size());

    DATA_BLOB outputBlob = { 0 };
    if (!CryptUnprotectData(
        &inputBlob,
        NULL,       // description
        NULL,       // optional entropy
        NULL,       // reserved
        NULL,       // prompt
        cryptProtection,
        &outputBlob
    )) {
        throw std::runtime_error("CryptUnprotectData failed.");
    }

    std::vector<BYTE> unprotectedData(outputBlob.pbData, outputBlob.pbData + outputBlob.cbData);

    if (outputBlob.pbData) {
        LocalFree(outputBlob.pbData);
    }
    std::string decrypted = Base64Encode(unprotectedData);
    char* outStr = static_cast<char*>(std::malloc(decrypted.size() + 1)); 
    std::memcpy(outStr, decrypted.c_str(), decrypted.size() + 1);
    *outSize = decrypted.size() + 1;
    return outStr;
}


extern "C" __declspec(dllexport)
void current_free(void* dest) {
    free(dest);
}