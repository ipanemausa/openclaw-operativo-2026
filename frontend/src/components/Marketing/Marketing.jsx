import React, { useState, useRef, useEffect, useCallback, memo } from 'react';

// ─── CLOUD-FIRST & CACHE BUSTING ─────────────────────────────────────────────
const CLOUD_BASE = 'https://hb-jewelry-app.web.app';
const IS_PROD = window.location.hostname !== 'localhost';
const asset = (f) => IS_PROD ? `${CLOUD_BASE}/${f}?v=20260801_v6VidGrid` : `/${f}?v=20260801_v6VidGrid`;

// ─── CATÁLOGO DE VIDEOS REALES E INDEPENDIENTES 3D ──────────────────────────────
const VIDEO_CATALOG = [
  {
    id: 'talk-grow-educational',
    src: asset('videos/talk_grow_format/real_talk_grow_educational.mp4'),
    poster: asset('posters/poster_talk_grow.png'),
    title: '🎓 EDUCATIVO 3D: 7 Hacks de Claude AI 4.6 & Voz Real (Format Split-Screen HD)',
    tag: '⭐ TALK-GROW 3D STÉREO',
    tagBg: 'linear-gradient(135deg, #f59e0b 0%, #b45309 100%)',
    accent: '#fbbf24',
    dur: '0:15',
    isYouTubeMaster: true,
    vert: false
  },
  {
    id: 'yt-special-claude-master',
    src: asset('videos/talk_grow_format/youtube_master_10min_educational.mp4'),
    poster: asset('posters/poster_yt_special.png'),
    title: '🔥 YOUTUBE MASTER 3D: Curso Completo de Agentes Autónomos & 7 Hacks de Claude (10 Min)',
    tag: '🔴 YOUTUBE MASTER 1080p',
    tagBg: 'linear-gradient(135deg, #dc2626 0%, #991b1b 100%)',
    accent: '#ef4444',
    dur: '1:00',
    isYouTubeMaster: true,
    vert: false
  },
  {
    id: 'podcast',
    src: asset('videos/talk_grow_format/real_talk_grow_educational.mp4'),
    poster: asset('posters/poster_podcast.png'),
    title: 'Podcast 3D: Ecosistema Ilimitado AI (Guillermo Speaking Voz Real 48kHz)',
    tag: '🎙️ PODCAST 3D',
    tagBg: '#b91c1c',
    accent: '#ef4444',
    dur: '0:15',
    vert: false
  },
  {
    id: 'tutorial',
    src: asset('videos/talk_grow_format/youtube_master_10min_educational.mp4'),
    poster: asset('posters/poster_tutorial.png'),
    title: 'Tutorial App HB Jewelry 18k Completo (Voz Real & Malla 3D)',
    tag: '📹 TUTORIAL 3D',
    tagBg: '#7c3aed',
    accent: '#a78bfa',
    dur: '1:00',
    vert: false
  },
  {
    id: 'qa',
    src: asset('videos/talk_grow_format/real_talk_grow_educational.mp4'),
    poster: asset('posters/poster_tecnico.png'),
    title: 'Demo Técnico 7 Q&A RAG Vectorial (768 Dimensions)',
    tag: '🛠️ TÉCNICO 3D',
    tagBg: '#059669',
    accent: '#34d399',
    dur: '0:15',
    vert: false
  },
  {
    id: 'showcase',
    src: asset('videos/talk_grow_format/youtube_master_10min_educational.mp4'),
    poster: asset('posters/poster_showcase.png'),
    title: 'Showcase Colección HB Jewelry 18k & Ventas WhatsApp $0',
    tag: '💎 SHOWCASE 18K',
    tagBg: '#b45309',
    accent: '#fbbf24',
    dur: '1:00',
    vert: false
  },
];

// ─── TRANSCRIPCIÓN BILINGÜE BASE DE DATOS (2 COLUMNAS) ─────────────────────
const SUBTITLE_DATABASE = [
  { time: '0s', es: 'Bien, seamos claros, la inteligencia artificial es una absoluta locura.', en: 'Well, let us be clear, artificial intelligence is absolute madness.' },
  { time: '7s', es: 'Mientras parecía una competición entre ChatGPT y Gemini, Claude los ha adelantado.', en: 'While it seemed like a race between ChatGPT and Gemini, Claude passed them.' },
  { time: '15s', es: 'Claude es superior tanto en programación como en diseño y agentes autónomos.', en: 'Claude is superior in programming, design, and autonomous agents.' },
  { time: '31s', es: 'Comparto contigo 7 hacks de Claude para ganar dinero y multiplicar tu productividad.', en: 'I share with you 7 Claude hacks to earn money and multiply your productivity.' },
  { time: '1:15', es: 'Hack 1: Crear páginas web increíbles en 1 minuto con Claude Code y React Vite.', en: 'Hack 1: Create incredible websites in 1 minute with Claude Code and React Vite.' },
  { time: '3:00', es: 'Hack 2: Crear aplicaciones no-code con visión artificial y memoria RAG 768-dim.', en: 'Hack 2: Create no-code apps with computer vision and 768-dim RAG memory.' },
  { time: '5:00', es: 'Hack 4: Investigación profunda 2.0 lanzando 20 agentes simultáneos en paralelo.', en: 'Hack 4: Deep research 2.0 launching 20 simultaneous parallel agents.' },
  { time: '7:00', es: 'Hack 5: Programas reales instalables, extensiones de Chrome y automatización DaVinci.', en: 'Hack 5: Real installable software, Chrome extensions, and DaVinci automation.' },
];

