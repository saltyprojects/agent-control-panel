const express = require('express');
const path = require('path');
const fs = require('fs');
const app = express();
const PORT = process.env.PORT || 3000;

// Get Railway build info from environment
const COMMIT_SHA = process.env.RAILWAY_GIT_COMMIT_SHA || 'unknown';
const COMMIT_SHORT = COMMIT_SHA.substring(0, 7);
const COMMIT_MESSAGE = process.env.RAILWAY_GIT_COMMIT_MESSAGE || '';
const BUILD_TIME_ISO = new Date().toISOString(); // Deployment time as ISO string

app.use(express.json());

// Middleware to inject build info into HTML pages
app.use((req, res, next) => {
  const originalSend = res.sendFile;
  res.sendFile = function(filepath, options) {
    const ext = path.extname(filepath);
    if (ext === '.html') {
      fs.readFile(filepath, 'utf8', (err, html) => {
        if (err) return next(err);
        
        // Inject build info
        const buildInfo = `
  <div style="position:fixed;bottom:0;left:0;right:0;background:rgba(15,23,42,0.95);backdrop-filter:blur(12px);border-top:1px solid rgba(255,255,255,0.1);padding:12px 24px;font-size:12px;color:#94a3b8;z-index:9999;display:flex;justify-content:space-between;align-items:center;">
    <span>Build: <a href="https://github.com/saltyprojects/agent-control-panel/commit/${COMMIT_SHA}" target="_blank" style="color:#10b981;text-decoration:none;font-weight:600;">${COMMIT_SHORT}</a> • <span id="build-time" data-time="${BUILD_TIME_ISO}"></span></span>
    <span>${COMMIT_MESSAGE.substring(0, 60)}${COMMIT_MESSAGE.length > 60 ? '...' : ''}</span>
  </div>
  <script>
    // Convert deployment time to browser's local timezone
    const timeEl = document.getElementById('build-time');
    if (timeEl) {
      const buildTimeISO = timeEl.getAttribute('data-time');
      const deployTime = new Date(buildTimeISO);
      timeEl.textContent = deployTime.toLocaleString();
    }
  </script>`;
        
        html = html.replace('</body>', `${buildInfo}\n</body>`);
        res.send(html);
      });
    } else {
      originalSend.call(res, filepath, options);
    }
  };
  next();
});

// Waitlist storage (simple file-based for MVP)
const WAITLIST_FILE = './waitlist.json';
let waitlist = [];
try {
  if (fs.existsSync(WAITLIST_FILE)) {
    waitlist = JSON.parse(fs.readFileSync(WAITLIST_FILE, 'utf8'));
  }
} catch (e) {
  waitlist = [];
}

// Serve landing page as homepage
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'landing.html'));
});

