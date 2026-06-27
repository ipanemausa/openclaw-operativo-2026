import React, { useState, useEffect } from 'react'

const BASE = ''

export default function Dashboard() {
  const [stack, setStack] = useState([])
  const [tareas, setTareas] = useState({})
  const [gateway, setGateway] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      const [s, t, g] = await Promise.allSettled([
        fetch('http://localhost:8090/stack').then(r => r.json()),
        fetch('http://localhost:8090/api/tareas').then(r => r.json()),
        fetch('http://localhost:8080/api/mcp/status').then(r => r.json()),
      ])
      if (s.status === 'fulfilled') setStack(s.value.containers || [])
      if (t.status === 'fulfilled') setTareas(t.value.tareas || {})
      if (g.status === 'fulfilled') setGateway(g.value)
      setLoading(false)
    }
    load()
    const interval = setInterval(load, 10000)
    return () => clearInterval(interval)
  }, [])

  if (loading) return <div style={{padding:'2rem',color:'#888'}}>Cargando sistema...</div>

  const estadoColor = s => ({
    completada:  '#4ade80',
    pendiente:   '#fbbf24',
    en_cola:     '#60a5fa',
    ejecutando:  '#fb923c',
  }[s] || '#a09d99')

  return (
    <div style={{padding:'1.5rem', minHeight:'100vh', color:'#e0e0e0', fontFamily:'monospace'}}>

      <h1 style={{color:'#d4af6a', marginBottom:'4px', fontSize:'1.4rem'}}>⬡ LAMAUTONOMIA</h1>
      <p style={{color:'#555', fontSize:'0.8rem', marginBottom:'1.5rem'}}>auto-refresh 10s</p>

      <div style={{display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(280px,1fr))', gap:'1rem'}}>

        {/* CONTENEDORES */}
        <div style={{background:'#111', border:'1px solid rgba(212,175,106,0.15)', borderRadius:'8px', padding:'1rem'}}>
          <h2 style={{color:'#d4af6a', fontSize:'0.85rem', letterSpacing:'2px', marginBottom:'12px'}}>CONTENEDORES</h2>
          {stack.map(c => (
            <div key={c.name} style={{display:'flex', justifyContent:'space-between', padding:'6px 0', borderBottom:'1px solid #1a1a1a', fontSize:'0.82rem'}}>
              <span>
                <span style={{display:'inline-block', width:'8px', height:'8px', borderRadius:'50%', background: c.status==='running' ? '#4ade80' : '#fb7185', marginRight:'6px'}}/>
                {c.name}
              </span>
              <span style={{color: c.status==='running' ? '#4ade80' : '#fb7185'}}>{c.status}</span>
            </div>
          ))}
        </div>

        {/* GATEWAY */}
        <div style={{background:'#111', border:'1px solid rgba(212,175,106,0.15)', borderRadius:'8px', padding:'1rem'}}>
          <h2 style={{color:'#d4af6a', fontSize:'0.85rem', letterSpacing:'2px', marginBottom:'12px'}}>HB JEWELRY — GATEWAY</h2>
          <div style={{display:'flex', justifyContent:'space-between', padding:'6px 0', borderBottom:'1px solid #1a1a1a', fontSize:'0.82rem'}}>
            <span>estado</span>
            <span style={{color: gateway.status==='ok' ? '#4ade80' : '#fb7185'}}>{gateway.status || 'sin respuesta'}</span>
          </div>
          {(gateway.agents||[]).map(a => (
            <div key={a} style={{display:'flex', justifyContent:'space-between', padding:'6px 0', borderBottom:'1px solid #1a1a1a', fontSize:'0.82rem'}}>
              <span style={{color:'#d4af6a'}}>⬡ {a}</span>
              <span style={{color:'#4ade80'}}>activo</span>
            </div>
          ))}
        </div>

        {/* DAG TAREAS */}
        <div style={{background:'#111', border:'1px solid rgba(212,175,106,0.15)', borderRadius:'8px', padding:'1rem'}}>
          <h2 style={{color:'#d4af6a', fontSize:'0.85rem', letterSpacing:'2px', marginBottom:'12px'}}>DAG — TAREAS</h2>
          {Object.entries(tareas).map(([k, v]) => (
            <div key={k} style={{display:'flex', justifyContent:'space-between', padding:'6px 0', borderBottom:'1px solid #1a1a1a', fontSize:'0.82rem'}}>
              <span style={{color:'#f0ede8'}}>{k.replace(/_/g,' ')}</span>
              <span style={{
                fontSize:'0.7rem', padding:'2px 8px', borderRadius:'4px',
                color: estadoColor(v.estado),
                border: `1px solid ${estadoColor(v.estado)}40`,
                background: `${estadoColor(v.estado)}20`
              }}>{v.estado}</span>
            </div>
          ))}
        </div>

      </div>
    </div>
  )
}