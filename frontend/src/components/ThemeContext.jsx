import React, { createContext, useState, useContext, useEffect } from 'react'

// Para saber que tema tiene la aplicación
const ThemeContext = createContext()

export const ThemeProvider = ({ children }) => {
  // Estado que maneja el tema, inicializado a claro
  const [theme, setTheme] = useState('light')

  // Cambia el tema de claro a oscuro
  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light')
  }

  // Si se cambia a modo oscuro, en el css se usa el classname dark-theme, sino se pone el root
  useEffect(() => {
    document.body.className = theme === 'dark' ? 'dark-theme' : ''
  }, [theme])

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export const useTheme = () => useContext(ThemeContext)