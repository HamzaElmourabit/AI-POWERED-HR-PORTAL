import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Employees from './pages/Employees'
import Recruitment from './pages/Recruitment'
import Analytics from './pages/Analytics'
import Chatbot from './pages/Chatbot'
import './App.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="employees" element={<Employees />} />
          <Route path="recruitment" element={<Recruitment />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="chatbot" element={<Chatbot />} />
          <Route path="settings" element={<div className="p-8 text-center text-gray-500">Page Paramètres - En développement</div>} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App