// Serve dashboard at /dashboard
app.get('/dashboard', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Static files
app.use(express.static('public'));

// Waitlist signup
app.post('/api/waitlist', (req, res) => {
  const { email } = req.body;
  if (!email || !email.includes('@')) {
    return res.status(400).json({ error: 'Invalid email' });
  }
  
  if (!waitlist.includes(email)) {
    waitlist.push(email);
    fs.writeFileSync(WAITLIST_FILE, JSON.stringify(waitlist, null, 2));
    console.log(`New signup: ${email} (total: ${waitlist.length})`);
  }
  
  res.json({ success: true, count: waitlist.length });
});

app.get('/api/waitlist/count', (req, res) => {
  res.json({ count: waitlist.length });
});

// Mock data with security features
const mockAgents = [
  {
    id: 'agent-1',
    name: 'Code Generator',
    status: 'running',
    model: 'claude-sonnet-4',
    uptime: '2h 34m',
    tokensUsed: 45231,
    cost: 2.34,
    permissions: ['read', 'write', 'exec'],
    lastActivity: 'Building React component...',
    securityScore: 'A',
    filesAccessed: 234,
    toolCalls: 892,
    alerts: 0
  },
  {
    id: 'agent-2',
    name: 'Data Analyzer',
    status: 'running',
    model: 'claude-opus-4.6',
    uptime: '45m',
    tokensUsed: 89012,
    cost: 8.90,
    permissions: ['read', 'web_search'],
    lastActivity: 'Analyzing dataset patterns...',
    securityScore: 'C',
    filesAccessed: 567,
    toolCalls: 1203,
    alerts: 2
  },
  {
    id: 'agent-3',
    name: 'QA Tester',
    status: 'idle',
    model: 'gpt-5.3-codex',
    uptime: '1h 12m',
    tokensUsed: 12400,
    cost: 0.62,
    permissions: ['read', 'exec'],
    lastActivity: 'Waiting for tasks...',
    securityScore: 'A+',
    filesAccessed: 46,
    toolCalls: 312,
    alerts: 0
  }
];

const auditLog = [
  { time: '00:42:31', agent: 'Data Analyzer', action: 'FILE_READ', target: '/etc/passwd', status: 'BLOCKED' },
  { time: '00:41:15', agent: 'Data Analyzer', action: 'FILE_READ', target: '~/.ssh/config', status: 'FLAGGED' },
  { time: '00:40:22', agent: 'Code Generator', action: 'EXEC', target: 'npm install', status: 'ALLOWED' },
  { time: '00:39:08', agent: 'Code Generator', action: 'FILE_WRITE', target: './src/component.tsx', status: 'ALLOWED' },
  { time: '00:38:45', agent: 'QA Tester', action: 'WEB_FETCH', target: 'api.github.com', status: 'ALLOWED' }
];

// API endpoints
app.get('/api/agents', (req, res) => {
  res.json({ agents: mockAgents });
});

app.get('/api/stats', (req, res) => {
  const totalCost = mockAgents.reduce((sum, a) => sum + a.cost, 0);
  const totalTokens = mockAgents.reduce((sum, a) => sum + a.tokensUsed, 0);
  const runningCount = mockAgents.filter(a => a.status === 'running').length;
  const totalAlerts = mockAgents.reduce((sum, a) => sum + a.alerts, 0);
  const totalFilesAccessed = mockAgents.reduce((sum, a) => sum + a.filesAccessed, 0);
  const totalToolCalls = mockAgents.reduce((sum, a) => sum + a.toolCalls, 0);
  
  res.json({
    totalAgents: mockAgents.length,
    runningAgents: runningCount,
    totalCost: totalCost.toFixed(2),
    totalTokens: totalTokens,
    securityAlerts: totalAlerts,
    filesAccessed: totalFilesAccessed,
    toolCalls: totalToolCalls
  });
});

app.get('/api/audit', (req, res) => {
  res.json({ log: auditLog });
});

app.post('/api/agents/:id/kill', (req, res) => {
  const agent = mockAgents.find(a => a.id === req.params.id);
  if (agent) {
    agent.status = 'stopped';
    res.json({ success: true, message: `Agent ${agent.name} stopped` });
  } else {
    res.status(404).json({ error: 'Agent not found' });
  }
});

app.post('/api/agents/spawn', (req, res) => {
  const { name, model, permissions } = req.body;
  const newAgent = {
    id: `agent-${Date.now()}`,
    name: name || 'New Agent',
    status: 'running',
    model: model || 'claude-sonnet-4',
    uptime: '0m',
    tokensUsed: 0,
    cost: 0,
    permissions: permissions || ['read'],
    lastActivity: 'Initializing...',
    securityScore: 'A',
    filesAccessed: 0,
    toolCalls: 0,
    alerts: 0
  };
  mockAgents.push(newAgent);
  res.json({ success: true, agent: newAgent });
});

app.listen(PORT, () => {
  console.log(`Agent Control Panel running on port ${PORT}`);
  console.log(`Landing page: /`);
  console.log(`Dashboard: /dashboard`);
  console.log(`Waitlist signups: ${waitlist.length}`);
});
