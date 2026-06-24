import React, { useState, useEffect } from 'react'

const GATEWAY = 'http://localhost:8080'
const ORCHESTRATOR = 'http://localhost:8090'

export default function Dashboard() {
  const [stack, setStack] = useState([])
  const [tareas, setTareas] = useState({})
  const [gateway, setGateway] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const [s, t, g, a] = await Promise.all([
          fetch(`${ORCHESTRATOR}/stack`).then(r => r.json()),
          fetch(`${ORCHESTRATOR}/api/tareas`).then(r => r.json()),
          fetch(`${GATEWAY}/health`).then(r => r.json()),
          fetch(`${GATEWAY}/api/mcp/status`).then(r => r.json()),
        ])
        setStack(s.containers || [])
        setTareas(t.tareas || {})
        setGateway({ ...g, agents: a.agents || [] })
      } catch (e) {
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    load()
    const interval = setInterval(load, 10000)
    return () => clearInterval(interval)
  }, [])

  if (loading) return <div style={{padding:'2rem',color:'#888'}}>Cargando sistema...</div>

  const tagColor = s => ({
    completada: '#555', pendiente: '#ffaa00', en_cola: '#00aaff', ejecutando: '#ff8800'
  }[s] || '#555')

  return (
    <div style={{padding:'1.5rem',background:'#0a0a0a',minHeight:'100vh',color:'#e0e0e0',fontFamily:'monospace'}}>
      <h1 style={{color:'#00ff88',marginBottom:'4px',fontSize:'1.4rem'}}>⬡ LAMAUTONOMIA</h1>
      <p style={{color:'#555',fontSize:'0.8rem',marginBottom:'1.5rem'}}>auto-refresh 10s</p>

      <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(280px,1fr))',gap:'1rem'}}>

        {/* CONTENEDORES */}
        <div style={{background:'#111',border:'1px solid #222',borderRadius:'8px',padding:'1rem'}}>
          <h2 style={{color:'#00aaff',fontSize:'0.85rem',letterSpacing:'2px',marginBottom:'12px'}}>CONTENEDORES</h2>
          {stack.map(c => (
            <div key={c.name} style={{display:'flex',justifyContent:'space-between',padding:'6px 0',borderBottom:'1px solid #1a1a1a',fontSize:'0.82rem'}}>
              <span>
                <span style={{display:'inline-block',width:'8px',height:'8px',borderRadius:'50%',background:c.status==='running'?'#00ff88':'#ff4444',marginRight:'6px'}}/>
                {c.name}
              </span>
              <span style={{color:c.status==='running'?'#00ff88':'#ff4444'}}>{c.status}</span>
            </div>
          ))}
        </div>

        {/* HB JEWELRY GATEWAY */}
        <div style={{background:'#111',border:'1px solid #222',borderRadius:'8px',padding:'1rem'}}>
          <h2 style={{color:'#00aaff',fontSize:'0.85rem',letterSpacing:'2px',marginBottom:'12px'}}>HB JEWELRY — GATEWAY</h2>
          <div style={{display:'flex',justifyContent:'space-between',padding:'6px 0',borderBottom:'1px solid #1a1a1a',fontSize:'0.82rem'}}>
            <span>estado</span>
            <span style={{color:gateway.status==='healthy'?'#00ff88':'#ff4444'}}>{gateway.status||'sin respuesta'}</span>
          </div>
          {(gateway.agents||[]).map(a => (
            <div key={a} style={{display:'flex',justifyContent:'space-between',padding:'6px 0',borderBottom:'1px solid #1a1a1a',fontSize:'0.82rem'}}>
              <span style={{color:'#ff88ff'}}>⬡ {a}</span>
              <span style={{color:'#00ff88'}}>activo</span>
            </div>
          ))}
        </div>

        {/* DAG TAREAS */}
        <div style={{background:'#111',border:'1px solid #222',borderRadius:'8px',padding:'1rem'}}>
          <h2 style={{color:'#00aaff',fontSize:'0.85rem',letterSpacing:'2px',marginBottom:'12px'}}>DAG — TAREAS</h2>
          {Object.entries(tareas).map(([k, v]) => (
            <div key={k} style={{display:'flex',justifyContent:'space-between',padding:'6px 0',borderBottom:'1px solid #1a1a1a',fontSize:'0.82rem'}}>
              <span>{k.replace(/_/g,' ')}</span>
              <span style={{fontSize:'0.7rem',padding:'2px 8px',borderRadius:'4px',color:tagColor(v.estado),border:`1px solid ${tagColor(v.estado)}40`,background:`${tagColor(v.estado)}20`}}>{v.estado}</span>
            </div>
          ))}
        </div>

      </div>
    </div>
  )
}