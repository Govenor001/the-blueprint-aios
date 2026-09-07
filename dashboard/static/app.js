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

  function renderMap(data) {
    map.innerHTML = data.wings.map(wing => `
      <article class="wing"><h2>${wing.wing}</h2>
        ${wing.departments.map(department => `
          <div class="department"><strong>${department.department}</strong>
            <div class="agents">${department.agents.map(agent =>
              `<button data-skill="${agent.name}" title="${agent.description}">${agent.name}</button>`
            ).join("")}</div>
          </div>`).join("")}
      </article>`).join("");
    map.querySelectorAll("[data-skill]").forEach(button => button.addEventListener("click", async () => {
      button.disabled = true; status.textContent = `Starting ${button.dataset.skill}…`;
      try { await api("/api/run", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({skill:button.dataset.skill})}); status.textContent = "Skill accepted."; }
      catch (error) { status.textContent = "Could not start that skill."; }
      finally { button.disabled = false; }
    }));
  }

  async function load() {
    try {
      const [data, events] = await Promise.all([api("/api/map"), api("/api/activity?limit=20")]);
      renderCounts(data); renderMap(data);
      activity.textContent = events.items.length ? events.items.map(item => `${item.ts}  ${item.event}  ${item.skill || ""}`).join("\n") : "No activity yet.";
      status.textContent = "Connected";
    } catch (error) { status.textContent = "Connect the dashboard to continue."; }
  }
  load();
})();
