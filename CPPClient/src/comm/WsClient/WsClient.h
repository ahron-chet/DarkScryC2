#pragma once

#include <websocketpp/config/asio_no_tls_client.hpp>
#include <websocketpp/client.hpp>


#include <thread>
#include <atomic>
#include <string>

#include "Logger/GlobalLogger.h"
#include "CommandHandler/CommandHandler.h"

namespace CppAgent {
    class WsClient {
    public:
        explicit WsClient(const std::string& uri);
        ~WsClient();

        bool start();
        void stop();
        bool send(const std::string& msg);
        const std::string& get_uri() const { return uri_; }

    private:
        using client = websocketpp::client<websocketpp::config::asio_client>;
        client ws_client_;
        websocketpp::connection_hdl hdl_;
        std::thread thread_;
        std::atomic_bool running_{false};
        std::atomic_bool open_{false};
        std::mutex open_mtx_;
        std::condition_variable open_cv_;
        std::string uri_;

        void on_open(websocketpp::connection_hdl hdl);
        void on_message(websocketpp::connection_hdl hdl, client::message_ptr msg);
        void run();
        CommandHandler cmd_handler_;
    };
}
