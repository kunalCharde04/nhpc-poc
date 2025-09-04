import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Header from './components/Header'
import HomePage from './pages/HomePage'
import ValidatePage from './pages/ValidatePage'
import HowItWorksPage from './pages/HowItWorksPage'
import './App.css'
import { createContext, useContext, useMemo, useState } from 'react'
import LoginPage from './pages/LoginPage'

type AuthContextType = {
  token: string | null
  login: (token: string) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}

const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('auth_token'))

  const value = useMemo(() => ({
    token,
    login: (t: string) => { localStorage.setItem('auth_token', t); setToken(t) },
    logout: () => { localStorage.removeItem('auth_token'); setToken(null) },
  }), [token])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const { token } = useAuth()
  if (!token) return <Navigate to="/login" replace />
  return children
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="min-h-screen bg-gray-50">
          <Header />
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/validate" element={<ProtectedRoute><ValidatePage /></ProtectedRoute>} />
            <Route path="/how-it-works" element={<HowItWorksPage />} />
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  )
}

export default App
