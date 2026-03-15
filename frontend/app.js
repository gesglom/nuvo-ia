const $ = (id) => document.getElementById(id);
const resultBox = $('resultBox');

async function api(path, method = 'GET', body) {
  const res = await fetch(path, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  return res.json();
}

function renderJobs(jobs) {
  const rows = jobs.map((j) => `
    <tr>
      <td>${j.job_id}</td>
      <td>${j.status}</td>
      <td>${(j.tasks || []).length}</td>
      <td>
        <button onclick="runJob('${j.job_id}')">Run</button>
        <button onclick="retryJob('${j.job_id}')">Retry</button>
      </td>
    </tr>
  `).join('');

  $('jobsTable').innerHTML = `
    <table class="table">
      <thead><tr><th>Job ID</th><th>Status</th><th>Tasks</th><th>Actions</th></tr></thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}

async function refreshDashboard() {
  const [jobsData, metrics, agentsData] = await Promise.all([
    api('/api/jobs'),
    api('/api/metrics'),
    api('/api/agents'),
  ]);

  const jobs = jobsData.jobs || [];
  $('kpiJobs').textContent = String(jobs.length);
  $('kpiAgents').textContent = String((agentsData.agents || []).length);
  $('kpiSuccess').textContent = `${metrics.success || 0}/${metrics.total_events || 0}`;
  $('kpiLatency').textContent = `${metrics.avg_latency_ms || 0} ms`;

  renderJobs(jobs);
}

async function createJob() {
  const goal = $('goal').value.trim();
  if (!goal) return;
  const data = await api('/api/jobs', 'POST', { goal });
  resultBox.textContent = JSON.stringify(data, null, 2);
  await refreshDashboard();
}

window.runJob = async (jobId) => {
  const data = await api(`/api/jobs/${jobId}/run`, 'POST', {});
  resultBox.textContent = JSON.stringify(data, null, 2);
  await refreshDashboard();
};

window.retryJob = async (jobId) => {
  const data = await api(`/api/jobs/${jobId}/retry`, 'POST', {});
  resultBox.textContent = JSON.stringify(data, null, 2);
  await refreshDashboard();
};

$('createJobBtn').addEventListener('click', () => createJob().catch((e) => resultBox.textContent = String(e)));
$('refreshBtn').addEventListener('click', () => refreshDashboard().catch((e) => resultBox.textContent = String(e)));
$('providersBtn').addEventListener('click', async () => resultBox.textContent = JSON.stringify(await api('/api/providers'), null, 2));
$('metricsBtn').addEventListener('click', async () => resultBox.textContent = JSON.stringify(await api('/api/metrics'), null, 2));
$('smokeBtn').addEventListener('click', async () => resultBox.textContent = JSON.stringify(await api('/api/agents/smoke', 'POST', { goal: 'smoke test factory' }), null, 2));
$('selfImproveBtn').addEventListener('click', async () => resultBox.textContent = JSON.stringify(await api('/api/self-improvement'), null, 2));

refreshDashboard().catch((e) => resultBox.textContent = String(e));
