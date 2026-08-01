import React, { useState, memo } from 'react'

// ─── CLOUD-FIRST & DYNAMIC CACHE BUSTING ──────────────────────────────────────
const CLOUD_BASE = 'https://hb-jewelry-app.web.app'
const IS_PROD = window.location.hostname !== 'localhost'
const asset = (f) => (IS_PROD ? `${CLOUD_BASE}/${f}?v=20260801_v3D_Hero` : `/${f}?v=20260801_v3D_Hero`)

/* ═══════════════════════════════════════════════════════════════════════════
   STATS PANEL (Sleek Glassmorphism System Metrics)
   ═══════════════════════════════════════════════════════════════════════════ */
const Stats = ({ stack, tareas, gateway }) => {
  const ec = s => ({ completada: '#4ade80', pendiente: '#fbbf24', en_cola: '#60a5fa', ejecutando: '#fb923c' }[s] || '#888')
  const card = {
    background: 'rgba(15, 23, 42, 0.65)',
    backdropFilter: 'blur(12px)',
    border: '1px solid rgba(212, 175, 106, 0.2)',
    borderRadius: 14,
    padding: 16,
    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)'
  }
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 14, marginTop: 12 }}>
      <div style={card}>
        <div style={{ color: '#d4af6a', fontSize: 11, letterSpacing: 2, fontWeight: 800, marginBottom: 12, display: 'flex', alignItems: 'center', gap: 6 }}>
          <span>📦</span> <span>STACK DOCKER GORDON</span>
        </div>
        {stack.map(c => (
          <div key={c.name} style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0', borderBottom: '1px solid rgba(255,255,255,0.04)', fontSize: 12 }}>
            <span style={{ color: '#e2e8f0', display: 'flex', alignItems: 'center' }}>
              <span style={{ width: 7, height: 7, borderRadius: '50%', background: c.status === 'running' ? '#4ade80' : '#fb7185', display: 'inline-block', marginRight: 8, boxShadow: c.status === 'running' ? '0 0 8px #4ade80' : 'none' }} />
              {c.name}
            </span>
            <span style={{ color: c.status === 'running' ? '#4ade80' : '#fb7185', fontSize: 11, fontWeight: 700 }}>{c.status.toUpperCase()}</span>
          </div>
        ))}
      </div>

      <div style={card}>
        <div style={{ color: '#d4af6a', fontSize: 11, letterSpacing: 2, fontWeight: 800, marginBottom: 12, display: 'flex', alignItems: 'center', gap: 6 }}>
          <span>🌐</span> <span>GATEWAY & ORQUESTADOR</span>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0', fontSize: 12, borderBottom: '1px solid rgba(255,255,255,0.04)', marginBottom: 6 }}>
          <span style={{ color: '#94a3b8' }}>Estado del Gateway</span>
          <span style={{ color: gateway.status === 'ok' ? '#4ade80' : '#fb7185', fontWeight: 800 }}>{gateway.status.toUpperCase()}</span>
        </div>
        {(gateway.agents || []).map(a => (
          <div key={a} style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0', borderBottom: '1px solid rgba(255,255,255,0.04)', fontSize: 12 }}>
            <span style={{ color: '#f59e0b', fontWeight: 600 }}>{a}</span>
            <span style={{ color: '#4ade80', fontSize: 11, fontWeight: 700 }}>ACTIVO</span>
          </div>
        ))}
      </div>

      <div style={card}>
        <div style={{ color: '#d4af6a', fontSize: 11, letterSpacing: 2, fontWeight: 800, marginBottom: 12, display: 'flex', alignItems: 'center', gap: 6 }}>
          <span>⚡</span> <span>TAREAS DAG RAG & NUBE</span>
        </div>
        {Object.entries(tareas).map(([k, v]) => (
          <div key={k} style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0', borderBottom: '1px solid rgba(255,255,255,0.04)', fontSize: 12 }}>
            <span style={{ color: '#cbd5e1' }}>{k.replace(/_/g, ' ').toUpperCase()}</span>
            <span style={{ fontSize: 10, padding: '2px 8px', borderRadius: 4, color: ec(v.estado), border: `1px solid ${ec(v.estado)}44`, background: `${ec(v.estado)}18`, fontWeight: 800 }}>
              {v.estado.toUpperCase()}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}

/* ═══════════════════════════════════════════════════════════════════════════
   MAIN UNIFIED DASHBOARD COMPONENT (2 HERO CARDS ARCHITECTURE)
   ═══════════════════════════════════════════════════════════════════════════ */
export default function Dashboard({ onNavigate }) {
  const [hoverAvatars, setHoverAvatars] = useState(false)
  const [hoverVideos, setHoverVideos] = useState(false)

  const handleNav = (target) => {
    if (onNavigate) {
      onNavigate(target)
    }
  }

  const stack = [
    { name: 'voice_worker', status: 'running' },
    { name: 'video_veo_worker', status: 'running' },
    { name: 'financial_rag_worker', status: 'running' },
    { name: 'chat_worker', status: 'running' }
  ]

  const tareas = {
    vectorizacion_rag_768dim: { estado: 'completada' },
    sintesis_3d_flame_mesh: { estado: 'completada' },
    audio_estereo_48khz_ebu: { estado: 'completada' },
    pipeline_cierre_gdrive_5tb: { estado: 'completada' }
  }

  const gateway = { status: 'ok', agents: ['claw-orchestrator', 'openclaw_gateway'] }

  return (
    <div style={{ padding: '24px 28px', maxWidth: 1440, margin: '0 auto', color: '#fff', fontFamily: 'Inter, system-ui, sans-serif' }}>
      
      {/* CABECERA PRINCIPAL REFINADA */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24, paddingBottom: 16, borderBottom: '1px solid rgba(212,175,106,0.2)' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <span style={{ padding: '4px 12px', borderRadius: 20, background: 'linear-gradient(135deg, #b45309 0%, #78350f 100%)', color: '#fbbf24', fontSize: 11, fontWeight: 800, letterSpacing: 1, border: '1px solid #fbbf24' }}>
              OPENCLAW ENTERPRISE v2026.7.1
            </span>
            <span style={{ color: '#4ade80', fontSize: 12, fontWeight: 700, display: 'flex', alignItems: 'center', gap: 4 }}>
              <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#4ade80', boxShadow: '0 0 8px #4ade80' }} />
              Nube Firebase CDN & Drive 5TB Activo
            </span>
          </div>
          <h1 style={{ fontSize: 26, fontWeight: 900, color: '#ffffff', margin: '8px 0 4px 0', letterSpacing: '-0.5px' }}>
            Panel de Control Maestro: Humano Digital 3D & Estudio de Video AI
          </h1>
          <p style={{ fontSize: 13, color: '#94a3b8', margin: 0 }}>
            Arquitectura Unificada con Claude 4.6, Malla Facial 3D FLAME, Audio Estéreo a 48kHz y Base RAG de 768 Dimensiones
          </p>
        </div>
        
        <div style={{ display: 'flex', gap: 12 }}>
          <div style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(212,175,106,0.2)', padding: '10px 16px', borderRadius: 12, textAlign: 'center' }}>
            <div style={{ color: '#fbbf24', fontSize: 18, fontWeight: 900 }}>6</div>
            <div style={{ color: '#94a3b8', fontSize: 10, fontWeight: 700, letterSpacing: 0.5 }}>AVATARES 3D</div>
          </div>
          <div style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(239,68,68,0.3)', padding: '10px 16px', borderRadius: 12, textAlign: 'center' }}>
            <div style={{ color: '#ef4444', fontSize: 18, fontWeight: 900 }}>6</div>
            <div style={{ color: '#94a3b8', fontSize: 10, fontWeight: 700, letterSpacing: 0.5 }}>VIDEOS MASTER</div>
          </div>
        </div>
      </div>

      {/* ─── ARQUITECTURA LIMPIA: 2 CARDS HERO DE INTEGRACIÓN DASHBOARD ─── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginBottom: 28 }}>
        
        {/* CARD 1: HERO AVATARES DIGITALES 3D */}
        <div
          onClick={() => handleNav('avatar')}
          onMouseEnter={() => setHoverAvatars(true)}
          onMouseLeave={() => setHoverAvatars(false)}
          style={{
            cursor: 'pointer',
            borderRadius: 20,
            overflow: 'hidden',
            position: 'relative',
            background: 'linear-gradient(145deg, #0f172a 0%, #1e1b4b 60%, #090d16 100%)',
            border: hoverAvatars ? '2px solid #fbbf24' : '1px solid rgba(212,175,106,0.3)',
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            transform: hoverAvatars ? 'translateY(-6px)' : 'none',
            boxShadow: hoverAvatars ? '0 24px 50px rgba(251,191,36,0.35)' : '0 10px 30px rgba(0,0,0,0.6)',
            display: 'flex',
            flexDirection: 'column',
            justify: 'space-between',
            height: 380
          }}
        >
          {/* Fondo Visual Avatar */}
          <div style={{ position: 'absolute', inset: 0, overflow: 'hidden', opacity: 0.55 }}>
            <img
              src={asset('avatar_pro.png')}
              alt="Avatar Master 3D"
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                objectPosition: 'top center',
                filter: hoverAvatars ? 'scale(1.05) brightness(1.1)' : 'brightness(0.95)',
                transition: 'transform 0.5s ease, filter 0.3s ease'
              }}
            />
            <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(to top, #0f172a 15%, transparent 75%)' }} />
          </div>

          {/* Badge Superior */}
          <div style={{ position: 'relative', zIndex: 3, padding: '20px 24px 0 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ padding: '6px 14px', borderRadius: 20, background: 'linear-gradient(135deg, #f59e0b 0%, #b45309 100%)', color: '#fff', fontSize: 11, fontWeight: 900, letterSpacing: 1, boxShadow: '0 4px 12px rgba(245,158,11,0.4)' }}>
              👑 CATÁLOGO DE AVATARES 3D (GUILLERMO AI)
            </span>
            <span style={{ background: 'rgba(0,0,0,0.75)', border: '1px solid rgba(255,255,255,0.2)', padding: '4px 10px', borderRadius: 8, color: '#fbbf24', fontSize: 12, fontWeight: 800 }}>
              6 Modelos Registrados
            </span>
          </div>

          {/* Contenido Inferior */}
          <div style={{ position: 'relative', zIndex: 3, padding: 24 }}>
            <h3 style={{ fontSize: 22, fontWeight: 900, color: '#ffffff', marginBottom: 8, textShadow: '0 2px 10px rgba(0,0,0,0.9)' }}>
              Guillermo AI Avatar Master 3D Mesh
            </h3>
            <p style={{ fontSize: 13, color: '#cbd5e1', lineHeight: 1.5, marginBottom: 16, maxWidth: '92%', textShadow: '0 1px 4px rgba(0,0,0,0.8)' }}>
              Reconstrucción de Malla Facial 3D FLAME, Rigging Esquelético Volumétrico $(X,Y,Z)$, Parpadeo y Gesticulación Vocal Anatómica.
            </p>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: 10, padding: '12px 22px', borderRadius: 12, background: 'linear-gradient(135deg, #fbbf24 0%, #d4af6a 100%)', color: '#000', fontWeight: 900, fontSize: 13, boxShadow: '0 6px 20px rgba(251,191,36,0.4)' }}>
              <span>ENTRAR A LA PESTAÑA DE AVATARES</span>
              <span style={{ fontSize: 16 }}>➔</span>
            </div>
          </div>
        </div>

        {/* CARD 2: HERO ESTUDIO DE VIDEO & CURSOS CLAUDE 4.6 */}
        <div
          onClick={() => handleNav('marketing')}
          onMouseEnter={() => setHoverVideos(true)}
          onMouseLeave={() => setHoverVideos(false)}
          style={{
            cursor: 'pointer',
            borderRadius: 20,
            overflow: 'hidden',
            position: 'relative',
            background: 'linear-gradient(145deg, #180909 0%, #3f0d0d 60%, #090d16 100%)',
            border: hoverVideos ? '2px solid #ef4444' : '1px solid rgba(239,68,68,0.4)',
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            transform: hoverVideos ? 'translateY(-6px)' : 'none',
            boxShadow: hoverVideos ? '0 24px 50px rgba(239,68,68,0.35)' : '0 10px 30px rgba(0,0,0,0.6)',
            display: 'flex',
            flexDirection: 'column',
            justify: 'space-between',
            height: 380
          }}
        >
          {/* Fondo Visual Video Poster */}
          <div style={{ position: 'absolute', inset: 0, overflow: 'hidden', opacity: 0.55 }}>
            <img
              src={asset('posters/poster_yt_special.png')}
              alt="Estudio de Video AI"
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                objectPosition: 'center',
                filter: hoverVideos ? 'scale(1.05) brightness(1.1)' : 'brightness(0.95)',
                transition: 'transform 0.5s ease, filter 0.3s ease'
              }}
            />
            <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(to top, #180909 15%, transparent 75%)' }} />
          </div>

          {/* Badge Superior */}
          <div style={{ position: 'relative', zIndex: 3, padding: '20px 24px 0 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ padding: '6px 14px', borderRadius: 20, background: 'linear-gradient(135deg, #dc2626 0%, #991b1b 100%)', color: '#fff', fontSize: 11, fontWeight: 900, letterSpacing: 1, boxShadow: '0 4px 12px rgba(220,38,38,0.4)' }}>
              🔴 ESTUDIO DE VIDEO & CURSOS CLAUDE 4.6
            </span>
            <span style={{ background: 'rgba(0,0,0,0.75)', border: '1px solid rgba(255,255,255,0.2)', padding: '4px 10px', borderRadius: 8, color: '#f87171', fontSize: 12, fontWeight: 800 }}>
              6 Videos HD 1080p
            </span>
          </div>

          {/* Contenido Inferior */}
          <div style={{ position: 'relative', zIndex: 3, padding: 24 }}>
            <h3 style={{ fontSize: 22, fontWeight: 900, color: '#ffffff', marginBottom: 8, textShadow: '0 2px 10px rgba(0,0,0,0.9)' }}>
              7 Hacks de Claude AI & Automatización DaVinci
            </h3>
            <p style={{ fontSize: 13, color: '#cbd5e1', lineHeight: 1.5, marginBottom: 16, maxWidth: '92%', textShadow: '0 1px 4px rgba(0,0,0,0.8)' }}>
              Curso Completo de Agentes Autónomos (10 Min), Audio Estéreo a 48kHz (-14 LUFS), Subtítulos Amarillos Dinámicos y Base Bilingüe de 2 Columnas.
            </p>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: 10, padding: '12px 22px', borderRadius: 12, background: 'linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)', color: '#fff', fontWeight: 900, fontSize: 13, boxShadow: '0 6px 20px rgba(239,68,68,0.4)' }}>
              <span>ABRIR PESTAÑA DE VIDEOS Y CURSOS</span>
              <span style={{ fontSize: 16 }}>➔</span>
            </div>
          </div>
        </div>

      </div>

      {/* ESTADO DEL ECOSISTEMA Y TAREAS */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12, paddingBottom: 6, borderBottom: '1px solid rgba(212,175,106,0.18)' }}>
        <span style={{ color: '#d4af6a', fontWeight: 800, fontSize: 13 }}>⚙️ INFRAESTRUCTURA & ESTADO DEL ECOSISTEMA OPENCLAW</span>
        <span style={{ color: '#64748b', fontSize: 11 }}>Docker Stack & Task DAG Status</span>
      </div>
      
      <Stats stack={stack} tareas={tareas} gateway={gateway} />

    </div>
  )
}
