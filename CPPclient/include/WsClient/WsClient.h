#pragma once

#include <websocketpp/client.hpp>
#include <websocketpp/config/asio_no_tls_client.hpp>

#include <thread>
#include <atomic>
#include <string>
#include "Logger.h"


namespace CppAgent {
    class WsClient {
    public:
        WsClient(const std::string& uri, Logger& logger);
        ~WsClient();

        bool start();
        void stop();
        void send(const std::string& msg);

    private:
        using client = websocketpp::client<websocketpp::config::asio_client>;
        client ws_client_;
        websocketpp::connection_hdl hdl_;
        std::thread thread_;
        std::atomic_bool running_{false};
        std::string uri_;
        Logger& logger_;

        void on_open(websocketpp::connection_hdl hdl);
        void on_message(websocketpp::connection_hdl hdl, client::message_ptr msg);
        void run();
    };
}
