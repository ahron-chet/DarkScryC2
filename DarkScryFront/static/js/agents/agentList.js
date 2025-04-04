

const chatHistory = {};
const socketMap = {};
const clientTabsMap = {};

const domRefs = {
  tabsContainer: document.getElementById("client-tabs-container"),
  tabContent: document.getElementById("client-tab-content"),
  clientsContainer: document.getElementById("clientsContainer"),
  allClientsTab: document.getElementById("allClients")
};

window.addEventListener("DOMContentLoaded", async () => {
  try {
    const agents = await fetchAgents();
    console.log("Fetched agents:", agents);
    renderClientCards(agents);
  } catch (err) {
    console.error("Failed to fetch agents:", err);
  }

  domRefs.allClientsTab.addEventListener("click", showAllClients);
});

async function fetchAgents() {
  const response = await fetch("/api/v2/agents");
  if (!response.ok) {
    throw new Error("Failed to fetch agents: " + response.status);
  }
  return response.json();
}

function renderClientCards(agents) {
  domRefs.clientsContainer.textContent = "";
  agents.forEach(agent => {
    console.log("Rendering card for agent:", agent);
    const card = document.createElement("div");
    card.classList.add("row", "client-card");
    card.dataset.clientName = agent.AgentId;
    const h4 = document.createElement("h4");
    h4.textContent = agent.HostName;
    card.appendChild(h4);

    const iconDiv = document.createElement("div");
    iconDiv.classList.add("client-icon");
    let iconSrc = "{% static 'images/windows.svg' %}";
    const osLower = agent.Os.toLowerCase();
    if (osLower.includes("linux")) {
      iconSrc = "{% static 'images/linux.png' %}";
    } else if (osLower.includes("mac") || osLower.includes("os x")) {
      iconSrc = "{% static 'images/apple.png' %}";
    }
    const osImg = document.createElement("img");
    osImg.src = iconSrc;
    osImg.alt = "OS Icon";
    iconDiv.appendChild(osImg);
    card.appendChild(iconDiv);

    const infoDiv = document.createElement("div");
    infoDiv.classList.add("col", "client-info");
    const osSpan = document.createElement("span");
    osSpan.textContent = "OS: " + agent.Os;
    infoDiv.appendChild(osSpan);
    card.appendChild(infoDiv);

    const activateBtn = document.createElement("button");
    activateBtn.classList.add("col-1", "activate-btn");
    activateBtn.textContent = "Activate";
    activateBtn.addEventListener("click", () => {
      activateClient(agent);
    });
    card.appendChild(activateBtn);

    domRefs.clientsContainer.appendChild(card);
  });
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
