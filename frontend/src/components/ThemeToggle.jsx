import React from 'react'
import { useTheme } from './ThemeContext'
import { Sun, Moon } from 'lucide-react'

function ThemeToggle() {
  // Obtenemos la funcion para saber el tema actual y cambiar el mismo
  const { theme, toggleTheme } = useTheme()

  /*
    Renderizado:Tenemos una label que se divide de dos partes, la primera una 
    checkbox que al cambiar de estado usa el toggleTheme para hacer el cambio 
    y la segunda es un contenedor para que cuando se cambie muestre un sol o 
    una luna con los iconos de la libreria lucide-react
  */
  return (
    <label className="theme-switch">
      <input
        type="checkbox"
        checked={theme === 'dark'}
        onChange={toggleTheme}
        aria-label="Toggle dark mode"
      />
      <span className="slider round">
        <span className="moon"><Moon size={20} /></span>
        <span className="sun"><Sun size={20} /> </span>
      </span>
    </label>
  )
}

export default ThemeToggle