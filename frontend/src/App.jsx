import React, { useState } from 'react'
import Layout from './components/Layout/Layout'
import Chat from './components/Chat/Chat'
import Productos from './components/Productos/Productos'
import Ventas from './components/Ventas/Ventas'
import Dashboard from './components/Dashboard/Dashboard'
import Marketing from './components/Marketing/Marketing'
import Ordenes from './components/Ordenes/Ordenes'
import Historial from './components/Historial/Historial'
import Chathistorial from './components/Chathistorial/Chathistorial'
import Workspace from './components/Workspace/Workspace'
import Auditoria from './components/Auditoria/Auditoria'
import VoiceCall from './components/VoiceCall/VoiceCall'
import Integraciones from './components/Integraciones/Integraciones'

export default function App() {
  const [activeSection, setActiveSection] = useState('dashboard')

  return (
    <Layout activeSection={activeSection} onSelect={setActiveSection}>
      {activeSection === 'dashboard' && <Dashboard />}
      {activeSection === 'chat' && <Chat />}
      {activeSection === 'productos' && <Productos />}
      {activeSection === 'ventas' && <Ventas />}
      {activeSection === 'marketing' && <Marketing />}
      {activeSection === 'ordenes' && <Ordenes />}
      {activeSection === 'historial' && <Historial />}
      {activeSection === 'chathistorial' && <Chathistorial />}
      {activeSection === 'workspace' && <Workspace />}
      {activeSection === 'auditoria' && <Auditoria />}
      {activeSection === 'voicecall' && <VoiceCall />}
      {activeSection === 'integraciones' && <Integraciones />}
    </Layout>
  )
}
