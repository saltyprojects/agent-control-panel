import { useState } from 'react'

export default function Landing() {
  const [email, setEmail] = useState('')
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setStatus('loading')
    
    try {
      const response = await fetch('/api/waitlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      })
      
      if (response.ok) {
        setStatus('success')
        setEmail('')
      } else {
        setStatus('error')
      }
    } catch (error) {
      setStatus('error')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Hero Section */}
      <div className="container mx-auto px-6 py-20">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-6xl font-bold text-white mb-6">
            Control Your AI Agents
          </h1>
          <p className="text-xl text-slate-300 mb-8">
            Monitor, manage, and secure your multi-agent systems with enterprise-grade controls
          </p>
          
          {/* Waitlist Form */}
          <form onSubmit={handleSubmit} className="max-w-md mx-auto">
            <div className="flex gap-4">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                required
                className="flex-1 px-6 py-3 rounded-lg bg-slate-800 text-white border border-slate-700 focus:outline-none focus:border-green-500"
              />
              <button
                type="submit"
                disabled={status === 'loading'}
                className="px-8 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition disabled:opacity-50"
              >
                {status === 'loading' ? 'Joining...' : 'Join Waitlist'}
              </button>
            </div>
            {status === 'success' && (
              <p className="mt-4 text-green-400">✓ Successfully joined the waitlist!</p>
            )}
            {status === 'error' && (
              <p className="mt-4 text-red-400">✗ Failed to join. Please try again.</p>
            )}
          </form>
        </div>
      </div>
    </div>
  )
}
