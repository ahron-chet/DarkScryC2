#pragma once
#include <websocketpp/config/asio_client.hpp>
#include <websocketpp/client.hpp>
#include <thread>
#include <mutex>
#include <functional>
#include "Logger.h"

namespace CppAgent {
    class NetworkClient {
    public:
        using MessageHandler = std::function<void(const std::string&)>;

        explicit NetworkClient(Logger& logger);
        ~NetworkClient();

        bool connect(const std::string& uri);
        void disconnect();
        void send(const std::string& text);
        void set_message_handler(MessageHandler handler);

    private:
        typedef websocketpp::client<websocketpp::config::asio_client> client_t;
        client_t client_;
        websocketpp::connection_hdl hdl_;
        std::thread run_thread_;
        std::mutex connection_mutex_;
        bool connected_ = false;
        Logger& logger_;
        MessageHandler on_message_;
    };
}
