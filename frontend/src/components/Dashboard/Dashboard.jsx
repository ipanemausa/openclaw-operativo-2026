import React, { useState } from 'react';

// ─── CLOUD-FIRST & DYNAMIC CACHE BUSTING ──────────────────────────────────────
const CLOUD_BASE = 'https://hb-jewelry-app.web.app';
const IS_PROD = window.location.hostname !== 'localhost';
const asset = (f) => (IS_PROD ? `${CLOUD_BASE}/${f}?v=20260801_vSidebarUnified` : `/${f}?v=20260801_vSidebarUnified`);

// ─── REGISTROS DE ACTIVIDAD RECIENTE (100% PALETA DORADO SIDEBAR #d4af6a) ──────
const RECENT_ACTIVITIES = [
  { timestamp: '2026-08-01 03:25:40', evento: 'Pipeline DAG: Respaldo Rclone a Google Drive 5TB', division: 'Sistema & IT', estado: 'completado' },
  { timestamp: '2026-08-01 03:20:12', evento: 'Firebase Hosting CDN: Build de producción desplegado', division: 'Infraestructura', estado: 'completado' },
  { timestamp: '2026-08-01 03:15:05', evento: 'Motor Video RAG: Renderizado teleprompter caracteres paso a paso', division: 'Marketing AI', estado: 'completado' },
  { timestamp: '2026-08-01 03:00:00', evento: 'Vectorización RAG: 768 dimensiones cargadas en Firestore', division: 'Agentes IA', estado: 'completado' },
  { timestamp: '2026-08-01 02:45:18', evento: 'Servidor WhatsApp Business ($0): Escucha en puerto 3001', division: 'Ventas Directas', estado: 'completado' },
  { timestamp: '2026-08-01 02:30:00', evento: 'Catálogo HB Jewelry 18k: Actualización de stock de piezas finas', division: 'Inventario & Logística', estado: 'completado' }
];

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
    <div style={{ padding: '20px 24px', maxWidth: 1400, margin: '0 auto', color: '#f0ede8', fontFamily: 'Inter, system-ui, sans-serif' }}>
      
      {/* ─── CABECERA EJECUTIVA 100% UNIFICADA CON SIDEBAR (#d4af6a) ─── */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20, paddingBottom: 14, borderBottom: '1px solid rgba(212,175,106,0.15)' }}>
        <div>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: 6, padding: '3px 10px', borderRadius: 16, background: 'rgba(212,175,106,0.08)', border: '1px solid rgba(212,175,106,0.2)', color: '#d4af6a', fontSize: 10, fontWeight: 700, letterSpacing: 1 }}>
            <span>✨ OPENCLAW ENTERPRISE v2026.7.1</span>
            <span style={{ color: '#d4af6a', fontSize: 9 }}>● ONLINE</span>
          </div>

          <h1 style={{ fontSize: 22, fontWeight: 700, color: '#d4af6a', margin: '6px 0 2px 0', letterSpacing: '-0.3px' }}>
            Plataforma Integral de Control Corporativo
          </h1>
          <p style={{ fontSize: 12, color: '#a09d99', margin: 0 }}>
            Ecosistema de gestión para Directivas, CEO, Gerencia, Supervisores y Operaciones
          </p>
        </div>

        <div style={{ display: 'flex', gap: 8 }}>
          <div style={{ background: '#161412', border: '1px solid rgba(212,175,106,0.15)', padding: '6px 12px', borderRadius: 6, textAlign: 'right' }}>
            <div style={{ color: '#d4af6a', fontSize: 11, fontWeight: 700 }}>HB Jewelry 18k</div>
            <div style={{ color: '#6b6866', fontSize: 9 }}>Firebase CDN</div>
          </div>
          <div style={{ background: '#161412', border: '1px solid rgba(212,175,106,0.15)', padding: '6px 12px', borderRadius: 6, textAlign: 'right' }}>
            <div style={{ color: '#d4af6a', fontSize: 11, fontWeight: 700 }}>Drive 5TB</div>
            <div style={{ color: '#6b6866', fontSize: 9 }}>Rclone Sync</div>
          </div>
        </div>
      </div>

      {/* ─── SECCIÓN 1: 2 BOTONES MAESTROS (100% PALETA SIDEBAR DORADO Y NEGRO) ─── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 24 }}>
        
        {/* BOTÓN 1: DESPLEGAR AVATARES 3D */}
        <div
          onClick={() => handleNav('avatar')}
          onMouseEnter={() => setHoverAvatars(true)}
          onMouseLeave={() => setHoverAvatars(false)}
          style={{
            cursor: 'pointer',
            borderRadius: 8,
            padding: '20px',
            background: hoverAvatars ? 'rgba(212,175,106,0.08)' : '#161412',
            border: hoverAvatars ? '1px solid #d4af6a' : '1px solid rgba(212,175,106,0.15)',
            transition: 'all 0.2s ease',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            minHeight: 160
          }}
        >
          <div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 6 }}>
              <span style={{ padding: '2px 8px', borderRadius: 4, background: 'rgba(212,175,106,0.12)', border: '1px solid rgba(212,175,106,0.25)', color: '#d4af6a', fontSize: 10, fontWeight: 700, letterSpacing: 1 }}>
                PARRILLA 6 COLUMNAS
              </span>
              <span style={{ color: '#d4af6a', fontSize: 16 }}>👤</span>
            </div>
            <h2 style={{ fontSize: 18, fontWeight: 700, color: '#f0ede8', margin: '0 0 4px 0' }}>
              Avatares Digitales 3D (Guillermo AI)
            </h2>
            <p style={{ fontSize: 11, color: '#a09d99', lineHeight: 1.4, margin: 0 }}>
              Catálogo de 8 modelos oficiales con fotos estáticas PNG transparentes RGBA HD e Inspector 3D.
            </p>
          </div>

          <div style={{
            marginTop: 12,
            padding: '8px 14px',
            borderRadius: 6,
            background: hoverAvatars ? 'rgba(212,175,106,0.2)' : 'rgba(212,175,106,0.1)',
            border: '1px solid rgba(212,175,106,0.25)',
            color: '#d4af6a',
            fontWeight: 700,
            fontSize: 11,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}>
            <span>DESPLEGAR SECCIÓN DE AVATARES 3D</span>
            <span style={{ fontSize: 12 }}>➔</span>
          </div>
        </div>

        {/* BOTÓN 2: DESPLEGAR ESTUDIO DE VIDEOS */}
        <div
          onClick={() => handleNav('marketing')}
          onMouseEnter={() => setHoverVideos(true)}
          onMouseLeave={() => setHoverVideos(false)}
          style={{
            cursor: 'pointer',
            borderRadius: 8,
            padding: '20px',
            background: hoverVideos ? 'rgba(212,175,106,0.08)' : '#161412',
            border: hoverVideos ? '1px solid #d4af6a' : '1px solid rgba(212,175,106,0.15)',
            transition: 'all 0.2s ease',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            minHeight: 160
          }}
        >
          <div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 6 }}>
              <span style={{ padding: '2px 8px', borderRadius: 4, background: 'rgba(212,175,106,0.12)', border: '1px solid rgba(212,175,106,0.25)', color: '#d4af6a', fontSize: 10, fontWeight: 700, letterSpacing: 1 }}>
                8 VIDEOS MP4 ÚNICOS
              </span>
              <span style={{ color: '#d4af6a', fontSize: 16 }}>🎬</span>
            </div>
            <h2 style={{ fontSize: 18, fontWeight: 700, color: '#f0ede8', margin: '0 0 4px 0' }}>
              Estudio de Video & Cursos de Automatización
            </h2>
            <p style={{ fontSize: 11, color: '#a09d99', lineHeight: 1.4, margin: 0 }}>
              Parrilla de 6 columnas con videos de 7 Hacks de Claude, voz FM 48kHz y subtítulos bilingües.
            </p>
          </div>

          <div style={{
            marginTop: 12,
            padding: '8px 14px',
            borderRadius: 6,
            background: hoverVideos ? 'rgba(212,175,106,0.2)' : 'rgba(212,175,106,0.1)',
            border: '1px solid rgba(212,175,106,0.25)',
            color: '#d4af6a',
            fontWeight: 700,
            fontSize: 11,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}>
            <span>DESPLEGAR ESTUDIO DE VIDEOS Y CURSOS</span>
            <span style={{ fontSize: 12 }}>➔</span>
          </div>
        </div>

      </div>

      {/* ─── SECCIÓN 2: LA AUTONOMÍA — TARJETAS CON PALETA SIDEBAR UNIFICADA ─── */}
      <div style={{ marginBottom: 10 }}>
        <h3 style={{ fontSize: 11, fontWeight: 700, color: '#d4af6a', margin: '0 0 10px 0', textTransform: 'uppercase', letterSpacing: '1.5px' }}>
          ⚡ LA AUTONOMÍA — CONTROL OPERATIVO POR DIVISIONES
        </h3>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12, marginBottom: 24 }}>
        
        {/* TARJETA 1: AGENTES AUTÓNOMOS */}
        <div
          onClick={() => handleNav('chat')}
          onMouseEnter={() => setHoverCard('chat')}
          onMouseLeave={() => setHoverCard(null)}
          style={{
            cursor: 'pointer',
            borderRadius: 8,
            padding: '14px 16px',
            background: hoverCard === 'chat' ? 'rgba(212,175,106,0.06)' : '#161412',
            border: hoverCard === 'chat' ? '1px solid #d4af6a' : '1px solid rgba(212,175,106,0.12)',
            transition: 'all 0.15s ease'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
            <span style={{ color: '#d4af6a', fontSize: 12, fontWeight: 700 }}>🤖 Agentes Autónomos & RAG</span>
            <span style={{ fontSize: 10, background: 'rgba(212,175,106,0.12)', border: '1px solid rgba(212,175,106,0.2)', color: '#d4af6a', padding: '1px 6px', borderRadius: 4 }}>3 Activos</span>
          </div>
          <p style={{ fontSize: 10, color: '#a09d99', margin: '0 0 8px 0' }}>
            Memoria vectorial RAG 768-dim en Firestore y 7 Hacks de Claude 4.6.
          </p>
          <div style={{ color: '#d4af6a', fontSize: 10, fontWeight: 700 }}>GESTIONAR AGENTES ➔</div>
        </div>

        {/* TARJETA 2: AUDITORÍA & SEGURIDAD */}
        <div
          onClick={() => handleNav('auditoria')}
          onMouseEnter={() => setHoverCard('auditoria')}
          onMouseLeave={() => setHoverCard(null)}
          style={{
            cursor: 'pointer',
            borderRadius: 8,
            padding: '14px 16px',
            background: hoverCard === 'auditoria' ? 'rgba(212,175,106,0.06)' : '#161412',
            border: hoverCard === 'auditoria' ? '1px solid #d4af6a' : '1px solid rgba(212,175,106,0.12)',
            transition: 'all 0.15s ease'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
            <span style={{ color: '#d4af6a', fontSize: 12, fontWeight: 700 }}>🔍 Auditoría & Trazabilidad</span>
            <span style={{ fontSize: 10, background: 'rgba(212,175,106,0.12)', border: '1px solid rgba(212,175,106,0.2)', color: '#d4af6a', padding: '1px 6px', borderRadius: 4 }}>100% Ok</span>
          </div>
          <p style={{ fontSize: 10, color: '#a09d99', margin: '0 0 8px 0' }}>
            Registro de logs en tiempo real y protocolo de blindaje AGENTS.md.
          </p>
          <div style={{ color: '#d4af6a', fontSize: 10, fontWeight: 700 }}>VER AUDITORÍA ➔</div>
        </div>

        {/* TARJETA 3: TAREAS EN EJECUCIÓN & MONITOR DAG */}
        <div
          onClick={() => handleNav('pipeline')}
          onMouseEnter={() => setHoverCard('pipe')}
          onMouseLeave={() => setHoverCard(null)}
          style={{
            cursor: 'pointer',
            borderRadius: 8,
            padding: '14px 16px',
            background: hoverCard === 'pipe' ? 'rgba(212,175,106,0.06)' : '#161412',
            border: hoverCard === 'pipe' ? '1px solid #d4af6a' : '1px solid rgba(212,175,106,0.12)',
            transition: 'all 0.15s ease'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
            <span style={{ color: '#d4af6a', fontSize: 12, fontWeight: 700 }}>⚡ Tareas & Pipeline DAG</span>
            <span style={{ fontSize: 10, background: 'rgba(212,175,106,0.12)', border: '1px solid rgba(212,175,106,0.2)', color: '#d4af6a', padding: '1px 6px', borderRadius: 4 }}>Drive 5TB</span>
          </div>
          <p style={{ fontSize: 10, color: '#a09d99', margin: '0 0 8px 0' }}>
            Estado de tareas en segundo plano, respaldos Rclone y despliegue continuo.
          </p>
          <div style={{ color: '#d4af6a', fontSize: 10, fontWeight: 700 }}>MONITOR PIPELINE ➔</div>
        </div>

        {/* TARJETA 4: VENTAS & CATALOGO 18K */}
        <div
          onClick={() => handleNav('ventas')}
          onMouseEnter={() => setHoverCard('ventas')}
          onMouseLeave={() => setHoverCard(null)}
          style={{
            cursor: 'pointer',
            borderRadius: 8,
            padding: '14px 16px',
            background: hoverCard === 'ventas' ? 'rgba(212,175,106,0.06)' : '#161412',
            border: hoverCard === 'ventas' ? '1px solid #d4af6a' : '1px solid rgba(212,175,106,0.12)',
            transition: 'all 0.15s ease'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
            <span style={{ color: '#d4af6a', fontSize: 12, fontWeight: 700 }}>💎 Ventas & Catálogo 18k</span>
            <span style={{ fontSize: 10, background: 'rgba(212,175,106,0.12)', border: '1px solid rgba(212,175,106,0.2)', color: '#d4af6a', padding: '1px 6px', borderRadius: 4 }}>Activo</span>
          </div>
          <p style={{ fontSize: 10, color: '#a09d99', margin: '0 0 8px 0' }}>
            Joyería Fina HB Jewelry con checkout automático y cierre a WhatsApp $0.
          </p>
          <div style={{ color: '#d4af6a', fontSize: 10, fontWeight: 700 }}>IR A VENTAS ➔</div>
        </div>

        {/* TARJETA 5: WHATSAPP BUSINESS ($0) */}
        <div
          onClick={() => handleNav('integraciones')}
          onMouseEnter={() => setHoverCard('wa')}
          onMouseLeave={() => setHoverCard(null)}
          style={{
            cursor: 'pointer',
            borderRadius: 8,
            padding: '14px 16px',
            background: hoverCard === 'wa' ? 'rgba(212,175,106,0.06)' : '#161412',
            border: hoverCard === 'wa' ? '1px solid #d4af6a' : '1px solid rgba(212,175,106,0.12)',
            transition: 'all 0.15s ease'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
            <span style={{ color: '#d4af6a', fontSize: 12, fontWeight: 700 }}>📲 WhatsApp Business ($0)</span>
            <span style={{ fontSize: 10, background: 'rgba(212,175,106,0.12)', border: '1px solid rgba(212,175,106,0.2)', color: '#d4af6a', padding: '1px 6px', borderRadius: 4 }}>Puerto 3001</span>
          </div>
          <p style={{ fontSize: 10, color: '#a09d99', margin: '0 0 8px 0' }}>
            Canal de comunicación 24/7 sin costo por mensaje ni intermediarios.
          </p>
          <div style={{ color: '#d4af6a', fontSize: 10, fontWeight: 700 }}>CANAL WHATSAPP ➔</div>
        </div>

        {/* TARJETA 6: INVENTARIO & PRODUCTOS */}
        <div
          onClick={() => handleNav('inventario')}
          onMouseEnter={() => setHoverCard('inv')}
          onMouseLeave={() => setHoverCard(null)}
          style={{
            cursor: 'pointer',
            borderRadius: 8,
            padding: '14px 16px',
            background: hoverCard === 'inv' ? 'rgba(212,175,106,0.06)' : '#161412',
            border: hoverCard === 'inv' ? '1px solid #d4af6a' : '1px solid rgba(212,175,106,0.12)',
            transition: 'all 0.15s ease'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
            <span style={{ color: '#d4af6a', fontSize: 12, fontWeight: 700 }}>📦 Control de Inventario</span>
            <span style={{ fontSize: 10, background: 'rgba(212,175,106,0.12)', border: '1px solid rgba(212,175,106,0.2)', color: '#d4af6a', padding: '1px 6px', borderRadius: 4 }}>Stock Ok</span>
          </div>
          <p style={{ fontSize: 10, color: '#a09d99', margin: '0 0 8px 0' }}>
            Gestión de stock de piezas finas en oro 18k e indicadores de inventario.
          </p>
          <div style={{ color: '#d4af6a', fontSize: 10, fontWeight: 700 }}>VER INVENTARIO ➔</div>
        </div>

      </div>

      {/* ─── SECCIÓN 3: ACCIONES RECIENTES 100% UNIFICADAS CON SIDEBAR ─── */}
      <div style={{ background: '#161412', border: '1px solid rgba(212,175,106,0.15)', borderRadius: 8, padding: '16px 18px' }}>
        
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
          <div>
            <h3 style={{ fontSize: 11, fontWeight: 700, color: '#d4af6a', margin: '0 0 2px 0', textTransform: 'uppercase', letterSpacing: '1.5px' }}>
              🚀 ACCIONES RECIENTES & DEPLOYS DIRECTOS
            </h3>
            <p style={{ fontSize: 11, color: '#6b6866', margin: 0 }}>Acciones rápidas para CEO, Gerencia, Supervisores y Operaciones</p>
          </div>

          <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
            <button onClick={() => handleNav('productos')} style={{ background: 'rgba(212,175,106,0.1)', border: '1px solid rgba(212,175,106,0.25)', color: '#d4af6a', padding: '5px 12px', borderRadius: 6, fontSize: 11, fontWeight: 700, cursor: 'pointer' }}>➕ AGREGAR PRODUCTO</button>
            <button onClick={() => handleNav('ordenes')} style={{ background: 'rgba(212,175,106,0.1)', border: '1px solid rgba(212,175,106,0.25)', color: '#d4af6a', padding: '5px 12px', borderRadius: 6, fontSize: 11, fontWeight: 700, cursor: 'pointer' }}>📦 VER PEDIDOS</button>
            <button onClick={() => handleNav('reportes')} style={{ background: 'rgba(212,175,106,0.1)', border: '1px solid rgba(212,175,106,0.25)', color: '#d4af6a', padding: '5px 12px', borderRadius: 6, fontSize: 11, fontWeight: 700, cursor: 'pointer' }}>📊 REPORTES FINANCIEROS</button>
            <button onClick={() => handleNav('pipeline')} style={{ background: 'rgba(212,175,106,0.1)', border: '1px solid rgba(212,175,106,0.25)', color: '#d4af6a', padding: '5px 12px', borderRadius: 6, fontSize: 11, fontWeight: 700, cursor: 'pointer' }}>⚡ EJECUTAR PIPELINE DAG</button>
          </div>
        </div>

        {/* TABLA DE ACTIVIDAD RECIENTE UNIFICADA */}
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 11 }}>
          <thead>
            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.06)', color: '#6b6866', textAlign: 'left', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              <th style={{ padding: '8px', width: '150px' }}>Timestamp</th>
              <th style={{ padding: '8px' }}>Evento Corporativo</th>
              <th style={{ padding: '8px', width: '140px' }}>División</th>
              <th style={{ padding: '8px', width: '100px' }}>Estado</th>
            </tr>
          </thead>
          <tbody>
            {RECENT_ACTIVITIES.map((act, idx) => (
              <tr key={idx} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)', color: '#c0bcb8' }}>
                <td style={{ padding: '8px', color: '#d4af6a', fontWeight: 600 }}>{act.timestamp}</td>
                <td style={{ padding: '8px', color: '#f0ede8' }}>{act.evento}</td>
                <td style={{ padding: '8px', color: '#a09d99' }}>{act.division}</td>
                <td style={{ padding: '8px' }}>
                  <span style={{ padding: '2px 8px', borderRadius: 4, background: 'rgba(212,175,106,0.12)', color: '#d4af6a', border: '1px solid rgba(212,175,106,0.25)', fontSize: 10, fontWeight: 600 }}>
                    {act.estado}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

      </div>

    </div>
  );
}
