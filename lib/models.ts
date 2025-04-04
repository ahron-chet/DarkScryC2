export const module_descriptior = {
    "remote_thread_shellcode": {
        "desc":"Remote Thread Shellcode Injection is a technique that injects and executes shellcode in a remote process by creating a new thread, often using VirtualAllocEx, WriteProcessMemory, and CreateRemoteThread.",
        "warn": `This module requires valid shellcode. If you want to run a PE file, use the "PE to Shellcode" module first.`
    } 
}