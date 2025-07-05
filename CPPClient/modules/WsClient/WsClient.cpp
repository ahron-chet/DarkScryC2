#include "WsClient.h"
#include <websocketpp/common/thread.hpp>

using websocketpp::lib::placeholders::_1;
using websocketpp::lib::placeholders::_2;
using websocketpp::lib::bind;

namespace CppAgent {

WsClient::WsClient(const std::string& uri)
    : uri_(uri) {
    ws_client_.init_asio();
    ws_client_.set_open_handler(bind(&WsClient::on_open, this, _1));
    ws_client_.set_message_handler(bind(&WsClient::on_message, this, _1, _2));
}

WsClient::~WsClient() {
    stop();
}

bool WsClient::start() {
    websocketpp::lib::error_code ec;
    client::connection_ptr con = ws_client_.get_connection(uri_, ec);
    if (ec) {
        getLogger().log(std::string("Connection init failed: ") + ec.message(), Logger::Level::Error);
        return false;
    }
    hdl_ = con->get_handle();
    ws_client_.connect(con);
    running_ = true;
    thread_ = std::thread(&WsClient::run, this);
    return true;
}

void WsClient::run() {
    ws_client_.run();
}

void WsClient::stop() {
    if(running_) {
        running_ = false;
        websocketpp::lib::error_code ec;
        ws_client_.close(hdl_, websocketpp::close::status::going_away, "stop", ec);
        if(ec) {
            getLogger().log(std::string("Close error: ") + ec.message(), Logger::Level::Error);
        }
        if(thread_.joinable()) {
            thread_.join();
        }
    }
}

void WsClient::send(const std::string& msg) {
    websocketpp::lib::error_code ec;
    ws_client_.send(hdl_, msg, websocketpp::frame::opcode::text, ec);
    if(ec) {
        getLogger().log(std::string("Send failed: ") + ec.message(), Logger::Level::Error);
    }
}

void WsClient::on_open(websocketpp::connection_hdl hdl) {
    getLogger().log("WebSocket connection opened", Logger::Level::Info);
}

void WsClient::on_message(websocketpp::connection_hdl, client::message_ptr msg) {
    getLogger().log(std::string("Received: ") + msg->get_payload(), Logger::Level::Debug);
}

}
