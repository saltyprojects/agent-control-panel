import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Landing from './pages/Landing'
import Dashboard from './pages/Dashboard'
import Workflows from './pages/Workflows'
import Pricing from './pages/Pricing'
import Integrations from './pages/Integrations'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/workflows.html" element={<Workflows />} />
        <Route path="/pricing.html" element={<Pricing />} />
        <Route path="/integrations.html" element={<Integrations />} />
      </Routes>
    </Router>
  )
}

export default App
