import React from 'react'
import { useTheme } from './ThemeContext'
import { Sun, Moon } from 'lucide-react'

function ThemeToggle() {
  const { theme, toggleTheme } = useTheme()

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