import React from 'react'
import { ThemeProvider } from './components/ThemeContext'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import AuthPage from './pages/AuthPage'
import ProtectedRoute from './pages/ProtectedRoute'
import Urolobot from './pages/Urolobot'
import AccountPage from './pages/AccountPage'
import PasswordPage from './pages/PasswordPage'

function App() {
  return (
    <ThemeProvider>
      <Router>
        <div className='app'>
          <main>
            <Routes>
                <Route path='/login' element={<AuthPage />} />
                <Route
                  path='/Urolobot'
                  element={
                    <ProtectedRoute>
                      <Urolobot />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path='/'
                  element={
                    <ProtectedRoute>
                      <Urolobot />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path='/account'
                  element={
                    <ProtectedRoute>
                      <AccountPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path='/passwd'
                  element={
                    <ProtectedRoute>
                      <PasswordPage />
                    </ProtectedRoute>
                  }
                />
              </Routes>
          </main>
        </div>
      </Router>
    </ThemeProvider>
  )
}

export default App
