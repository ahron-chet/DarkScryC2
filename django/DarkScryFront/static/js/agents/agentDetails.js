
// Reuses chatHistory, socketMap, clientTabsMap, domRefs from agentList.js

async function activateClient(agent) {
  const agentId = agent.AgentId;
  console.log("Activating client:", agentId);

  if (clientTabsMap[agentId]) {
    openTab(agentId);
    return;
  }

  const card = domRefs.clientsContainer.querySelector(`[data-client-name="${agentId}"]`);
  if (card) {
    card.style.border = "3px solid #006fa1";
  }

  const newTab = document.createElement("div");
  newTab.classList.add("tab");
  newTab.dataset.tab = agentId;
  newTab.textContent = agent.HostName;

  const closeBtn = document.createElement("span");
  closeBtn.textContent = "×";
  closeBtn.classList.add("tab-close");
  closeBtn.addEventListener("click", (event) => {
    event.stopPropagation();
    closeTab(agentId);
  });
  newTab.appendChild(closeBtn);

  newTab.addEventListener("click", () => openTab(agentId));
  domRefs.tabsContainer.appendChild(newTab);

  const detailDiv = document.createElement("div");
  detailDiv.classList.add("active-client-tab");
  detailDiv.dataset.client = agentId;
  domRefs.tabContent.appendChild(detailDiv);

  clientTabsMap[agentId] = {
    tabEl: newTab,
    panelEl: detailDiv
  };

  createClientDetails(agent);
  try {
    const info = await fetchMachineInfo(agentId);
    console.log("Fetched machine info for " + agentId, info);
    renderMachineInfo(agentId, info);
  } catch (err) {
    console.error("Failed to fetch machine info:", err);
  }
  openTab(agentId);
}

function createClientDetails(agent) {
  const agentId = agent.AgentId;
  const detailDiv = clientTabsMap[agentId].panelEl;
  while (detailDiv.firstChild) {
    detailDiv.removeChild(detailDiv.firstChild);
  }

  const navBar = document.createElement("div");
  navBar.classList.add("navbar");

  const h3 = document.createElement("h3");
  h3.classList.add("optionHeader");
  h3.dataset.optionHeader = agentId;
  h3.textContent = agentId + " Details";
  navBar.appendChild(h3);

  const modulesDiv = document.createElement("div");
  modulesDiv.classList.add("dropdown", "modules");

  const machineInfoBtn = document.createElement("button");
  machineInfoBtn.classList.add("machineInfoButton", "active");
  machineInfoBtn.textContent = "Machine Info";
  machineInfoBtn.addEventListener("click", async () => {
    setActiveModule(agentId, machineInfoBtn);
    try {
      const info = await fetchMachineInfo(agent.AgentId);
      console.log("Refetched machine info for " + agentId, info);
      renderMachineInfo(agentId, info);
    } catch (err) {
      console.error("Failed to fetch machine info:", err);
    }
  });
  modulesDiv.appendChild(machineInfoBtn);

  const remoteShellBtn = document.createElement("button");
  remoteShellBtn.classList.add("remoteShellButton");
  remoteShellBtn.textContent = "Remote Shell";
  remoteShellBtn.addEventListener("click", () => {
    setActiveModule(agentId, remoteShellBtn);
    showRemoteShell(agentId);
  });
  modulesDiv.appendChild(remoteShellBtn);

  const browserPassBtn = document.createElement("button");
  browserPassBtn.classList.add("browserPassButton");
  browserPassBtn.textContent = "Browser Passwowrds";
  modulesDiv.appendChild(browserPassBtn);

  const injectionsBtn = document.createElement("button");
  injectionsBtn.classList.add("injectionsButton");
  injectionsBtn.textContent = "Injections";
  modulesDiv.appendChild(injectionsBtn);

  const processesBtn = document.createElement("button");
  processesBtn.classList.add("processesButton");
  processesBtn.textContent = "Processes";
  modulesDiv.appendChild(processesBtn);

  navBar.appendChild(modulesDiv);
  detailDiv.appendChild(navBar);

  const rowDiv = document.createElement("div");
  rowDiv.classList.add("row");
  rowDiv.dataset.clientModulesRow = agentId;
  detailDiv.appendChild(rowDiv);
}

