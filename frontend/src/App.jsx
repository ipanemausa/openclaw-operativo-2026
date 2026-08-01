import React, { useState, Component } from 'react'
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

// ─── ERROR BOUNDARY DE PROTECCIÓN TOTAL CONTRA PANTALLA NEGRA ────────────────
class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    console.error("⚠️ Exception interceptada en React App Root:", error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: 40, background: '#0d0d0d', color: '#d4af6a', fontFamily: 'sans-serif', minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <h2 style={{ fontSize: 24, margin: '0 0 10px 0' }}>✨ OpenClaw Enterprise — Modo de Recuperación</h2>
          <p style={{ color: '#a09d99', fontSize: 14 }}>Se ha restaurado la sesión tras un ajuste de interfaz.</p>
          <button
            onClick={() => {
              this.setState({ hasError: false, error: null });
              window.location.reload();
            }}
            style={{ background: '#d4af6a', color: '#000', border: 'none', padding: '10px 24px', borderRadius: 8, fontWeight: 'bold', cursor: 'pointer', marginTop: 15 }}
          >
            RECARGAR DASHBOARD PRINCIPAL ➔
          </button>
        </div>
      )
    }
    return this.props.children
  }
}

export default function App() {
  const [activeSection, setActiveSection] = useState('dashboard')

  const renderSection = () => {
    switch (activeSection) {
      case 'dashboard':      return <Dashboard onNavigate={setActiveSection} />
      case 'chat':           return <Chat />
      case 'productos':      return <Productos />
      case 'ventas':         return <Ventas />
      case 'marketing':      return <Marketing />
      case 'ordenes':        return <Ordenes />
      case 'inventario':     return <Inventario />
      case 'clientes':       return <Clientes />
      case 'analytics':      return <Analytics />
      case 'reportes':       return <Reportes />
      case 'pipeline':       return <Pipeline />
      case 'workspace':      return <Workspace />
      case 'monitor':        return <Monitor />
      case 'terminal':       return <Terminal />
      case 'admin':          return <AdminDashboard />
      case 'historial':      return <Historial />
      case 'chat-historial': return <Chathistorial />
      case 'auditoria':      return <Auditoria />
      case 'avatar':         return <AvatarMeet />
      case 'voicecall':      return <VoiceCall />
      case 'integraciones':  return <Integraciones />
      case 'certificaciones': return <Certificaciones />
      default:               return <Dashboard onNavigate={setActiveSection} />
    }
  }

  return (
    <ErrorBoundary>
      <Layout activeSection={activeSection} onSelect={setActiveSection}>
        {renderSection()}
        <FloatingVoiceWidget />
      </Layout>
    </ErrorBoundary>
  )
}
