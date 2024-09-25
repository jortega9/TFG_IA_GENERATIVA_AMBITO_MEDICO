import React from 'react'
import { ThemeProvider } from './components/ThemeContext'
import TobiChat from './components/TobiChat'

function App() {
  return (
    <ThemeProvider>
      <TobiChat />
    </ThemeProvider>
  )
}

export default App
