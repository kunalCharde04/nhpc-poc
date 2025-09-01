import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import HomePage from './pages/HomePage'
import ValidatePage from './pages/ValidatePage'
import HowItWorksPage from './pages/HowItWorksPage'
import './App.css'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/validate" element={<ValidatePage />} />
          <Route path="/how-it-works" element={<HowItWorksPage />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
