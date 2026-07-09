import React, { useState } from 'react'
import Header from '../Header/Header'
import Sidebar from '../Sidebar/Sidebar'
import '../../styles/layout.css'

export default function Layout({ children, activeSection, onSelect }) {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="app-layout">
      <Header onToggleSidebar={() => setSidebarOpen(prev => !prev)} />

      <div className="app-body">
        <Sidebar
          activeSection={activeSection}
          onSelect={(id) => {
            onSelect(id)
            setSidebarOpen(false)
          }}
          sidebarOpen={sidebarOpen}
        />

        <main className="app-content">
          {children}
        </main>
      </div>
    </div>
  )
}
