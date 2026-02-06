const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static('public'));

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

// Security audit log
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

app.get('/api/alerts', (req, res) => {
  const alerts = auditLog.filter(l => l.status !== 'ALLOWED');
  res.json({ alerts });
});

app.post('/api/agents/:id/kill', (req, res) => {
  const agent = mockAgents.find(a => a.id === req.params.id);
  if (agent) {
    agent.status = 'stopped';
    auditLog.unshift({
      time: new Date().toTimeString().split(' ')[0],
      agent: agent.name,
      action: 'TERMINATED',
      target: 'Process killed by user',
      status: 'ALLOWED'
    });
    res.json({ success: true, message: `Agent ${agent.name} stopped` });
  } else {
    res.status(404).json({ error: 'Agent not found' });
  }
});

app.post('/api/agents/:id/audit', (req, res) => {
  const agent = mockAgents.find(a => a.id === req.params.id);
  if (agent) {
    const agentLogs = auditLog.filter(l => l.agent === agent.name);
    res.json({ agent: agent.name, logs: agentLogs });
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
  auditLog.unshift({
    time: new Date().toTimeString().split(' ')[0],
    agent: newAgent.name,
    action: 'SPAWNED',
    target: `Model: ${newAgent.model}`,
    status: 'ALLOWED'
  });
  res.json({ success: true, agent: newAgent });
});

app.post('/api/emergency-stop', (req, res) => {
  mockAgents.forEach(a => {
    if (a.status === 'running') {
      a.status = 'stopped';
      auditLog.unshift({
        time: new Date().toTimeString().split(' ')[0],
        agent: a.name,
        action: 'EMERGENCY_STOP',
        target: 'All agents terminated',
        status: 'ALLOWED'
      });
    }
  });
  res.json({ success: true, message: 'All agents terminated' });
});

app.listen(PORT, () => {
  console.log(`Agent Control Panel running on port ${PORT}`);
  console.log(`Security monitoring enabled`);
});
