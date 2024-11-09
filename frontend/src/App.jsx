import React from 'react'
import { ThemeProvider } from './components/ThemeContext'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import AuthPage from './pages/AuthPage'
import ProtectedRoute from './pages/ProtectedRoute'
import TobiChat from './pages/TobiChat'
import AccountPage from './pages/AccountPage'
import PasswordPage from './pages/PasswordPage'

function App() {
  return (
    <ThemeProvider>
      <Router>
        <div className='app'>
          <main>
            <Routes>
              <Route path='/login' element={<AuthPage/>}/>
              <Route path='/Tobichat' element={<TobiChat />}/>
              <Route path='/' element={<TobiChat />}/>
              <Route path='/account' element={<AccountPage />}/>
              <Route path='/passwd' element={<PasswordPage />}/>

            </Routes>
          </main>
        </div>
      </Router>
    </ThemeProvider>
  )
}

export default App
