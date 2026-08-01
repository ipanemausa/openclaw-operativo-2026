import React, { useState, useRef, useEffect, useCallback } from 'react';

// ─── CLOUD-FIRST & DYNAMIC CACHE BUSTING ─────────────────────────────────────────────
const CLOUD_BASE = 'https://hb-jewelry-app.web.app';
const IS_PROD = window.location.hostname !== 'localhost';
const asset = (f) => IS_PROD ? `${CLOUD_BASE}/${f}?v=20260801_vPristineGuillermo` : `/${f}?v=20260801_vPristineGuillermo`;

// ─── CATÁLOGO DE VIDEOS REALES (POSTERS 100% LIMPIOS DE GUILLERMO SIN TEXTO BASTARDO) ───
const VIDEO_CATALOG = [
  {
    id: 'talk-grow-educational',
    src: asset('videos/talk_grow_format/real_talk_grow_educational.mp4'),
    poster: asset('avatars/studio_mic.png'),
    title: 'Educativo 3D: 7 Hacks de Claude AI 4.6',
    tag: 'TALK-GROW 3D',
    dur: '0:15',
    description: 'Demostración de 7 hacks con teleprompter paso a paso y voz FM 48kHz.'
  },
  {
    id: 'yt-special-claude-master',
    src: asset('videos/talk_grow_format/youtube_master_10min_educational.mp4'),
    poster: asset('avatars/desk_mic.png'),
    title: 'YouTube Master: Agentes AI & 7 Hacks (10 Min)',
    tag: 'MASTER 1080p',
    dur: '1:00',
    description: 'Curso intensivo de agentes autónomos y vectorización RAG en Firestore.'
  },
  {
    id: 'podcast',
    src: asset('hb_tutorial_avatar_v1.mp4'),
    poster: asset('posters/poster_podcast.png'),
    title: 'Podcast: Ecosistema Ilimitado AI',
    tag: 'PODCAST',
    dur: '1:35',
    description: 'Guillermo AI en estudio explicando la automatización comercial.'
  },
  {
    id: 'tutorial',
    src: asset('hb_tutorial_narrado_v1.mp4'),
    poster: asset('avatars/studio_mic.png'),
    title: 'Tutorial: Manejo Completo de App HB 18k',
    tag: 'TUTORIAL APP',
    dur: '1:16',
    description: 'Guía paso a paso: módulo de ventas, WhatsApp $0 e inventario.'
  },
  {
    id: 'qa-english',
    src: asset('output_avatar_english_7qa.mp4'),
    poster: asset('avatars/desk_mic.png'),
    title: 'Técnico: Demo Arquitectura 7 Q&A RAG (English)',
    tag: 'TECHNICAL DEMO',
    dur: '0:15',
    description: 'Demostración técnica en inglés con arquitectura RAG 768-dim.'
  },
  {
    id: 'showcase-18k',
    src: asset('final_showcase.mp4'),
    poster: asset('avatar_pro.png'),
    title: 'Showcase: Colección Joyería 18k & WhatsApp $0',
    tag: 'SHOWCASE 18K',
    dur: '0:45',
    description: 'Presentación comercial de joyería fina con cierre automático.'
  },
  {
    id: 'tiktok-viral',
    src: asset('tiktok_showcase.mp4'),
    poster: asset('avatar_pro.png'),
    title: 'TikTok Viral: Promocional Vertical 1080p',
    tag: 'TIKTOK 9:16',
    dur: '0:30',
    description: 'Video vertical promocional optimizado para redes sociales.'
  },
  {
    id: 'showcase-human-loop',
    src: asset('showcase_human_loop.mp4'),
    poster: asset('avatar_pro.png'),
    title: 'Avatar Base: Guillermo AI Studio Loop',
    tag: 'AVATAR LOOP',
    dur: '0:20',
    description: 'Video base en estudio con loop continuo para gesticulación vocal.'
  }
];

// ─── TRANSCRIPCIÓN BILINGÜE BASE DE DATOS (2 COLUMNAS) ─────────────────────
const SUBTITLE_DATABASE = [
  { time: '00:01', es: 'Hola, soy Guillermo de HB Jewelry. Bienvenidos a nuestra colección.', en: 'Hello, I am Guillermo from HB Jewelry. Welcome to our collection.' },
  { time: '00:05', es: 'Hoy les mostraré los 7 hacks avanzados para dominar Claude 4.6 en su empresa.', en: 'Today I will show you the 7 advanced hacks to master Claude 4.6 in your business.' },
  { time: '00:09', es: 'Cada pedido se procesa automáticamente a través de WhatsApp Business sin costo.', en: 'Every order is automatically processed through WhatsApp Business at zero cost.' },
  { time: '00:12', es: 'Toda nuestra información está respaldada en tiempo real en Google Drive 5TB.', en: 'All our information is backed up in real time on Google Drive 5TB.' }
];

