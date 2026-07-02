import React from 'react'
import '../../styles/layout.css'

export default function Header() {
  return (
    <header className="app-header">
      <div className="header-brand">HB <span>Jewelry</span></div>
      <div className="header-status">
        <span className="status-dot"></span>
        <span className="status-text">Sistema operativo</span>
      </div>
    </header>
  )
}
