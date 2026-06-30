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
import Clientes from './components/Clientes/Clientes'
import Inventario from './components/Inventario/Inventario'
import Reportes from './components/Reportes/Reportes'
import Configuracion from './components/Configuracion/Configuracion'
import Notificaciones from './components/Notificaciones/Notificaciones'
import Monitor from './components/Monitor/Monitor'
import Analytics from './components/Analytics/Analytics'
import Pipeline from './components/Pipeline/Pipeline'
import Chatui from './components/Chatui/Chatui'

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
      {activeSection === 'clientes' && <Clientes />}
      {activeSection === 'inventario' && <Inventario />}
      {activeSection === 'reportes' && <Reportes />}
      {activeSection === 'configuracion' && <Configuracion />}
      {activeSection === 'notificaciones' && <Notificaciones />}
      {activeSection === 'monitor' && <Monitor />}
      {activeSection === 'analytics' && <Analytics />}
      {activeSection === 'pipeline' && <Pipeline />}
      {activeSection === 'chatui' && <Chatui />}
    </Layout>
  )
}


