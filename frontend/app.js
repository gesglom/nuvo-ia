const agentsList = document.getElementById('agentsList');
const planContainer = document.getElementById('planContainer');
const resultBox = document.getElementById('resultBox');

async function api(path, method = 'GET', body) {
  const res = await fetch(path, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`HTTP ${res.status}: ${txt}`);
  }
  return res.json();
}

document.getElementById('loadAgentsBtn').addEventListener('click', async () => {
  try {
    const data = await api('/api/agents');
    agentsList.innerHTML = '';
    data.agents.forEach((name) => {
      const li = document.createElement('li');
      li.textContent = name;
      agentsList.appendChild(li);
    });
  } catch (err) {
    resultBox.textContent = String(err);
  }
});

document.getElementById('planBtn').addEventListener('click', async () => {
  try {
    const goal = document.getElementById('goal').value.trim();
    const data = await api('/api/plan', 'POST', { goal });
    planContainer.innerHTML = '';
    (data.plan || []).forEach((step, i) => {
      const div = document.createElement('div');
      div.className = 'step';
      div.textContent = `${i + 1}. [${step.agent}] ${step.task}`;
      planContainer.appendChild(div);
    });
    resultBox.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    resultBox.textContent = String(err);
  }
});

document.getElementById('runAgentBtn').addEventListener('click', async () => {
  try {
    const agent = document.getElementById('agentName').value.trim();
    const task = document.getElementById('agentTask').value.trim();
    const data = await api('/api/run-agent', 'POST', { agent, task });
    resultBox.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    resultBox.textContent = String(err);
  }
});


document.getElementById('providersBtn').addEventListener('click', async () => {
  try {
    const data = await api('/api/providers');
    resultBox.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    resultBox.textContent = String(err);
  }
});
