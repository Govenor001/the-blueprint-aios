(() => {
  const el = (selector) => document.querySelector(selector);
  const counts = el("#counts");
  const map = el("#department-map");
  const panels = el("#panels");
  const connections = el("#connections");
  const activity = el("#activity-list");
  const activitySummary = el("#activity-summary");
  const brainCount = el("#brain-count");
  const systemStatus = el("#system-status");
  const drawer = el("#drawer");
  const drawerContent = el("#drawer-content");
  const tints = ["#bff4d6", "#cceafb", "#e5dcff", "#fff1b8", "#ffd7c8", "#d9f0e8", "#dce7ff"];

  const escape = (value) => String(value ?? "").replace(/[&<>'"]/g, (character) => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;","\"":"&quot;"}[character]));
  const list = (values) => Array.isArray(values) ? values.map(escape).join(", ") : escape(values);

  async function api(path, options = {}) {
    const response = await fetch(path, options);
    if (!response.ok) throw new Error(await response.text());
    return response.json();
  }

  function allAgents(data) {
    return data.wings.flatMap((wing) => wing.departments.flatMap((department) => department.functions.flatMap((fn) => fn.agents)));
  }

  function renderCounts(data) {
    const labels = {total:"agents mapped", manual:"manual", assisted:"assisted", autonomous:"autonomous"};
    counts.innerHTML = Object.keys(labels).map((key) => `<div class="metric"><b>${escape(data.counts[key] ?? 0)}</b><span>${labels[key]}</span></div>`).join("");
    brainCount.textContent = data.counts.total ?? "—";
  }

  function renderDepartments(data) {
    const departments = data.wings.flatMap((wing) => wing.departments.map((department) => ({...department, wing:wing.wing})));
    map.innerHTML = departments.map((department, index) => {
      const agents = department.functions.flatMap((fn) => fn.agents);
      const chips = agents.slice(0, 3).map((agent) => `<span class="agent-chip">${escape(agent.name)}</span>`).join("");
      const remainder = agents.length > 3 ? `<span class="agent-chip">+${agents.length - 3} more</span>` : "";
      return `<button class="department" type="button" data-department="${index}" style="--tint:${tints[index % tints.length]}"><span class="dept-top"><span class="dept-name">${escape(department.department)}</span><span class="dept-count">${agents.length}</span></span><span class="dept-agents">${chips}${remainder}</span><span class="dept-note">${escape(department.wing)} · ${department.functions.length} function${department.functions.length === 1 ? "" : "s"}</span></button>`;
    }).join("");
    map.querySelectorAll("[data-department]").forEach((button) => button.addEventListener("click", () => openDepartment(departments[Number(button.dataset.department)])));
  }

  function openDepartment(department) {
    const agents = department.functions.flatMap((fn) => fn.agents);
    drawerContent.innerHTML = `<p class="eyebrow">${escape(department.wing)}</p><h2>${escape(department.department)}</h2><p class="description">${agents.length} agent${agents.length === 1 ? "" : "s"} assigned to this part of the operating system.</p><div class="details">${department.functions.map((fn) => `<div class="detail"><b>${escape(fn.function)}</b><p>${fn.agents.map((agent) => `<button class="agent-link" data-agent="${escape(agent.name)}" type="button">${escape(agent.name)}</button>`).join(" ")}</p></div>`).join("")}</div>`;
    drawerContent.querySelectorAll("[data-agent]").forEach((button) => button.addEventListener("click", () => openAgent(agents.find((agent) => agent.name === button.dataset.agent))));
    drawer.classList.add("open");
  }

  function openAgent(agent) {
    if (!agent) return;
    drawerContent.innerHTML = `<p class="eyebrow">${escape(agent.autonomy)} agent</p><h2>${escape(agent.name)}</h2><p class="description">${escape(agent.description)}</p><div class="details"><div class="detail"><b>Job it replaces</b><p>${escape(agent.replaces)}</p></div><div class="detail"><b>Your role</b><p>${escape(agent["the-human"])}</p></div><div class="detail"><b>Trigger</b><p>${escape(agent.trigger)}</p></div><div class="detail"><b>Outputs</b><p>${list(agent.outputs)}</p></div><div class="detail"><b>Measures</b><p>${list(agent.kpis)}</p></div><div class="detail"><b>Tools</b><p>${list(agent.tools)}</p></div></div><button id="run-agent" class="run" type="button">Run ${escape(agent.name)}</button><p id="drawer-message" class="drawer-message"></p>`;
    el("#run-agent").addEventListener("click", async (event) => {
      event.currentTarget.disabled = true;
      el("#drawer-message").textContent = "Starting this run…";
      try {
        const result = await api("/api/run", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({skill:agent.name})});
        el("#drawer-message").textContent = `Run accepted: ${result.run_id.slice(0, 8)}.`;
      } catch {
        el("#drawer-message").textContent = "This run could not start. Check the system connection and setup status.";
      } finally {
        event.currentTarget.disabled = false;
      }
    });
    drawer.classList.add("open");
  }

  function renderPanels(payload) {
    const cards = payload.panels.flatMap((panel) => panel.cards.map((card) => ({...card, panel:panel.name}))).slice(0, 6);
    panels.innerHTML = cards.length ? cards.map((card) => {
      const latest = card.latest;
      const value = latest?.status === "available" ? (latest.value ?? "Available") : "Not connected";
      const source = latest?.source || latest?.error || `Set up ${card.panel}`;
      return `<article class="panel-card"><small>${escape(card.title)}</small><strong>${escape(value)}</strong><span>${escape(source)}</span></article>`;
    }).join("") : `<article class="panel-card"><small>First panel</small><strong>Not connected</strong><span>Connect your tools during setup.</span></article>`;
  }

  function renderConnections(payload) {
    connections.innerHTML = payload.connections.map((connection) => `<div class="health-row"><span>${escape(connection.name)}</span><span class="badge ${escape(connection.status)}">${connection.status === "connected" ? "Connected" : `${connection.configured}/${connection.required} configured`}</span></div>`).join("");
  }

  function renderActivity(payload) {
    const items = payload.items || [];
    activitySummary.textContent = items.length ? `${items.length} recent event${items.length === 1 ? "" : "s"}, recorded locally.` : "No activity yet. The first approved run will appear here.";
    activity.innerHTML = items.length ? items.slice(0, 8).map((item) => `<div class="activity-row"><div><b>${escape(item.event)}</b>${item.skill ? ` · ${escape(item.skill)}` : ""}</div><time>${escape((item.ts || "").replace("T", " ").replace("Z", ""))}</time></div>`).join("") : `<div class="activity-row"><div><b>Waiting for the first run</b> · Activity remains on this machine and is redacted before display.</div></div>`;
  }

  function renderHealth(payload) {
    const ready = payload.bridge && payload.claude;
    systemStatus.innerHTML = `<span class="dot"></span><span>${ready ? "System ready" : "Setup in progress"}</span>`;
    systemStatus.classList.toggle("needs-setup", !ready);
  }

  async function load() {
    try {
      const [mapData, panelData, connectionData, activityData, healthData] = await Promise.all([api("/api/map"), api("/api/panels"), api("/api/connections"), api("/api/activity?limit=50"), api("/api/health")]);
      renderCounts(mapData); renderDepartments(mapData); renderPanels(panelData); renderConnections(connectionData); renderActivity(activityData); renderHealth(healthData);
    } catch {
      systemStatus.innerHTML = `<span class="dot"></span><span>Needs setup</span>`;
      activitySummary.textContent = "Mission Control could not read its local data. Check dashboard access and setup.";
    }
  }

  el("#drawer-close").addEventListener("click", () => drawer.classList.remove("open"));
  document.addEventListener("keydown", (event) => { if (event.key === "Escape") drawer.classList.remove("open"); });
  load();
  setInterval(load, 10000);
})();
