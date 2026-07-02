import React, { useState, useEffect } from 'react'
import '../../styles/hb.css'

const STAT_CARDS = [
  { label: 'Ventas hoy',     value: '$0',   sub: '0 órdenes',    icon: '◆', color: '#d4af6a' },
  { label: 'Productos',      value: '0',    sub: 'en catálogo',  icon: '◇', color: '#60a5fa' },
  { label: 'Clientes',       value: '0',    sub: 'registrados',  icon: '👥', color: '#34d399' },
  { label: 'Contenedores',   value: '0',    sub: 'activos',      icon: '🐳', color: '#a78bfa' },
]

export default function Dashboard() {
  const [stats, setStats] = useState(STAT_CARDS)
  const [tasks, setTasks]   = useState([])
  const [ts, setTs] = useState('')

  useEffect(() => {
    setTs(new Date().toLocaleString('es-MX', { dateStyle: 'medium', timeStyle: 'short' }))

    // Contenedores activos
    fetch('/api/status').then(r => r.json()).then(d => {
      const running = (d.containers || []).filter(c => c.status === 'running').length
      setStats(prev => prev.map(s => s.label === 'Contenedores' ? { ...s, value: running, sub: `${running} running` } : s))
    }).catch(() => {})

    // Tareas pendientes
    fetch('/api/tareas').then(r => r.json()).then(d => {
      setTasks((d.tareas || []).slice(0, 5))
    }).catch(() => {})

    // Ventas del día
    fetch('/api/ventas').then(r => r.json()).then(d => {
      const ventas = d.ventas || []
      const total = ventas.reduce((a, v) => a + (v.total || 0), 0)
      setStats(prev => prev.map(s => s.label === 'Ventas hoy' ? { ...s, value: `$${total.toLocaleString()}`, sub: `${ventas.length} órdenes` } : s))
    }).catch(() => {})

    // Productos
    fetch('/api/productos').then(r => r.json()).then(d => {
      const n = (d.productos || []).length
      setStats(prev => prev.map(s => s.label === 'Productos' ? { ...s, value: n, sub: `${n} en catálogo` } : s))
    }).catch(() => {})
  }, [])

  return (
    <div className="hb-page">

      {/* Header */}
      <div className="hb-page-header">
        <div>
          <h1 className="hb-page-title">Dashboard</h1>
          <p className="hb-page-subtitle">Actualizado: {ts}</p>
        </div>
        <button className="hb-btn hb-btn-sm" onClick={() => window.location.reload()}>↻ Refrescar</button>
      </div>

      {/* Stats cards */}
      <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(180px,1fr))', gap:'12px', marginBottom:'24px' }}>
        {stats.map((s, i) => (
          <div key={i} className="hb-card" style={{ borderTop: `2px solid ${s.color}` }}>
            <div style={{ display:'flex', justifyContent:'space-between', alignItems:'flex-start' }}>
              <div>
                <div style={{ fontSize:'11px', color:'#a09d99', textTransform:'uppercase', letterSpacing:'.06em', marginBottom:'6px' }}>{s.label}</div>
                <div style={{ fontSize:'22px', fontWeight:'700', color:'#f0ede8' }}>{s.value}</div>
                <div style={{ fontSize:'11px', color:'#6b6866', marginTop:'4px' }}>{s.sub}</div>
              </div>
              <span style={{ fontSize:'20px', opacity:0.7 }}>{s.icon}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Tareas + Acciones rápidas */}
      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:'16px' }}>

        {/* Tareas recientes */}
        <div className="hb-table-wrap">
          <div style={{ padding:'12px 14px', fontSize:'13px', fontWeight:'600', color:'#f0ede8', borderBottom:'1px solid rgba(255,255,255,0.07)' }}>
            🔄 Tareas activas
          </div>
          {tasks.length === 0 ? (
            <div style={{ padding:'20px', color:'#6b6866', fontSize:'13px', textAlign:'center' }}>
              Sin tareas pendientes
            </div>
          ) : (
            <table className="hb-table">
              <tbody>
                {tasks.map((t, i) => (
                  <tr key={i}>
                    <td className="td-main">{t.nombre || t.id}</td>
                    <td>
                      <span className={t.estado === 'completado' ? 'hb-badge hb-badge-green' : 'hb-badge hb-badge-gray'}>
                        {t.estado || 'pendiente'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* Acciones rápidas */}
        <div className="hb-card">
          <div style={{ fontSize:'13px', fontWeight:'600', color:'#f0ede8', marginBottom:'14px' }}>⚡ Acciones rápidas</div>
          <div style={{ display:'flex', flexDirection:'column', gap:'8px' }}>
            {[
              { label:'➕ Agregar producto',  id:'productos' },
              { label:'📦 Ver pedidos',       id:'ordenes'   },
              { label:'💬 Abrir chat',        id:'chat'      },
              { label:'📊 Ver reportes',      id:'reportes'  },
              { label:'🔍 Auditoría',         id:'auditoria' },
            ].map(a => (
              <button key={a.id} className="hb-btn hb-btn-sm" style={{ textAlign:'left' }}>
                {a.label}
              </button>
            ))}
          </div>
        </div>

      </div>
    </div>
  )
}




