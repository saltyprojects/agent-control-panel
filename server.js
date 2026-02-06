const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static('public'));

// Mock data for demo - will connect to real OpenClaw API later
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
    lastActivity: 'Building React component...'
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
    lastActivity: 'Processing dataset...'
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
    lastActivity: 'Waiting for tasks...'
  }
];

// API endpoints
app.get('/api/agents', (req, res) => {
  res.json({ agents: mockAgents });
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
    status: 'starting',
    model: model || 'claude-sonnet-4',
    uptime: '0m',
    tokensUsed: 0,
    cost: 0,
    permissions: permissions || ['read'],
    lastActivity: 'Initializing...'
  };
  mockAgents.push(newAgent);
  res.json({ success: true, agent: newAgent });
});

app.get('/api/stats', (req, res) => {
  const totalCost = mockAgents.reduce((sum, a) => sum + a.cost, 0);
  const totalTokens = mockAgents.reduce((sum, a) => sum + a.tokensUsed, 0);
  const runningCount = mockAgents.filter(a => a.status === 'running').length;
  
  res.json({
    totalAgents: mockAgents.length,
    runningAgents: runningCount,
    totalCost: totalCost.toFixed(2),
    totalTokens: totalTokens
  });
});

app.listen(PORT, () => {
  console.log(`Agent Control Panel running on port ${PORT}`);
});
