// dllmain.cpp : Defines the entry point for the DLL application.
#include "pch.h"

extern "C" __declspec(dllexport)
void __stdcall GetUserNameByPid(DWORD processID, LPWSTR* buffer)
{
	HANDLE hToken;
	HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION, FALSE, processID);
	if (hProcess)
	{
		if (OpenProcessToken(hProcess, TOKEN_QUERY, &hToken))
		{
			DWORD tokenInfoSize = 0;
			GetTokenInformation(hToken, TokenUser, NULL, 0, &tokenInfoSize);
			PTOKEN_USER pTokenUser = (PTOKEN_USER)LocalAlloc(LPTR, tokenInfoSize);
			if (GetTokenInformation(hToken, TokenUser, pTokenUser, tokenInfoSize, &tokenInfoSize))
			{
				DWORD accountNameSize = 0;
				DWORD domainNameSize = 0;
				SID_NAME_USE sidNameUse;
				LookupAccountSid(NULL, pTokenUser->User.Sid, NULL, &accountNameSize, NULL, &domainNameSize, &sidNameUse);
				LPWSTR accountName = (LPWSTR)LocalAlloc(LPTR, accountNameSize * sizeof(WCHAR));
				LPWSTR domainName = (LPWSTR)LocalAlloc(LPTR, domainNameSize * sizeof(WCHAR));
				if (LookupAccountSid(NULL, pTokenUser->User.Sid, accountName, &accountNameSize, domainName, &domainNameSize, &sidNameUse))
				{
					if (domainNameSize > 0)
					{
						size_t resultSize = domainNameSize + accountNameSize + 2;
						*buffer = (LPWSTR)LocalAlloc(LPTR, resultSize * sizeof(WCHAR));
						swprintf_s(*buffer, resultSize, L"%s\\%s", domainName, accountName);
					}
					else
					{
						*buffer = (LPWSTR)LocalAlloc(LPTR, (accountNameSize + 1) * sizeof(WCHAR));
						wcscpy_s(*buffer, accountNameSize + 1, accountName);
					}
				}
				LocalFree(accountName);
				LocalFree(domainName);
			}
			CloseHandle(hToken);
			LocalFree(pTokenUser);
		}
		CloseHandle(hProcess);
	}
}

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

