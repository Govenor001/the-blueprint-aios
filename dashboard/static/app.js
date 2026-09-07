(() => {
  const status = document.querySelector("#status");
  const counts = document.querySelector("#counts");
  const map = document.querySelector("#map");
  const activity = document.querySelector("#activity");

  async function api(path, options = {}) {
    const response = await fetch(path, options);
    if (!response.ok) throw new Error(await response.text());
    return response.json();
  }

  function renderCounts(data) {
    counts.innerHTML = ["total", "manual", "assisted", "autonomous"].map(key =>
      `<div class="card"><span class="subtle">${key}</span><strong>${data.counts[key] ?? 0}</strong></div>`
    ).join("");
  }

  function agents(data) {
    return data.wings.flatMap(wing => wing.departments.flatMap(department =>
      department.functions.flatMap(func => func.agents)
    ));
  }

  function renderPanel(agent) {
    if (!agent) return;
    let panel = document.querySelector("#panel");
    if (!panel) {
      panel = document.createElement("section");
      panel.id = "panel";
      panel.className = "card";
      panel.style.marginTop = "16px";
      map.after(panel);
    }
    panel.innerHTML = `
      <h2>${agent.name}</h2>
      <p class="subtle">${agent.description}</p>
      <p><strong>Replaces:</strong> ${agent.replaces}</p>
      <p><strong>Human:</strong> ${agent["the-human"]}</p>
      <p><strong>Trigger:</strong> ${agent.trigger}</p>
      <p><strong>Current mode:</strong> ${agent.autonomy}</p>
      <p><strong>Outputs:</strong> ${agent.outputs.join(", ")}</p>
      <p><strong>KPIs:</strong> ${agent.kpis.join(", ")}</p>
      <button data-run="${agent.name}">Run ${agent.name}</button>`;
    panel.querySelector("[data-run]").addEventListener("click", async event => {
      event.currentTarget.disabled = true;
      try {
        await api("/api/run", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({skill: agent.name})});
        status.textContent = "Skill accepted.";
      } catch {
        status.textContent = "Could not start that skill.";
      } finally {
        event.currentTarget.disabled = false;
      }
    });
  }

  function renderMap(data) {
    map.innerHTML = data.wings.map(wing => `
      <article class="wing"><h2>${wing.wing}</h2>
        ${wing.departments.map(department => `
          <div class="department"><strong>${department.department}</strong>
            ${department.functions.map(func => `
              <div><span class="subtle">${func.function}</span><div class="agents">${func.agents.map(agent =>
                `<button data-skill="${agent.name}"><span aria-hidden="true">${agent.autonomy === "manual" ? "○" : agent.autonomy === "assisted" ? "◐" : "●"}</span> ${agent.name}</button>`
              ).join("")}</div></div>`).join("")}
          </div>`).join("")}
      </article>`).join("");
    map.querySelectorAll("[data-skill]").forEach(button => button.addEventListener("click", () => {
      renderPanel(agents(data).find(agent => agent.name === button.dataset.skill));
    }));
  }

  async function load() {
    try {
      const [data, events] = await Promise.all([api("/api/map"), api("/api/activity?limit=50")]);
      renderCounts(data);
      renderMap(data);
      activity.textContent = events.items.length ? events.items.map(item => `${item.ts}  ${item.event}  ${item.skill || ""}`).join("\n") : "No activity yet.";
      status.textContent = "Connected";
    } catch {
      status.textContent = "Map not built yet — run: python3 scripts/build_map.py";
    }
  }
  load();
  setInterval(load, 10000);
})();
