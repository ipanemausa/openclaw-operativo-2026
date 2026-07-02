import React, { useState } from 'react'
import Header from '../Header/Header'
import Sidebar from '../Sidebar/Sidebar'
import './layout.css'

export default function Layout({ children }) {
  const [activeSection, setActiveSection] = useState('dashboard')

  return (
    <div className="layout">
      <Header />

      <Sidebar
        activeSection={activeSection}
        onSelect={setActiveSection}
      />

      <main className="layout-content">
        {children}
      </main>
    </div>
  )
}