function setActiveModule(agentId, buttonEl) {
  const detailDiv = clientTabsMap[agentId].panelEl;
  const allButtons = detailDiv.querySelectorAll(".dropdown.modules button");
  allButtons.forEach(btn => btn.classList.remove("active"));
  buttonEl.classList.add("active");
}

async function fetchMachineInfo(agentId) {
  const url = `/api/v2/agents/${agentId}/modules/collection/machine/basic_mashine_info`;
  const resp = await runFetchUntilComplete(url);
  const data = resp.result?.data?.result;
  if (data.length === 0) {
    throw new Error("Invalid or empty response data received");
  }
  return data;
}

function renderMachineInfo(agentId, info) {
  const detail = Array.isArray(info) ? info[0] : info;
  const detailDiv = clientTabsMap[agentId].panelEl;
  const rowDiv = detailDiv.querySelector(`[data-client-modules-row="${agentId}"]`);
  while (rowDiv.firstChild) {
    rowDiv.removeChild(rowDiv.firstChild);
  }

  const fields = [
    ["HostName", detail.HostName],
    ["OperatingSystem", detail.OperatingSystem],
    ["OSVersionDetail", detail.OSVersionDetail],
    ["CPU", detail.CPU],
    ["RAM", detail.RAM],
    ["Disk", detail.Disk],
    ["PrimaryIP", detail.PrimaryIP],
    ["GPU", detail.GPU],
    ["AgentStatus", detail.AgentStatus],
    ["LastLogin", detail.LastLogin],
    [
      "LogedInSessions",
      Array.isArray(detail.LogedInSessions) ? detail.LogedInSessions.join(", ") : ""
    ]
  ];

  const fragment = document.createDocumentFragment();
  fields.forEach(([label, value]) => {
    const p = document.createElement("p");
    p.textContent = label + ": " + (value || "");
    fragment.appendChild(p);
  });
  rowDiv.appendChild(fragment);
}

function showRemoteShell(agentId) {
  const detailDiv = clientTabsMap[agentId].panelEl;
  const rowDiv = detailDiv.querySelector(`[data-client-modules-row="${agentId}"]`);
  while (rowDiv.firstChild) {
    rowDiv.removeChild(rowDiv.firstChild);
  }

  const chatPanel = document.createElement("div");
  chatPanel.classList.add("chat-slide-panel");
  chatPanel.dataset.chatPanel = agentId;

  const headerDiv = document.createElement("div");
  headerDiv.classList.add("chat-slide-header");
  const strongEl = document.createElement("strong");
  strongEl.textContent = agentId + " - Remote Shell";
  headerDiv.appendChild(strongEl);
  chatPanel.appendChild(headerDiv);

  const bodyDiv = document.createElement("div");
  bodyDiv.classList.add("chat-slide-body");
  bodyDiv.dataset.chatBody = agentId;
  chatPanel.appendChild(bodyDiv);

  const footerDiv = document.createElement("div");
  footerDiv.classList.add("chat-slide-footer");
  const inputEl = document.createElement("input");
  inputEl.type = "text";
  inputEl.classList.add("chat-input");
  inputEl.placeholder = "Type a command...";
  inputEl.dataset.chatInput = agentId;
  footerDiv.appendChild(inputEl);

  const sendBtn = document.createElement("button");
  sendBtn.classList.add("chat-send-btn");
  sendBtn.textContent = "Send";
  sendBtn.addEventListener("click", () => sendCommand(agentId));
  footerDiv.appendChild(sendBtn);

  chatPanel.appendChild(footerDiv);
  rowDiv.appendChild(chatPanel);

  inputEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      sendBtn.click();
    }
  });

  if (!chatHistory[agentId]) {
    chatHistory[agentId] = [];
  }
  getOrCreateSocket(agentId);
  renderChatHistory(agentId);
}

