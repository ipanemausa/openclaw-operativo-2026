import React, { useState } from 'react'

// ─── CLOUD-FIRST & DYNAMIC CACHE BUSTING ──────────────────────────────────────
const CLOUD_BASE = 'https://hb-jewelry-app.web.app'
const IS_PROD = window.location.hostname !== 'localhost'
const asset = (f) => (IS_PROD ? `${CLOUD_BASE}/${f}?v=20260801_vMinimal` : `/${f}?v=20260801_vMinimal`)

/* ═══════════════════════════════════════════════════════════════════════════
   ULTRA-CLEAN EXECUTIVE DASHBOARD (2 MASTER LAUNCH BUTTONS)
   ═══════════════════════════════════════════════════════════════════════════ */
export default function Dashboard({ onNavigate }) {
  const [hoverAvatars, setHoverAvatars] = useState(false)
  const [hoverVideos, setHoverVideos] = useState(false)

  const handleNav = (target) => {
    if (onNavigate) {
      onNavigate(target)
    }
  }

  return (
    <div style={{ padding: '32px 36px', maxWidth: 1280, margin: '0 auto', color: '#fff', fontFamily: 'Inter, system-ui, sans-serif' }}>
      
      {/* ─── CABECERA EJECUTIVA LIMPIA ─── */}
      <div style={{ textAlign: 'center', marginBottom: 40 }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8, padding: '6px 16px', borderRadius: 20, background: 'rgba(212,175,106,0.1)', border: '1px solid rgba(212,175,106,0.3)', color: '#fbbf24', fontSize: 11, fontWeight: 800, letterSpacing: 1.5, marginBottom: 12 }}>
          <span>✨ OPENCLAW ENTERPRISE v2026.7.1</span>
          <span style={{ color: '#4ade80', fontSize: 10 }}>● ONLINE</span>
        </div>

        <h1 style={{ fontSize: 32, fontWeight: 900, color: '#ffffff', margin: '0 0 8px 0', letterSpacing: '-0.8px' }}>
          Plataforma de Control Integrada
        </h1>
        <p style={{ fontSize: 14, color: '#94a3b8', margin: 0, maxWidth: 640, margin: '0 auto', lineHeight: 1.5 }}>
          Seleccione una de las secciones principales a continuación para desplegar el catálogo de modelos o el estudio de video.
        </p>
      </div>

      {/* ─── 2 BOTONES / CARDS PRINCIPALES DE DESPLIEGUE ─── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 28, marginBottom: 40 }}>
        
        {/* BOTÓN 1: DESPLEGAR AVATARES 3D */}
        <div
          onClick={() => handleNav('avatar')}
          onMouseEnter={() => setHoverAvatars(true)}
          onMouseLeave={() => setHoverAvatars(false)}
          style={{
            cursor: 'pointer',
            borderRadius: 20,
            padding: '36px 32px',
            background: hoverAvatars ? 'linear-gradient(145deg, #1e1b4b 0%, #0f172a 100%)' : 'rgba(15, 23, 42, 0.75)',
            backdropFilter: 'blur(16px)',
            border: hoverAvatars ? '2px solid #fbbf24' : '1px solid rgba(212,175,106,0.25)',
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            transform: hoverAvatars ? 'translateY(-6px)' : 'none',
            boxShadow: hoverAvatars ? '0 20px 45px rgba(251,191,36,0.25)' : '0 10px 30px rgba(0,0,0,0.5)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            alignItems: 'flex-start',
            minHeight: 280
          }}
        >
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 16 }}>
              <span style={{ fontSize: 32 }}>👑</span>
              <span style={{ padding: '4px 10px', borderRadius: 8, background: '#b45309', color: '#fff', fontSize: 11, fontWeight: 900, letterSpacing: 1 }}>
                6 MODELOS 3D
              </span>
            </div>
            <h2 style={{ fontSize: 24, fontWeight: 900, color: '#ffffff', margin: '0 0 10px 0' }}>
              Avatares Digitales 3D
            </h2>
            <p style={{ fontSize: 13, color: '#cbd5e1', lineHeight: 1.6, margin: 0 }}>
              Catálogo completo con malla facial 3D FLAME, gesticulación vocal anatómica y transparencia PNG RGBA.
            </p>
          </div>

          <div style={{
            marginTop: 24,
            padding: '14px 24px',
            borderRadius: 12,
            background: 'linear-gradient(135deg, #fbbf24 0%, #d4af6a 100%)',
            color: '#000',
            fontWeight: 900,
            fontSize: 13,
            display: 'inline-flex',
            alignItems: 'center',
            gap: 10,
            boxShadow: '0 6px 20px rgba(251,191,36,0.3)'
          }}>
            <span>DESPLEGAR SECCIÓN DE AVATARES</span>
            <span style={{ fontSize: 16 }}>➔</span>
          </div>
        </div>

        {/* BOTÓN 2: DESPLEGAR ESTUDIO DE VIDEOS */}
        <div
          onClick={() => handleNav('marketing')}
          onMouseEnter={() => setHoverVideos(true)}
          onMouseLeave={() => setHoverVideos(false)}
          style={{
            cursor: 'pointer',
            borderRadius: 20,
            padding: '36px 32px',
            background: hoverVideos ? 'linear-gradient(145deg, #3f0d0d 0%, #180909 100%)' : 'rgba(15, 23, 42, 0.75)',
            backdropFilter: 'blur(16px)',
            border: hoverVideos ? '2px solid #ef4444' : '1px solid rgba(239,68,68,0.25)',
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            transform: hoverVideos ? 'translateY(-6px)' : 'none',
            boxShadow: hoverVideos ? '0 20px 45px rgba(239,68,68,0.25)' : '0 10px 30px rgba(0,0,0,0.5)',
            display: 'flex',
            flexDirection: 'column',
            justify: 'space-between',
            alignItems: 'flex-start',
            minHeight: 280
          }}
        >
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 16 }}>
              <span style={{ fontSize: 32 }}>🔴</span>
              <span style={{ padding: '4px 10px', borderRadius: 8, background: '#991b1b', color: '#fff', fontSize: 11, fontWeight: 900, letterSpacing: 1 }}>
                6 VIDEOS MASTER
              </span>
            </div>
            <h2 style={{ fontSize: 24, fontWeight: 900, color: '#ffffff', margin: '0 0 10px 0' }}>
              Estudio de Video & Cursos AI
            </h2>
            <p style={{ fontSize: 13, color: '#cbd5e1', lineHeight: 1.6, margin: 0 }}>
              Cursos de automatización con 7 Hacks de Claude 4.6, audio estéreo a 48kHz y base bilingüe de 2 columnas.
            </p>
          </div>

          <div style={{
            marginTop: 24,
            padding: '14px 24px',
            borderRadius: 12,
            background: 'linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)',
            color: '#fff',
            fontWeight: 900,
            fontSize: 13,
            display: 'inline-flex',
            alignItems: 'center',
            gap: 10,
            boxShadow: '0 6px 20px rgba(239,68,68,0.3)'
          }}>
            <span>DESPLEGAR ESTUDIO DE VIDEOS</span>
            <span style={{ fontSize: 16 }}>➔</span>
          </div>
        </div>

      </div>

      {/* ─── PIE COMPACTO DE INFRAESTRUCTURA ─── */}
      <div style={{ textAlign: 'center', padding: '16px 20px', borderRadius: 14, background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.06)', display: 'flex', justifyContent: 'space-around', alignItems: 'center', fontSize: 12, color: '#94a3b8' }}>
        <span>📦 Stack Docker: <strong style={{ color: '#4ade80' }}>Activo</strong></span>
        <span>🌐 Gateway: <strong style={{ color: '#4ade80' }}>Conectado</strong></span>
        <span>⚡ Memoria RAG: <strong style={{ color: '#fbbf24' }}>768 Dimensiones</strong></span>
        <span>☁️ Respaldo Nube: <strong style={{ color: '#60a5fa' }}>Google Drive 5TB</strong></span>
      </div>

    </div>
  )
}