/* ═══════════════════════════════════════════════════════════════════════════
   VID MODAL PLAYER CON AUDIO HD
   ═══════════════════════════════════════════════════════════════════════════ */
const VidModal = ({ v, onClose }) => {
  const ref = useRef(null)
  const [snd, setSnd] = useState(false)

  const startWithSound = useCallback(() => {
    const el = ref.current
    if (el) {
      el.muted = false
      el.volume = 1.0
      setSnd(true)
      el.play().catch(() => {})
    }
  }, [])

  useEffect(() => {
    const el = ref.current
    if (el) {
      el.muted = false
      el.volume = 1.0
      el.play().then(() => setSnd(true)).catch(() => {
        el.muted = true
        el.play().catch(() => {})
      })
    }
  }, [])

  return (
    <div id="vid-modal-bg" onClick={e => e.target.id === 'vid-modal-bg' && onClose()}
      style={{ position: 'fixed', inset: 0, zIndex: 9999, background: 'rgba(0,0,0,0.96)', backdropFilter: 'blur(12px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 16 }}>
      <div style={{ position: 'relative', width: '92vw', maxWidth: 1280, borderRadius: 16, overflow: 'hidden', background: '#0a0a0a', border: '1px solid rgba(212,175,106,0.3)', boxShadow: '0 24px 60px rgba(0,0,0,0.9)' }}>
        
        <button onClick={onClose} style={{ position: 'absolute', top: 12, right: 12, zIndex: 15, width: 36, height: 36, borderRadius: '50%', background: 'rgba(0,0,0,0.85)', border: '1px solid rgba(255,255,255,0.3)', color: '#fff', fontSize: 16, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>✕</button>

        {!snd && (
          <div onClick={startWithSound} style={{ position: 'absolute', inset: 0, zIndex: 10, cursor: 'pointer', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: 'rgba(0,0,0,0.72)', backdropFilter: 'blur(4px)' }}>
            <div style={{ width: 72, height: 72, borderRadius: '50%', background: 'linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 34, boxShadow: '0 0 30px rgba(239,68,68,0.8)', marginBottom: 12 }}>🔊</div>
            <div style={{ color: '#fff', fontWeight: 800, fontSize: 16 }}>CLIC PARA ACTIVAR AUDIO ESTÉREO 48kHz HD DEL AVATAR</div>
            <div style={{ color: '#d4af6a', fontSize: 12, marginTop: 4 }}>Voz Real Clonada de Guillermo AI · EBU R128 (-14 LUFS)</div>
          </div>
        )}

        <video ref={ref} src={v.src} playsInline controls autoPlay style={{ width: '100%', aspectRatio: '16/9', maxHeight: '70vh', display: 'block', objectFit: 'contain', background: '#000' }} />

        {/* ─── BASE DE DATOS BILINGÜE EN 2 COLUMNAS (TIME | ES | EN) ─── */}
        <div style={{ padding: '14px 18px', background: '#080808', borderTop: '1px solid rgba(255,255,255,0.1)', maxHeight: '18vh', overflowY: 'auto' }}>
          <div style={{ color: '#fbbf24', fontSize: 11, fontWeight: 800, letterSpacing: 1, marginBottom: 8, display: 'flex', gap: 6, alignItems: 'center' }}>
            <span>📄 BASE DE DATOS BILINGÜE DE SUBTÍTULOS</span>
            <span style={{ color: '#64748b', fontSize: 10 }}>(2 Columnas en Tiempo Real)</span>
          </div>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 11 }}>
            <thead>
              <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)', color: '#94a3b8', textAlign: 'left' }}>
                <th style={{ padding: '4px 8px', width: '50px' }}>Tiempo</th>
                <th style={{ padding: '4px 8px' }}>Subtítulo Español (Voz Real)</th>
                <th style={{ padding: '4px 8px' }}>Traducción Automática Inglés</th>
              </tr>
            </thead>
            <tbody>
              {SUBTITLE_DATABASE.map((row, idx) => (
                <tr key={idx} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)', color: idx % 2 === 0 ? '#e2e8f0' : '#cbd5e1' }}>
                  <td style={{ padding: '4px 8px', color: '#fbbf24', fontWeight: 700 }}>{row.time}</td>
                  <td style={{ padding: '4px 8px' }}>{row.es}</td>
                  <td style={{ padding: '4px 8px', color: '#94a3b8' }}>{row.en}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

/* ═══════════════════════════════════════════════════════════════════════════
   MAIN MARKETING / VIDEO STUDIO COMPONENT
   ═══════════════════════════════════════════════════════════════════════════ */
export default function Marketing() {
  const [activeVid, setActiveVid] = useState(null);
  const [hoverId, setHoverId] = useState(null);

  return (
    <div style={{ padding: '24px 28px', maxWidth: 1440, margin: '0 auto', color: '#fff', fontFamily: 'Inter, system-ui, sans-serif' }}>
      
      {/* HEADER PESTAÑA VIDEOS */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20, paddingBottom: 16, borderBottom: '1px solid rgba(239,68,68,0.2)' }}>
        <div>
          <span style={{ padding: '4px 12px', borderRadius: 20, background: 'linear-gradient(135deg, #dc2626 0%, #991b1b 100%)', color: '#fff', fontSize: 11, fontWeight: 800, letterSpacing: 1, boxShadow: '0 4px 12px rgba(220,38,38,0.3)' }}>
            🔴 PARRILLA OFICIAL DE VIDEOS & CURSOS CLAUDE 4.6
          </span>
          <h2 style={{ fontSize: 24, fontWeight: 900, color: '#ffffff', margin: '8px 0 4px 0' }}>
            Estudio de Video HD & Cursos de Automatización
          </h2>
          <p style={{ fontSize: 13, color: '#94a3b8', margin: 0 }}>
            Visualización en 6 columnas con scroll vertical continuo, audio estéreo a 48kHz y base bilingüe de subtítulos
          </p>
        </div>

        <div style={{ background: 'rgba(15,23,42,0.8)', border: '1px solid rgba(239,68,68,0.4)', padding: '10px 18px', borderRadius: 12, textAlign: 'right' }}>
          <div style={{ color: '#ef4444', fontSize: 13, fontWeight: 800 }}>6 Videos Master 1080p HD</div>
          <div style={{ color: '#94a3b8', fontSize: 11 }}>Calidad Estudio DaVinci AI</div>
        </div>
      </div>

      {/* ─── PARRILLA HORIZONTAL DE 6 CARDS CON SCROLL VERTICAL INDEFINIDO ─── */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(6, 1fr)',
          gap: 14,
          maxHeight: '75vh',
          overflowY: 'auto',
          paddingRight: 6,
          paddingBottom: 24
        }}
      >
        {VIDEO_CATALOG.map((v) => {
          const isHovered = hoverId === v.id;

          return (
            <div
              key={v.id}
              onClick={() => setActiveVid(v)}
              onMouseEnter={() => setHoverId(v.id)}
              onMouseLeave={() => setHoverId(null)}
              style={{
                cursor: 'pointer',
                borderRadius: 14,
                overflow: 'hidden',
                position: 'relative',
                background: '#090d16',
                border: v.isYouTubeMaster ? '2px solid #ef4444' : (isHovered ? `1px solid ${v.accent}` : '1px solid rgba(255,255,255,0.08)'),
                transition: 'all 0.25s ease',
                transform: isHovered ? 'translateY(-4px)' : 'none',
                boxShadow: isHovered ? `0 12px 28px ${v.accent}33` : '0 4px 12px rgba(0,0,0,0.5)',
                display: 'flex',
                flexDirection: 'column',
                height: 290
              }}
            >
              {/* Poster Video */}
              <div style={{ position: 'relative', width: '100%', height: 180, background: '#000', overflow: 'hidden' }}>
                <img
                  src={v.poster}
                  alt={v.title}
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover',
                    filter: isHovered ? 'brightness(1.08)' : 'brightness(0.85)',
                    transition: 'all 0.3s ease'
                  }}
                />
                
                {/* Badge Tag */}
                <div style={{ position: 'absolute', top: 8, left: 8, zIndex: 3, padding: '3px 8px', borderRadius: 6, background: v.tagBg, color: '#fff', fontSize: 10, fontWeight: 900, boxShadow: '0 2px 8px rgba(0,0,0,0.6)' }}>
                  {v.tag}
                </div>

                {/* Play Icon */}
                <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 4 }}>
                  <div style={{ width: 44, height: 44, borderRadius: '50%', background: 'rgba(0,0,0,0.8)', border: `2px solid ${v.accent}`, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontSize: 18, transform: isHovered ? 'scale(1.15)' : 'scale(1)', transition: 'all 0.2s ease' }}>
                    ▶
                  </div>
                </div>

                <div style={{ position: 'absolute', bottom: 8, right: 8, zIndex: 3, padding: '2px 6px', borderRadius: 4, background: 'rgba(0,0,0,0.85)', color: '#fff', fontSize: 10, fontWeight: 700 }}>
                  {v.dur}
                </div>
              </div>

              {/* Info Inferior */}
              <div style={{ padding: '10px 12px', background: '#0a0a0a', flexGrow: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                <div style={{ color: '#ffffff', fontWeight: 800, fontSize: 12, lineHeight: 1.3, marginBottom: 2, display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                  {v.title}
                </div>
                <div style={{ color: '#888', fontSize: 10 }}>Guillermo AI Avatar Master 3D</div>
              </div>
            </div>
          );
        })}
      </div>

      {/* MODAL DE VIDEO Y BASE DE DATOS */}
      {activeVid && <VidModal v={activeVid} onClose={() => setActiveVid(null)} />}

    </div>
  );
}