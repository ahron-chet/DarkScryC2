#include "NetworkClient.h"
#include "Config.h"

using namespace CppAgent;

NetworkClient::NetworkClient(Logger& logger) : logger_(logger) {
    client_.init_asio();
    client_.set_message_handler([this](websocketpp::connection_hdl, client_t::message_ptr msg) {
        if (on_message_) {
            on_message_(msg->get_payload());
        }
    });
    client_.set_fail_handler([this](websocketpp::connection_hdl){
        logger_.log("WebSocket connection failed", Logger::Level::Error);
    });
    client_.set_open_handler([this](websocketpp::connection_hdl hdl){
        std::lock_guard<std::mutex> lock(connection_mutex_);
        hdl_ = hdl;
        connected_ = true;
        logger_.log("WebSocket connected", Logger::Level::Info);
    });
    client_.set_close_handler([this](websocketpp::connection_hdl){
        std::lock_guard<std::mutex> lock(connection_mutex_);
        connected_ = false;
        logger_.log("WebSocket disconnected", Logger::Level::Info);
    });
}

NetworkClient::~NetworkClient() {
    disconnect();
}

bool NetworkClient::connect(const std::string& uri) {
    websocketpp::lib::error_code ec;
    client_t::connection_ptr con = client_.get_connection(uri, ec);
    if (ec) {
        logger_.log("Connection init failed: " + ec.message(), Logger::Level::Error);
        return false;
    }
    client_.connect(con);
    run_thread_ = std::thread([this](){ client_.run(); });
    return true;
}

void NetworkClient::disconnect() {
    {
        std::lock_guard<std::mutex> lock(connection_mutex_);
        if (!connected_) return;
        client_.close(hdl_, websocketpp::close::status::normal, "closing");
    }
    if (run_thread_.joinable()) run_thread_.join();
    connected_ = false;
}

void NetworkClient::send(const std::string& text) {
    std::lock_guard<std::mutex> lock(connection_mutex_);
    if (!connected_) return;
    websocketpp::lib::error_code ec;
    client_.send(hdl_, text, websocketpp::frame::opcode::text, ec);
    if (ec) {
        logger_.log("Send failed: " + ec.message(), Logger::Level::Error);
    }
}

void NetworkClient::set_message_handler(MessageHandler handler) {
    on_message_ = handler;
}
