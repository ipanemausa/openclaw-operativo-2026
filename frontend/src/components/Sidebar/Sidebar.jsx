import React from 'react'
import '../../styles/sidebar.css'

const sectionGroups = [
  {
    title: 'Principal',
    items: [
      { id: 'dashboard', label: 'Dashboard', icon: '◈' },
      { id: 'chat', label: 'Chat Agentes', icon: '◎' },
      { id: 'workspace', label: 'Workspace', icon: '⬡' },
      { id: 'monitor', label: 'Monitor', icon: '🖥' },
    ]
  },
  {
    title: 'Operaciones',
    items: [
      { id: 'ventas', label: 'Ventas', icon: '◆' },
      { id: 'productos', label: 'Productos', icon: '◇' },
      { id: 'inventario', label: 'Inventario', icon: '📦' },
      { id: 'clientes', label: 'Clientes', icon: '👥' },
      { id: 'ordenes', label: 'Ordenes', icon: '▣' },
    ]
  },
  {
    title: 'Marketing & Analytics',
    items: [
      { id: 'marketing', label: 'Marketing', icon: '◉' },
      { id: 'analytics', label: 'Analytics', icon: '📈' },
      { id: 'reportes', label: 'Reportes', icon: '📊' },
      { id: 'pipeline', label: 'Pipeline', icon: '🚀' },
    ]
  },
  {
    title: 'Sistema',
    items: [
      { id: 'voicecall', label: 'Voz Bilingüe', icon: '🎙' },
      { id: 'integraciones', label: 'WhatsApp', icon: '📲' },
      { id: 'historial', label: 'Historial', icon: '◷' },
      { id: 'chathistorial', label: 'Chat Historial', icon: '💬' },
      { id: 'auditoria', label: 'Auditoria', icon: '🔍' },
      { id: 'notificaciones', label: 'Notificaciones', icon: '🔔' },
      { id: 'configuracion', label: 'Configuracion', icon: '⚙️' },
    ]
  }
]

export default function Sidebar({ activeSection, onSelect }) {
  return (
    <aside className="sidebar">
      <nav className="sidebar-nav">
        {sectionGroups.map((group, idx) => (
          <div key={idx} className="sidebar-section">
            {idx > 0 && <hr className="sidebar-divider" />}
            <h3 className="sidebar-section-title">{group.title}</h3>
            <ul className="sidebar-menu">
              {group.items.map(item => (
                <li key={item.id}>
                  <button
                    className={'sidebar-item' + (activeSection === item.id ? ' active' : '')}
                    onClick={() => onSelect(item.id)}
                  >
                    <span className="sidebar-icon">{item.icon}</span>
                    <span className="sidebar-label">{item.label}</span>
                  </button>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </nav>
      <div className="sidebar-footer">OpenClaw 2026</div>
    </aside>
  )
}
