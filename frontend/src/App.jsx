import React, { useState } from 'react'
import ErrorBoundary from './components/ErrorBoundary/ErrorBoundary'
import Layout from './components/Layout/Layout'
import Chat from './components/Chat/Chat'
import Productos from './components/Productos/Productos'
import Ventas from './components/Ventas/Ventas'
import Dashboard from './components/Dashboard/Dashboard'
import Marketing from './components/Marketing/Marketing'
import Ordenes from './components/Ordenes/Ordenes'
import Inventario from './components/Inventario/Inventario'
import Clientes from './components/Clientes/Clientes'
import Analytics from './components/Analytics/Analytics'
import Reportes from './components/Reportes/Reportes'
import Pipeline from './components/Pipeline/Pipeline'
import Workspace from './components/Workspace/Workspace'
import Monitor from './components/Monitor/Monitor'
import Terminal from './components/Terminal/Terminal'
import AdminDashboard from './components/AdminDashboard/AdminDashboard'
import Historial from './components/Historial/Historial'
import Chathistorial from './components/Chathistorial/Chathistorial'
import Auditoria from './components/Auditoria/Auditoria'
import AvatarMeet from './components/AvatarMeet/AvatarMeet'
import VoiceCall from './components/VoiceCall/VoiceCall'
import Integraciones from './components/Integraciones/Integraciones'
import Certificaciones from './components/Certificaciones/Certificaciones'
import FloatingVoiceWidget from './components/FloatingVoiceWidget/FloatingVoiceWidget'

export default function App() {
  const [activeSection, setActiveSection] = useState('dashboard')

  return (
    <ErrorBoundary>
      <Layout activeSection={activeSection} onSelect={setActiveSection}>
        {activeSection === 'dashboard' && <ErrorBoundary><Dashboard onNavigate={setActiveSection} /></ErrorBoundary>}
        {activeSection === 'chat' && <ErrorBoundary><Chat /></ErrorBoundary>}
        {activeSection === 'productos' && <ErrorBoundary><Productos /></ErrorBoundary>}
        {activeSection === 'ventas' && <ErrorBoundary><Ventas /></ErrorBoundary>}
        {activeSection === 'marketing' && <ErrorBoundary><Marketing /></ErrorBoundary>}
        {activeSection === 'ordenes' && <ErrorBoundary><Ordenes /></ErrorBoundary>}
        {activeSection === 'inventario' && <ErrorBoundary><Inventario /></ErrorBoundary>}
        {activeSection === 'clientes' && <ErrorBoundary><Clientes /></ErrorBoundary>}
        {activeSection === 'analytics' && <ErrorBoundary><Analytics /></ErrorBoundary>}
        {activeSection === 'reportes' && <ErrorBoundary><Reportes /></ErrorBoundary>}
        {activeSection === 'pipeline' && <ErrorBoundary><Pipeline /></ErrorBoundary>}
        {activeSection === 'workspace' && <ErrorBoundary><Workspace /></ErrorBoundary>}
        {activeSection === 'monitor' && <ErrorBoundary><Monitor /></ErrorBoundary>}
        {activeSection === 'terminal' && <ErrorBoundary><Terminal /></ErrorBoundary>}
        {activeSection === 'admin' && <ErrorBoundary><AdminDashboard /></ErrorBoundary>}
        {activeSection === 'historial' && <ErrorBoundary><Historial /></ErrorBoundary>}
        {activeSection === 'chat-historial' && <ErrorBoundary><Chathistorial /></ErrorBoundary>}
        {activeSection === 'auditoria' && <ErrorBoundary><Auditoria /></ErrorBoundary>}
        {activeSection === 'avatar' && <ErrorBoundary><AvatarMeet /></ErrorBoundary>}
        {activeSection === 'voicecall' && <ErrorBoundary><VoiceCall /></ErrorBoundary>}
        {activeSection === 'integraciones' && <ErrorBoundary><Integraciones /></ErrorBoundary>}
        {activeSection === 'certificaciones' && <ErrorBoundary><Certificaciones /></ErrorBoundary>}
        <ErrorBoundary>
          <FloatingVoiceWidget />
        </ErrorBoundary>
      </Layout>
    </ErrorBoundary>
  )
}
