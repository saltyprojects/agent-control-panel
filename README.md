# Agent Control Panel

**The control panel for coordinating multiple AI agents. Track what they're building, manage permissions, monitor costs, and stop runaways instantly.**

🌐 **Live Demo:** https://agent-control-panel-production.up.railway.app/

---

## Features

### 🤝 Multi-Agent Orchestration
- Real-time dashboard for agent teams
- Track coordination between agents
- Monitor agent-to-agent communication
- Team performance analytics

### 💰 Cost Control
- Real-time token usage tracking
- Per-agent budget caps
- Cost projections and alerts
- Prevent runaway spending

### 🛡️ Security & Permissions
- Granular permission controls
- File access monitoring
- API call auditing
- Security scoring per agent

### 📋 Compliance Ready
- Complete audit logs (7 days → 1 year retention)
- SOC2-ready controls
- Exportable logs (CSV, JSON, PDF)
- Immutable, cryptographically signed records

### 🏠 Self-Hosted First
- Deploy on your infrastructure
- Docker + Kubernetes ready
- Air-gapped deployments supported
- Zero vendor lock-in

---

## Why Agent Control Panel?

**Multi-agent systems are here** (Claude Code teams, GPT-5.3-Codex, agent orchestration frameworks). But most teams have:
- ❌ No visibility into what agents are doing
- ❌ No cost control (bills are a mystery until they arrive)
- ❌ No security controls (full system access by default)
- ❌ No compliance audit trails

**Agent Control Panel fixes this.**

---

## Tech Stack

- **Frontend:** Vanilla HTML/CSS/JS (no framework bloat)
- **Backend:** Node.js + Express
- **Deployment:** Railway (or self-hosted)
- **Storage:** File-based (simple MVP, scales to PostgreSQL)

---

## Getting Started

### Quick Demo
Visit the [live demo](https://agent-control-panel-production.up.railway.app/) to explore the dashboard with mock agents.

### Self-Hosted Deployment

**Docker:**
```bash
git clone https://github.com/saltyprojects/agent-control-panel.git
cd agent-control-panel
docker build -t agent-control-panel .
docker run -p 3000:3000 agent-control-panel
```

**Local Development:**
```bash
npm install
npm start
# Visit http://localhost:3000
```

**Environment Variables:**
```bash
PORT=3000  # Server port (optional, defaults to 3000)
```

---

## Integrations

### Currently Supported:
- ✅ **OpenClaw** - Native integration
- ✅ **Claude Code** - Session monitoring (beta)
- ✅ **GitHub** - Repo access auditing

### Coming Soon:
- 🔜 Custom agents (REST API + SDK)
- 🔜 LangChain / LlamaIndex
- 🔜 AutoGPT / BabyAGI

---

## Roadmap

**Q1 2026:**
- [x] MVP dashboard
- [x] Cost tracking
- [x] Basic security monitoring
- [ ] Public launch (waitlist)

**Q2 2026:**
- [ ] SOC2 compliance certification
- [ ] Team collaboration features
- [ ] Advanced workflow automation
- [ ] API + SDK release

---

## Contributing

We're not accepting contributions yet (pre-launch). Follow [@saltyprojects](https://github.com/saltyprojects) for updates.

---

## Pricing

- **Free:** Up to 3 agents forever
- **Pro:** $19/mo per user (unlimited agents)
- **Self-Hosted:** $499 one-time + $99/yr support

See [pricing page](https://agent-control-panel-production.up.railway.app/pricing.html) for details.

---

## Built With 🧂

Agent Control Panel is built by [Salty Projects](https://github.com/saltyprojects) - creating tools for the multi-agent era.

**Questions?** Join our [waitlist](https://agent-control-panel-production.up.railway.app/) or check out the [live demo](https://agent-control-panel-production.up.railway.app/index.html).

---

## License

Copyright © 2026 Salty Projects. All rights reserved.

This is proprietary software. See LICENSE file for details.
