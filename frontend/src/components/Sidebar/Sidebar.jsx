import React from 'react'
import '../../styles/sidebar.css'

const sections = [
  { id: 'dashboard', label: 'Dashboard', icon: '◈' },
  { id: 'chat', label: 'Chat Agentes', icon: '◎' },
  { id: 'productos', label: 'Productos', icon: '◇' },
  { id: 'ventas', label: 'Ventas', icon: '◆' },
  { id: 'marketing', label: 'Marketing', icon: '◉' },
  { id: 'ordenes', label: 'Ordenes', icon: '▣' },
  { id: 'historial', label: 'Historial', icon: '◷' },
  { id: 'chathistorial', label: 'Chat Historial', icon: '💬' },
  { id: 'workspace', label: 'Workspace', icon: '⬡' },
  { id: 'auditoria', label: 'Auditoria', icon: '🔍' },
  { id: 'clientes', label: 'Clientes', icon: '👥' },
  { id: 'inventario', label: 'Inventario', icon: '📦' },
  { id: 'reportes', label: 'Reportes', icon: '📊' },
  { id: 'analytics', label: 'Analytics', icon: '📈' },
  { id: 'monitor', label: 'Monitor', icon: '🖥' },
  { id: 'pipeline', label: 'Pipeline', icon: '🚀' },
  { id: 'notificaciones', label: 'Notificaciones', icon: '🔔' },
  { id: 'configuracion', label: 'Configuracion', icon: '⚙️' },
]

export default function Sidebar({ activeSection, onSelect, sidebarOpen }) {
  return (
    <aside className={'sidebar' + (sidebarOpen ? ' open' : '')}>
      <nav className='sidebar-nav'>
        {sections.map(s => (
          <button 
            key={s.id} 
            className={'sidebar-item' + (activeSection === s.id ? ' active' : '')}
            onClick={() => onSelect(s.id)}
          >
            <span className='sidebar-icon'>{s.icon}</span>
            <span className='sidebar-label'>{s.label}</span>
          </button>
        ))}
      </nav>

      <div className='sidebar-footer'>OpenClaw 2026</div>
    </aside>
  )
}