/* ═══════════════════════════════════════════════════════════════════════════
   MODAL PARA REPRODUCIR CADA VIDEO CON AUDIO UNMUTED & SUBTÍTULOS BILINGÜES
   ═══════════════════════════════════════════════════════════════════════════ */
function VidModal({ v, onClose }) {
  const ref = useRef(null);
  const [unmuted, setUnmuted] = useState(false);

  const enableAudio = useCallback(() => {
    if (ref.current) {
      ref.current.muted = false;
      ref.current.volume = 1.0;
      ref.current.play().catch(() => {});
      setUnmuted(true);
    }
  }, []);

  useEffect(() => {
    enableAudio();
  }, [enableAudio]);

  return (
    <div style={{ position: 'fixed', inset: 0, zIndex: 9999, background: 'rgba(5,5,5,0.95)', backdropFilter: 'blur(16px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 20 }}>
      <div style={{ position: 'relative', width: '100%', maxWidth: 1000, background: '#161412', border: '1px solid rgba(212,175,106,0.25)', borderRadius: 12, overflow: 'hidden', boxShadow: '0 20px 60px rgba(0,0,0,0.9)' }}>
        
        {/* CABECERA DEL MODAL */}
        <div style={{ padding: '12px 18px', background: '#0f0f0f', borderBottom: '1px solid rgba(212,175,106,0.15)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <span style={{ padding: '2px 8px', borderRadius: 4, background: 'rgba(212,175,106,0.12)', border: '1px solid rgba(212,175,106,0.25)', color: '#d4af6a', fontSize: 10, fontWeight: 700 }}>{v.tag}</span>
            <strong style={{ color: '#d4af6a', fontSize: 15 }}>{v.title}</strong>
          </div>
          <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: '#a09d99', fontSize: 20, cursor: 'pointer', padding: '0 8px' }}>✕</button>
        </div>

        {/* OVERLAY BOTÓN DESBLOQUEO AUDIO SI NAVEGADOR BLOQUEA AUTO-PLAY */}
        {!unmuted && (
          <div onClick={enableAudio} style={{ position: 'absolute', inset: 0, zIndex: 10, background: 'rgba(0,0,0,0.85)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', cursor: 'pointer' }}>
            <div style={{ width: 64, height: 64, borderRadius: '50%', background: 'rgba(212,175,106,0.2)', border: '2px solid #d4af6a', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 28, color: '#d4af6a', marginBottom: 12 }}>🔊</div>
            <div style={{ color: '#f0ede8', fontWeight: 800, fontSize: 15 }}>CLIC PARA ACTIVAR AUDIO ESTÉREO 48kHz HD</div>
            <div style={{ color: '#d4af6a', fontSize: 12, marginTop: 4 }}>Voz Real Clonada de Guillermo AI · EBU R128 (-14 LUFS)</div>
          </div>
        )}

        <video ref={ref} key={v.src} src={v.src} playsInline controls autoPlay style={{ width: '100%', aspectRatio: '16/9', maxHeight: '62vh', display: 'block', objectFit: 'contain', background: '#000' }} />

        {/* SUBTÍTULOS BILINGÜES EN 2 COLUMNAS */}
        <div style={{ padding: '14px 18px', background: '#161412', borderTop: '1px solid rgba(212,175,106,0.15)', maxHeight: '22vh', overflowY: 'auto' }}>
          <div style={{ color: '#d4af6a', fontSize: 11, fontWeight: 700, letterSpacing: 1, marginBottom: 8, display: 'flex', gap: 6, alignItems: 'center' }}>
            <span>📄 BASE DE DATOS BILINGÜE DE SUBTÍTULOS DE ESTE VIDEO</span>
            <span style={{ color: '#6b6866', fontSize: 10 }}>(2 Columnas en Tiempo Real)</span>
          </div>
          
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 11 }}>
            <thead>
              <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.06)', color: '#6b6866', textAlign: 'left' }}>
                <th style={{ padding: '4px 8px', width: '50px' }}>Tiempo</th>
                <th style={{ padding: '4px 8px' }}>Subtítulo Español (Voz Real)</th>
                <th style={{ padding: '4px 8px' }}>Traducción Automática Inglés</th>
              </tr>
            </thead>
            <tbody>
              {SUBTITLE_DATABASE.map((row, idx) => (
                <tr key={idx} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)', color: '#c0bcb8' }}>
                  <td style={{ padding: '4px 8px', color: '#d4af6a', fontWeight: 700 }}>{row.time}</td>
                  <td style={{ padding: '4px 8px' }}>{row.es}</td>
                  <td style={{ padding: '4px 8px', color: '#a09d99' }}>{row.en}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════════════════════
   MAIN MARKETING / VIDEO STUDIO COMPONENT (THUMBNAILS 100% LIMPIAS SIN TEXTO SOBRE LA FOTO)
   ═══════════════════════════════════════════════════════════════════════════ */
export default function Marketing() {
  const [activeVid, setActiveVid] = useState(null);
  const [hoverId, setHoverId] = useState(null);

  return (
    <div style={{ padding: '20px 24px', maxWidth: 1400, margin: '0 auto', color: '#f0ede8', fontFamily: 'Inter, system-ui, sans-serif' }}>
      
      {/* HEADER PESTAÑA VIDEOS UNIFICADO PALETA HB GOLD (#d4af6a) */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 18, paddingBottom: 14, borderBottom: '1px solid rgba(212,175,106,0.15)' }}>
        <div>
          <span style={{ padding: '3px 10px', borderRadius: 16, background: 'rgba(212,175,106,0.08)', border: '1px solid rgba(212,175,106,0.2)', color: '#d4af6a', fontSize: 10, fontWeight: 700, letterSpacing: 1 }}>
            🎬 PARRILLA OFICIAL DE VIDEOS 100% ÚNICOS & INDEPENDIENTES
          </span>
          <h2 style={{ fontSize: 22, fontWeight: 700, color: '#d4af6a', margin: '6px 0 2px 0' }}>
            Estudio de Video HD & Cursos de Automatización
          </h2>
          <p style={{ fontSize: 12, color: '#a09d99', margin: 0 }}>
            Parrilla de 6 columnas con scroll vertical. Cada tarjeta reproduce su propio archivo MP4 único.
          </p>
        </div>

        <div style={{ background: '#161412', border: '1px solid rgba(212,175,106,0.15)', padding: '8px 14px', borderRadius: 8, textAlign: 'right' }}>
          <div style={{ color: '#d4af6a', fontSize: 12, fontWeight: 700 }}>{VIDEO_CATALOG.length} Videos Únicos</div>
          <div style={{ color: '#6b6866', fontSize: 10 }}>Estudio DaVinci AI 1080p</div>
        </div>
      </div>

      {/* ─── PARRILLA DE 6 COLUMNAS CON THUMBNAILS 100% LIMPIAS (TEXTO AFUERA) ─── */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(6, 1fr)',
          gap: 14,
          maxHeight: '75vh',
          overflowY: 'auto',
          paddingRight: 4,
          paddingBottom: 20
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
                borderRadius: 8,
                overflow: 'hidden',
                position: 'relative',
                background: isHovered ? 'rgba(212,175,106,0.06)' : '#161412',
                border: isHovered ? '1px solid #d4af6a' : '1px solid rgba(212,175,106,0.12)',
                transition: 'all 0.2s ease',
                transform: isHovered ? 'translateY(-3px)' : 'none',
                boxShadow: isHovered ? '0 8px 20px rgba(212,175,106,0.15)' : '0 4px 10px rgba(0,0,0,0.5)',
                display: 'flex',
                flexDirection: 'column',
                height: 260
              }}
            >
              {/* THUMBNAIL 100% LIMPIA DE IMAGEN DE GUILLERMO (NINGÚN TEXTO SOBRE EL ROSTRO/CUERPO) */}
              <div style={{ position: 'relative', width: '100%', height: 160, background: '#000', overflow: 'hidden' }}>
                <img src={v.poster} alt={v.title} style={{ width: '100%', height: '100%', objectFit: 'cover', objectPosition: 'top center' }} />

                {/* BOTÓN PLAY SUTIL CENTRADO */}
                <div style={{ position: 'absolute', inset: 0, zIndex: 2, background: isHovered ? 'rgba(0,0,0,0.15)' : 'rgba(0,0,0,0.25)', display: 'flex', alignItems: 'center', justifyContent: 'center', transition: 'all 0.2s ease' }}>
                  <div style={{ width: 38, height: 38, borderRadius: '50%', background: 'rgba(212,175,106,0.9)', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 4px 12px rgba(0,0,0,0.6)', transform: isHovered ? 'scale(1.1)' : 'scale(1)', transition: 'all 0.2s ease' }}>
                    <span style={{ color: '#000', fontSize: 15, marginLeft: 2 }}>▶</span>
                  </div>
                </div>
              </div>

              {/* PANEL METADATA ESTRUCTURADO Y REUBICADO 100% AFUERA DEL THUMBNAIL */}
              <div style={{ padding: '10px 12px', background: '#161412', flexGrow: 1, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                    <span style={{ padding: '1px 6px', borderRadius: 4, background: 'rgba(212,175,106,0.12)', border: '1px solid rgba(212,175,106,0.2)', color: '#d4af6a', fontSize: 9, fontWeight: 700 }}>
                      {v.tag}
                    </span>
                    <span style={{ color: '#6b6866', fontSize: 9, fontWeight: 700 }}>{v.dur}</span>
                  </div>
                  <div style={{ color: '#f0ede8', fontWeight: 700, fontSize: 11, marginBottom: 2, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {v.title}
                  </div>
                  <div style={{ color: '#a09d99', fontSize: 9, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {v.description}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {activeVid && <VidModal v={activeVid} onClose={() => setActiveVid(null)} />}
    </div>
  );
}