function renderChatHistory(agentId) {
  const bodyDiv = document.querySelector(`[data-chat-body="${agentId}"]`);
  if (!bodyDiv) return;
  while (bodyDiv.firstChild) {
    bodyDiv.removeChild(bodyDiv.firstChild);
  }
  const history = chatHistory[agentId] || [];
  history.forEach(msg => {
    const row = document.createElement("div");
    row.classList.add("message-row", msg.role === "user" ? "right" : "left");
    const bubble = document.createElement("div");
    bubble.classList.add("message-bubble");
    bubble.textContent = msg.text;
    row.appendChild(bubble);
    bodyDiv.appendChild(row);
  });
  bodyDiv.scrollTop = bodyDiv.scrollHeight;
}

function sendCommand(agentId) {
  const inputEl = document.querySelector(`[data-chat-input="${agentId}"]`);
  if (!inputEl) return;
  const userCmd = inputEl.value.trim();
  if (!userCmd) return;

  if (!chatHistory[agentId]) {
    chatHistory[agentId] = [];
  }
  chatHistory[agentId].push({ role: "user", text: userCmd });
  renderChatHistory(agentId);

  const socket = getOrCreateSocket(agentId);
  socket.send(JSON.stringify({ command: userCmd }));

  inputEl.value = "";
}

function showAllClients() {
  Object.values(clientTabsMap).forEach(({ tabEl }) => tabEl.classList.remove("active"));
  Object.values(clientTabsMap).forEach(({ panelEl }) => panelEl.classList.remove("active"));
  domRefs.allClientsTab.classList.add("active");
  domRefs.clientsContainer.querySelectorAll(".client-card").forEach((card) => {
    card.style.display = "flex";
    card.style.border = "";
  });
}

function openTab(agentId) {
  console.log("openTab for agent:", agentId);
  domRefs.clientsContainer.querySelectorAll(".client-card").forEach((c) => {
    c.style.display = "none";
  });
  domRefs.tabsContainer.querySelectorAll(".tab").forEach((tab) => {
    tab.classList.remove("active");
  });
  domRefs.tabContent.querySelectorAll(".active-client-tab").forEach((p) => {
    p.classList.remove("active");
  });
  const tabInfo = clientTabsMap[agentId];
  if (tabInfo) {
    tabInfo.tabEl.classList.add("active");
    tabInfo.panelEl.classList.add("active");
  }
}

function closeTab(agentId) {
  const tabInfo = clientTabsMap[agentId];
  if (!tabInfo) return;
  domRefs.tabsContainer.removeChild(tabInfo.tabEl);
  domRefs.tabContent.removeChild(tabInfo.panelEl);
  delete clientTabsMap[agentId];
  const card = domRefs.clientsContainer.querySelector(`[data-client-name="${agentId}"]`);
  if (card) {
    card.style.border = "";
  }
  showAllClients();
}

async function runFetchUntilComplete(url, { method = "GET", headers = {}, body, intervalMs = 2000, maxAttempts = 30 } = {}) {
  const startResp = await fetch(url, { method, headers, body });
  if (!startResp.ok) throw new Error(`Initial request failed with status ${startResp.status}`);
  const taskId = (await startResp.json())?.task_id;
  if (!taskId) throw new Error("No task_id returned from initial request");

  let attempts = 0;
  return new Promise((resolve, reject) => {
    const checkStatus = async () => {
      attempts++;
      try {
        const statusResp = await fetch(`/api/v2/tasks/${taskId}/status`);
        if (!statusResp.ok) return reject(new Error(`Status request failed with code ${statusResp.status}`));
        const statusData = await statusResp.json();
        if (statusData.status === "complete") {
          const resultResp = await fetch(`/api/v2/tasks/${taskId}/result`);
          if (!resultResp.ok) return reject(new Error(`Result request failed with code ${resultResp.status}`));
          return resolve(await resultResp.json());
        } else if (statusData.status === "failed") return reject(new Error(`Task ${taskId} failed.`));
        if (attempts < maxAttempts) setTimeout(checkStatus, intervalMs);
        else reject(new Error(`Task ${taskId} not complete after ${maxAttempts} attempts.`));
      } catch (err) {
        reject(err);
      }
    };
    checkStatus();
  });
}
