function getOrCreateSocket(agentId) {
  if (socketMap[agentId]) {
    return socketMap[agentId];
  }
  const protocol = (window.location.protocol === "https:") ? "wss:" : "ws:";
  const socketUrl = `${protocol}//${window.location.host}/ws/shell/${agentId}/`;
  const newSocket = new WebSocket(socketUrl);

  newSocket.onopen = () => {
    console.log("WebSocket open for:", agentId);
  };
  newSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (!chatHistory[agentId]) {
      chatHistory[agentId] = [];
    }
    const output = data?.message?.result?.output || "[No output]";
    chatHistory[agentId].push({ role: "bot", text: output });
    if (typeof renderChatHistory === "function") {
      renderChatHistory(agentId);
    }
  };
  newSocket.onerror = (err) => {
    console.error("WebSocket error:", err);
  };
  newSocket.onclose = (evt) => {
    console.log("WebSocket closed for:", agentId, evt.reason);
    delete socketMap[agentId];
  };

  socketMap[agentId] = newSocket;
  return newSocket;
}

function toggleChat(agentId) {
  const chatPanel = document.querySelector(`[data-chat-panel="${agentId}"]`);
  if (!chatPanel) return;

  if (chatPanel.style.display === "none" || chatPanel.style.display === "") {
    chatPanel.style.display = "block";
    chatPanel.classList.remove("animate__flipOutX");
    chatPanel.classList.add("animate__animated", "animate__flipInX");
  } else {
    chatPanel.classList.remove("animate__flipInX");
    chatPanel.classList.add("animate__flipOutX");
    chatPanel.addEventListener("animationend", function handleFlipOut(e) {
      if (e.animationName === "flipOutX") {
        chatPanel.style.display = "none";
      }
      chatPanel.classList.remove("animate__animated", "animate__flipOutX");
      chatPanel.removeEventListener("animationend", handleFlipOut);
    });
  }
}
