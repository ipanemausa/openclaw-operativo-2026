import React, { useState } from 'react';

// ─── CLOUD-FIRST & DYNAMIC CACHE BUSTING ──────────────────────────────────────
const CLOUD_BASE = 'https://hb-jewelry-app.web.app';
const IS_PROD = window.location.hostname !== 'localhost';
const asset = (f) => (IS_PROD ? `${CLOUD_BASE}/${f}?v=20260801_vExecutiveHub` : `/${f}?v=20260801_vExecutiveHub`);

/* ═══════════════════════════════════════════════════════════════════════════
   EXECUTIVE COMMAND DASHBOARD (2 MASTER LAUNCH BUTTONS + 6 BUSINESS CARDS)
   ═══════════════════════════════════════════════════════════════════════════ */
export default function Dashboard({ onNavigate }) {
  const [hoverAvatars, setHoverAvatars] = useState(false);
  const [hoverVideos, setHoverVideos] = useState(false);
  const [hoverCard, setHoverCard] = useState(null);

  const handleNav = (target) => {
    if (onNavigate) {
      onNavigate(target);
    }
  };

  return (
    <div style={{ padding: '28px 32px', maxWidth: 1440, margin: '0 auto', color: '#fff', fontFamily: 'Inter, system-ui, sans-serif' }}>
      
      {/* ─── CABECERA EJECUTIVA DE ALTO IMPACTO ─── */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 28, paddingBottom: 16, borderBottom: '1px solid rgba(212,175,106,0.2)' }}>
        <div>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8, padding: '4px 12px', borderRadius: 20, background: 'linear-gradient(135deg, #b45309 0%, #78350f 100%)', border: '1px solid #fbbf24', color: '#fbbf24', fontSize: 11, fontWeight: 800, letterSpacing: 1 }}>
            <span>✨ OPENCLAW ENTERPRISE v2026.7.1</span>
            <span style={{ color: '#4ade80', fontSize: 10 }}>● ONLINE</span>
          </div>

          <h1 style={{ fontSize: 26, fontWeight: 900, color: '#ffffff', margin: '8px 0 4px 0', letterSpacing: '-0.5px' }}>
            Plataforma Integrada de Control y Operaciones
          </h1>
          <p style={{ fontSize: 13, color: '#94a3b8', margin: 0 }}>
            Visión global del negocio: Avatares 3D, Estudio de Video, Ventas WhatsApp $0, RAG 768-dim y Respaldo Cloud 5TB
          </p>
        </div>

        <div style={{ display: 'flex', gap: 10 }}>
          <div style={{ background: 'rgba(15,23,42,0.85)', border: '1px solid rgba(251,191,36,0.3)', padding: '8px 14px', borderRadius: 10, textAlign: 'right' }}>
            <div style={{ color: '#fbbf24', fontSize: 12, fontWeight: 800 }}>HB Jewelry 18k</div>
            <div style={{ color: '#94a3b8', fontSize: 10 }}>Firebase Cloud CDN</div>
          </div>
          <div style={{ background: 'rgba(15,23,42,0.85)', border: '1px solid rgba(52,211,153,0.3)', padding: '8px 14px', borderRadius: 10, textAlign: 'right' }}>
            <div style={{ color: '#34d399', fontSize: 12, fontWeight: 800 }}>Rclone Drive 5TB</div>
            <div style={{ color: '#94a3b8', fontSize: 10 }}>Pipeline DAG Sincronizado</div>
          </div>
        </div>
      </div>

      {/* ─── 2 BOTONES PRINCIPALES DE DESPLIEGUE (PANTONE STYLED) ─── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginBottom: 32 }}>
        
        {/* BOTÓN 1: DESPLEGAR AVATARES 3D */}
        <div
          onClick={() => handleNav('avatar')}
          onMouseEnter={() => setHoverAvatars(true)}
          onMouseLeave={() => setHoverAvatars(false)}
          style={{
            cursor: 'pointer',
            borderRadius: 18,
            padding: '28px 28px',
            background: hoverAvatars 
              ? 'linear-gradient(145deg, #1e1b4b 0%, #0f172a 100%)' 
              : 'linear-gradient(145deg, #111827 0%, #0b0f19 100%)',
            backdropFilter: 'blur(16px)',
            border: hoverAvatars ? '2px solid #fbbf24' : '1px solid rgba(251,191,36,0.35)',
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            transform: hoverAvatars ? 'translateY(-4px)' : 'none',
            boxShadow: hoverAvatars ? '0 16px 40px rgba(251,191,36,0.25)' : '0 8px 24px rgba(0,0,0,0.5)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            minHeight: 220
          }}
        >
          <div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 }}>
              <span style={{ padding: '4px 10px', borderRadius: 20, background: '#b45309', color: '#fff', fontSize: 10, fontWeight: 900, letterSpacing: 1 }}>
                👑 PARRILLA 6 COLUMNAS
              </span>
              <span style={{ fontSize: 24 }}>👤</span>
            </div>
            <h2 style={{ fontSize: 22, fontWeight: 900, color: '#ffffff', margin: '0 0 6px 0' }}>
              Avatares Digitales 3D (Guillermo AI)
            </h2>
            <p style={{ fontSize: 12, color: '#cbd5e1', lineHeight: 1.5, margin: 0 }}>
              Catálogo tridimensional de 8 avatares oficiales con fotos estáticas PNG transparentes RGBA e Inspector 3D FLAME.
            </p>
          </div>

          <div style={{
            marginTop: 18,
            padding: '12px 20px',
            borderRadius: 10,
            background: 'linear-gradient(135deg, #fbbf24 0%, #d4af6a 100%)',
            color: '#000',
            fontWeight: 900,
            fontSize: 12,
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            boxShadow: '0 4px 16px rgba(251,191,36,0.3)'
          }}>
            <span>👑 DESPLEGAR SECCIÓN DE AVATARES 3D</span>
            <span style={{ fontSize: 14 }}>➔</span>
          </div>
        </div>

        {/* BOTÓN 2: DESPLEGAR ESTUDIO DE VIDEOS */}
        <div
          onClick={() => handleNav('marketing')}
          onMouseEnter={() => setHoverVideos(true)}
          onMouseLeave={() => setHoverVideos(false)}
          style={{
            cursor: 'pointer',
            borderRadius: 18,
            padding: '28px 28px',
            background: hoverVideos 
              ? 'linear-gradient(145deg, #450a0a 0%, #0f172a 100%)' 
              : 'linear-gradient(145deg, #111827 0%, #0b0f19 100%)',
            backdropFilter: 'blur(16px)',
            border: hoverVideos ? '2px solid #ef4444' : '1px solid rgba(239,68,68,0.35)',
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            transform: hoverVideos ? 'translateY(-4px)' : 'none',
            boxShadow: hoverVideos ? '0 16px 40px rgba(239,68,68,0.25)' : '0 8px 24px rgba(0,0,0,0.5)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            minHeight: 220
          }}
        >
          <div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 }}>
              <span style={{ padding: '4px 10px', borderRadius: 20, background: '#991b1b', color: '#fff', fontSize: 10, fontWeight: 900, letterSpacing: 1 }}>
                🔴 8 VIDEOS MP4 ÚNICOS
              </span>
              <span style={{ fontSize: 24 }}>🎬</span>
            </div>
            <h2 style={{ fontSize: 22, fontWeight: 900, color: '#ffffff', margin: '0 0 6px 0' }}>
              Estudio de Video & Cursos de Automatización
            </h2>
            <p style={{ fontSize: 12, color: '#cbd5e1', lineHeight: 1.5, margin: 0 }}>
              Parrilla de 6 columnas con videos de 7 Hacks de Claude, voz real FM estéreo a 48kHz y subtítulos bilingües.
            </p>
          </div>

          <div style={{
            marginTop: 18,
            padding: '12px 20px',
            borderRadius: 10,
            background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
            color: '#fff',
            fontWeight: 900,
            fontSize: 12,
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            boxShadow: '0 4px 16px rgba(239,68,68,0.3)'
          }}>
            <span>🔴 DESPLEGAR ESTUDIO DE VIDEOS Y CURSOS</span>
            <span style={{ fontSize: 14 }}>➔</span>
          </div>
        </div>

      </div>

      {/* ─── 6 CARDS DE OPERACIÓN GLOBAL DEL NEGOCIO (RECONSTRUIDAS) ─── */}
      <div style={{ marginBottom: 14 }}>
        <h3 style={{ fontSize: 16, fontWeight: 900, color: '#fbbf24', margin: '0 0 14px 0', display: 'flex', alignItems: 'center', gap: 8 }}>
          <span>🌐 MÓDULOS OPERATIVOS DEL ECOSISTEMA DE NEGOCIO</span>
        </h3>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
        
        {/* CARD 1: VENTAS & CATALOGO */}
        <div
          onClick={() => handleNav('ventas')}
          onMouseEnter={() => setHoverCard('ventas')}
          onMouseLeave={() => setHoverCard(null)}
          style={{
            cursor: 'pointer',
            borderRadius: 14,
            padding: '18px 20px',
            background: hoverCard === 'ventas' ? 'linear-gradient(145deg, #1e1b4b 0%, #090d16 100%)' : '#090d16',
            border: hoverCard === 'ventas' ? '1px solid #fbbf24' : '1px solid rgba(255,255,255,0.08)',
            transition: 'all 0.2s ease',
            transform: hoverCard === 'ventas' ? 'translateY(-2px)' : 'none'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
            <span style={{ color: '#fbbf24', fontSize: 13, fontWeight: 800 }}>💎 Ventas & Catálogo 18k</span>
            <span style={{ fontSize: 18 }}>◆</span>
          </div>
          <p style={{ fontSize: 11, color: '#94a3b8', margin: '0 0 10px 0' }}>
            Colección de Joyería Fina HB Jewelry con checkout automático y cierre directo a WhatsApp $0.
          </p>
          <div style={{ color: '#fbbf24', fontSize: 10, fontWeight: 700 }}>VER SECCIÓN DE VENTAS ➔</div>
        </div>

        {/* CARD 2: AGENTES IA & RAG */}
        <div
          onClick={() => handleNav('chat')}
          onMouseEnter={() => setHoverCard('chat')}
          onMouseLeave={() => setHoverCard(null)}
          style={{
            cursor: 'pointer',
            borderRadius: 14,
            padding: '18px 20px',
            background: hoverCard === 'chat' ? 'linear-gradient(145deg, #1e1b4b 0%, #090d16 100%)' : '#090d16',
            border: hoverCard === 'chat' ? '1px solid #60a5fa' : '1px solid rgba(255,255,255,0.08)',
            transition: 'all 0.2s ease',
            transform: hoverCard === 'chat' ? 'translateY(-2px)' : 'none'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
            <span style={{ color: '#60a5fa', fontSize: 13, fontWeight: 800 }}>🤖 Agentes IA & RAG 768-dim</span>
            <span style={{ fontSize: 18 }}>◎</span>
          </div>
          <p style={{ fontSize: 11, color: '#94a3b8', margin: '0 0 10px 0' }}>
            Orquestación de agentes autónomos con memoria RAG en Firestore y 7 Hacks de Claude 4.6.
          </p>
          <div style={{ color: '#60a5fa', fontSize: 10, fontWeight: 700 }}>ABRIR CHAT AGENTES ➔</div>
        </div>

        {/* CARD 3: WHATSAPP BUSINESS ($0) */}
        <div
          onClick={() => handleNav('integraciones')}
          onMouseEnter={() => setHoverCard('wa')}
          onMouseLeave={() => setHoverCard(null)}
          style={{
            cursor: 'pointer',
            borderRadius: 14,
            padding: '18px 20px',
            background: hoverCard === 'wa' ? 'linear-gradient(145deg, #064e3b 0%, #090d16 100%)' : '#090d16',
            border: hoverCard === 'wa' ? '1px solid #34d399' : '1px solid rgba(255,255,255,0.08)',
            transition: 'all 0.2s ease',
            transform: hoverCard === 'wa' ? 'translateY(-2px)' : 'none'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
            <span style={{ color: '#34d399', fontSize: 13, fontWeight: 800 }}>📲 WhatsApp Business ($0)</span>
            <span style={{ fontSize: 18 }}>💬</span>
          </div>
          <p style={{ fontSize: 11, color: '#94a3b8', margin: '0 0 10px 0' }}>
            Canal de ventas y atención autónoma 24/7 en puerto 3001 sin costo por mensaje.
          </p>
          <div style={{ color: '#34d399', fontSize: 10, fontWeight: 700 }}>CONFIGURAR WHATSAPP ➔</div>
        </div>

        {/* CARD 4: INVENTARIO & PRODUCTOS */}
        <div
          onClick={() => handleNav('inventario')}
          onMouseEnter={() => setHoverCard('inv')}
          onMouseLeave={() => setHoverCard(null)}
          style={{
            cursor: 'pointer',
            borderRadius: 14,
            padding: '18px 20px',
            background: hoverCard === 'inv' ? 'linear-gradient(145deg, #1e1b4b 0%, #090d16 100%)' : '#090d16',
            border: hoverCard === 'inv' ? '1px solid #a78bfa' : '1px solid rgba(255,255,255,0.08)',
            transition: 'all 0.2s ease',
            transform: hoverCard === 'inv' ? 'translateY(-2px)' : 'none'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
            <span style={{ color: '#a78bfa', fontSize: 13, fontWeight: 800 }}>📦 Control de Inventario</span>
            <span style={{ fontSize: 18 }}>▣</span>
          </div>
          <p style={{ fontSize: 11, color: '#94a3b8', margin: '0 0 10px 0' }}>
            Gestión de stock de piezas en oro 18k, diamantes e indicadores de reabastecimiento.
          </p>
          <div style={{ color: '#a78bfa', fontSize: 10, fontWeight: 700 }}>VER INVENTARIO ➔</div>
        </div>

        {/* CARD 5: ANALYTICS & REPORTES */}
        <div
          onClick={() => handleNav('analytics')}
          onMouseEnter={() => setHoverCard('an')}
          onMouseLeave={() => setHoverCard(null)}
          style={{
            cursor: 'pointer',
            borderRadius: 14,
            padding: '18px 20px',
            background: hoverCard === 'an' ? 'linear-gradient(145deg, #1e1b4b 0%, #090d16 100%)' : '#090d16',
            border: hoverCard === 'an' ? '1px solid #f43f5e' : '1px solid rgba(255,255,255,0.08)',
            transition: 'all 0.2s ease',
            transform: hoverCard === 'an' ? 'translateY(-2px)' : 'none'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
            <span style={{ color: '#f43f5e', fontSize: 13, fontWeight: 800 }}>📊 Analytics & Conversión</span>
            <span style={{ fontSize: 18 }}>📈</span>
          </div>
          <p style={{ fontSize: 11, color: '#94a3b8', margin: '0 0 10px 0' }}>
            Métricas de tráfico, conversión de ventas, engagement de avatares y retorno operativo.
          </p>
          <div style={{ color: '#f43f5e', fontSize: 10, fontWeight: 700 }}>ABRIR ANALYTICS ➔</div>
        </div>

        {/* CARD 6: PIPELINE DAG & RESPALDO 5TB */}
        <div
          onClick={() => handleNav('pipeline')}
          onMouseEnter={() => setHoverCard('pipe')}
          onMouseLeave={() => setHoverCard(null)}
          style={{
            cursor: 'pointer',
            borderRadius: 14,
            padding: '18px 20px',
            background: hoverCard === 'pipe' ? 'linear-gradient(145deg, #1e1b4b 0%, #090d16 100%)' : '#090d16',
            border: hoverCard === 'pipe' ? '1px solid #cbd5e1' : '1px solid rgba(255,255,255,0.08)',
            transition: 'all 0.25s ease',
            transform: hoverCard === 'pipe' ? 'translateY(-2px)' : 'none'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
            <span style={{ color: '#cbd5e1', fontSize: 13, fontWeight: 800 }}>⚡ Pipeline DAG & Drive 5TB</span>
            <span style={{ fontSize: 18 }}>☁️</span>
          </div>
          <p style={{ fontSize: 11, color: '#94a3b8', margin: '0 0 10px 0' }}>
            Estado de tareas en segundo plano, respaldos Rclone y despliegue autómata de cierre.
          </p>
          <div style={{ color: '#cbd5e1', fontSize: 10, fontWeight: 700 }}>VER MONITOR PIPELINE ➔</div>
        </div>

      </div>

    </div>
  );
}
