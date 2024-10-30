import React from 'react'
import { ThemeProvider } from './components/ThemeContext'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import AuthPage from './pages/AuthPage'
import ProtectedRoute from './ProtectedRoute'

function App() {
  return (
    <ThemeProvider>
      <Router>
        <div className='app'>
          <main>
            <Routes>
              <Route path='/login' element={<AuthPage/>}/>
              <Route path='/Tobichat' element={<ProtectedRoute />}/>
              <Route path='/' element={<ProtectedRoute />}/>
            </Routes>
          </main>
        </div>
      </Router>
    </ThemeProvider>
  )
}

export default App
