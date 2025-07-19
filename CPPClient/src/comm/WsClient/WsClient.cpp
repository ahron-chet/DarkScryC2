#include "WsClient.h"
#include <websocketpp/common/thread.hpp>
#include <chrono>

using websocketpp::lib::placeholders::_1;
using websocketpp::lib::placeholders::_2;
using websocketpp::lib::bind;

namespace CppAgent {

WsClient::WsClient(const std::string& uri)
    : uri_(uri) {
    ws_client_.init_asio();

    ws_client_.clear_access_channels(websocketpp::log::alevel::frame_payload);
    ws_client_.clear_access_channels(websocketpp::log::alevel::frame_header);
    ws_client_.clear_access_channels(websocketpp::log::alevel::control);
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
        DARKSCRY_LOG(std::string("Connection init failed: ") + ec.message(), Logger::Level::Error);
        return false;
    }
    hdl_ = con->get_handle();
    ws_client_.connect(con);
    thread_ = std::thread(&WsClient::run, this);
    std::unique_lock<std::mutex> lock(open_mtx_);
    if(!open_cv_.wait_for(lock, std::chrono::seconds(5), [this]{ return open_.load(); })) {
        DARKSCRY_LOG("Connection timeout", Logger::Level::Error);
        return false;
    }
    running_ = true;
    return true;
}

void WsClient::run() {
    ws_client_.run();
}

void WsClient::stop() {
    if(running_) {
        running_ = false;
        websocketpp::lib::error_code ec;
        client::connection_ptr con = ws_client_.get_con_from_hdl(hdl_, ec);
        if(!ec && con->get_state() == websocketpp::session::state::open) {
            ws_client_.close(hdl_, websocketpp::close::status::going_away, "stop", ec);
        }
        if(ec) {
            DARKSCRY_LOG(std::string("Close error: ") + ec.message(), Logger::Level::Error);
        }
        if(thread_.joinable()) {
            thread_.join();
        }
    }
}

bool WsClient::send(const std::string& msg) {
    if(!open_) {
        DARKSCRY_LOG("Send failed: connection not open", Logger::Level::Error);
        return false;
    }
    websocketpp::lib::error_code ec;
    ws_client_.send(hdl_, msg, websocketpp::frame::opcode::text, ec);
    if(ec) {
        DARKSCRY_LOG(std::string("Send failed: ") + ec.message(), Logger::Level::Error);
        return false;
    }
    return true;
}

void WsClient::on_open(websocketpp::connection_hdl hdl) {
    {
        std::lock_guard<std::mutex> lock(open_mtx_);
        open_ = true;
    }
    open_cv_.notify_all();
    DARKSCRY_LOG("WebSocket connection opened", Logger::Level::Info);
}

void WsClient::on_message(websocketpp::connection_hdl, client::message_ptr msg) {
    std::string payload = msg->get_payload();
    std::string response = cmd_handler_.handle(payload);
    if(!response.empty()) {
        send(response);
    }
}


void WsClient::wait_close() {
    if (thread_.joinable()) {
        thread_.join();
    }
}

}
