import { useEffect, useState } from 'react'

interface Agent {
  id: string
  name: string
  status: 'idle' | 'running' | 'stopped' | 'failed'
  security_score: number
  last_active_at: string | null
}

interface DashboardStats {
  total_agents: number
  active_agents: number
  total_cost: number
  avg_security_score: number
  recent_alerts: number
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [agents, setAgents] = useState<Agent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch dashboard stats
        const statsRes = await fetch('/api/dashboard/stats/')
        if (!statsRes.ok) throw new Error('Failed to fetch stats')
        const statsData = await statsRes.json()
        setStats(statsData)

        // Fetch agents list
        const agentsRes = await fetch('/api/agents/')
        if (!agentsRes.ok) throw new Error('Failed to fetch agents')
        const agentsData = await agentsRes.json()
        setAgents(agentsData.results || agentsData)

        setLoading(false)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
        setLoading(false)
      }
    }

    fetchData()
    // Refresh every 30 seconds
    const interval = setInterval(fetchData, 30000)
    return () => clearInterval(interval)
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'bg-green-500'
      case 'idle': return 'bg-yellow-500'
      case 'stopped': return 'bg-gray-500'
      case 'failed': return 'bg-red-500'
      default: return 'bg-gray-400'
    }
  }

  const getSecurityColor = (score: number) => {
    if (score >= 80) return 'text-green-400'
    if (score >= 60) return 'text-yellow-400'
    return 'text-red-400'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-slate-400">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-900 text-white flex items-center justify-center">
        <div className="bg-red-900/20 border border-red-500 rounded-lg p-8 max-w-md">
          <h2 className="text-2xl font-bold text-red-400 mb-2">Error Loading Dashboard</h2>
          <p className="text-slate-300">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="mt-4 px-4 py-2 bg-red-600 hover:bg-red-700 rounded"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Agent Control Panel</h1>
        <p className="text-slate-400">Monitor and manage your AI agents in real-time</p>
      </div>

      {/* Stats Grid */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <div className="text-slate-400 text-sm mb-1">Total Agents</div>
            <div className="text-3xl font-bold">{stats.total_agents}</div>
          </div>
          
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <div className="text-slate-400 text-sm mb-1">Active Now</div>
            <div className="text-3xl font-bold text-green-400">{stats.active_agents}</div>
          </div>
          
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <div className="text-slate-400 text-sm mb-1">Total Cost</div>
            <div className="text-3xl font-bold">${stats.total_cost.toFixed(2)}</div>
          </div>
          
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <div className="text-slate-400 text-sm mb-1">Avg Security</div>
            <div className={`text-3xl font-bold ${getSecurityColor(stats.avg_security_score)}`}>
              {stats.avg_security_score.toFixed(0)}%
            </div>
          </div>
          
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <div className="text-slate-400 text-sm mb-1">Recent Alerts</div>
            <div className={`text-3xl font-bold ${stats.recent_alerts > 0 ? 'text-red-400' : 'text-slate-500'}`}>
              {stats.recent_alerts}
            </div>
          </div>
        </div>
      )}

      {/* Agents Table */}
      <div className="bg-slate-800 rounded-lg border border-slate-700 overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-700">
          <h2 className="text-xl font-bold">Active Agents</h2>
        </div>
        
        {agents.length === 0 ? (
          <div className="px-6 py-12 text-center text-slate-400">
            <p>No agents registered yet.</p>
            <p className="text-sm mt-2">Connect your first agent to get started.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-700/50">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold">Agent</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold">Status</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold">Security Score</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold">Last Active</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700">
                {agents.map((agent) => (
                  <tr key={agent.id} className="hover:bg-slate-700/30 transition">
                    <td className="px-6 py-4">
                      <div className="font-medium">{agent.name}</div>
                      <div className="text-xs text-slate-400">{agent.id.slice(0, 8)}</div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        <div className={`w-2 h-2 rounded-full ${getStatusColor(agent.status)}`}></div>
                        <span className="capitalize">{agent.status}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`font-semibold ${getSecurityColor(agent.security_score)}`}>
                        {agent.security_score}%
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-400">
                      {agent.last_active_at 
                        ? new Date(agent.last_active_at).toLocaleString()
                        : 'Never'
                      }
                    </td>
                    <td className="px-6 py-4">
                      <button className="text-blue-400 hover:text-blue-300 text-sm font-medium">
                        View Details →
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* API Status Indicator */}
      <div className="mt-8 text-center text-sm text-slate-500">
        <span className="inline-flex items-center gap-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          Connected to API • Auto-refreshing every 30s
        </span>
      </div>
    </div>
  )
}
