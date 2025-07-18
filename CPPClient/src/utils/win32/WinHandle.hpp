#pragma once
#include <Windows.h>
#include <memory>

namespace win32 {

struct HandleCloser {
    void operator()(HANDLE h) const noexcept { if (h) ::CloseHandle(h); }
};

using unique_handle = std::unique_ptr<std::remove_pointer_t<HANDLE>, HandleCloser>;

inline unique_handle make_handle(HANDLE h = nullptr) noexcept { return unique_handle(h); }

} // namespace win32
