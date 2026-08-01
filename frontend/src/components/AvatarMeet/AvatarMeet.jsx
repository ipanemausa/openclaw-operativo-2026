import React, { useState, useEffect } from 'react';

// ─── CLOUD-FIRST PROTOCOL & CACHE BUSTING ──────────────────────────────────
const CLOUD_BASE_URL = 'https://hb-jewelry-app.web.app';
const IS_PROD = window.location.hostname !== 'localhost';
const cloudAsset = (f) => IS_PROD ? `${CLOUD_BASE_URL}/${f}?v=20260801_vModelStudioFull` : `/${f}?v=20260801_vModelStudioFull`;

// ─── CATÁLOGO DE 8 AVATARES OFICIALES GUILLERMO AI (EXCLUSIVAMENTE GUILLERMO) ───
const AVATAR_CATALOG = [
  {
    id: 'master',
    name: 'Guillermo — Master Principal 3D',
    style: 'Identidad Raíz · HB Official Master',
    img: cloudAsset('avatar_pro.png'),
    accent: '#d4af6a',
    badge: '👑 MASTER',
    badgeBg: '#b45309',
    mesh: 'Malla Facial FLAME 3D (52 Blendshapes)',
    pose: 'De Pie · Presencia Corporativa'
  },
  {
    id: 'studio',
    name: 'Guillermo — Studio 3D (De Pie)',
    style: 'Cuerpo Entero · Micrófono Boom · Jeans',
    img: cloudAsset('avatars/studio_mic.png'),
    accent: '#d4af6a',
    badge: '🎙️ STUDIO',
    badgeBg: '#7c3aed',
    mesh: 'Rigging Volumétrico 3D Body',
    pose: 'De Pie con Micrófono de Estudio'
  },
  {
    id: 'desk',
    name: 'Guillermo — Escritorio 3D',
    style: 'Silla Ejecutiva · Micrófono al Frente',
    img: cloudAsset('avatars/desk_mic.png'),
    accent: '#d4af6a',
    badge: '🎧 DESK',
    badgeBg: '#1d4ed8',
    mesh: 'Postura Sentado + Malla Craneal 3D',
    pose: 'Escritorio de Radio & Podcast'
  },
  {
    id: 'casual',
    name: 'Guillermo — Casual Azul 3D',
    style: 'Confiado · Blue Jeans · Logo HB',
    img: cloudAsset('avatars/azul.png'),
    accent: '#d4af6a',
    badge: '👔 CASUAL',
    badgeBg: '#059669',
    mesh: 'PNG Transparente RGBA High-Res',
    pose: 'Brazos Cruzados · Confianza'
  },
  {
    id: 'premium',
    name: 'Guillermo — Premium Blanco 3D',
    style: 'Elegante · Blue Jeans · Logo HB',
    img: cloudAsset('avatars/blanco.png'),
    accent: '#d4af6a',
    badge: '⭐ PREMIUM',
    badgeBg: '#475569',
    mesh: 'Renderizado Físico 1080p',
    pose: 'Postura Erguida Elegante'
  },
  {
    id: 'vip',
    name: 'Guillermo — VIP Gold 3D',
    style: 'Colección HB 18k · Malla Volumétrica',
    img: cloudAsset('avatars/dorado.png'),
    accent: '#d4af6a',
    badge: '👑 VIP GOLD',
    badgeBg: '#b91c1c',
    mesh: 'Iluminación Volumétrica Dorado 18k',
    pose: 'Brazos Abiertos · Presentador'
  },
  {
    id: 'executive',
    name: 'Guillermo — Ejecutivo Negro 3D',
    style: 'Edición Limitada · Black Logo HB',
    img: cloudAsset('avatars/negro.png'),
    accent: '#d4af6a',
    badge: '🖤 BLACK',
    badgeBg: '#1e293b',
    mesh: 'Malla Facial Fisiológica HD',
    pose: 'Saco Negro Ejecutivo'
  },
  {
    id: 'passion',
    name: 'Guillermo — Pasión Rojo 3D',
    style: 'Alto Impacto · Red Logo HB',
    img: cloudAsset('avatars/rojo.png'),
    accent: '#d4af6a',
    badge: '🔥 RED',
    badgeBg: '#9f1239',
    mesh: 'Gesticulación Vocal Activa',
    pose: 'Actitud Dinámica Redes'
  }
];

export default function AvatarMeet() {
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [hoverId, setHoverId] = useState(null);
  const [isFullScreenOpen, setIsFullScreenOpen] = useState(false);

  const selectedAvatar = AVATAR_CATALOG[selectedIndex];

  const handlePrev = () => {
    setSelectedIndex((prev) => (prev === 0 ? AVATAR_CATALOG.length - 1 : prev - 1));
  };

  const handleNext = () => {
    setSelectedIndex((prev) => (prev === AVATAR_CATALOG.length - 1 ? 0 : prev + 1));
  };

  // NAVEGACIÓN POR TECLADO (FLECHAS IZQ / DER Y ESCAPE)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!isFullScreenOpen) return;
      if (e.key === 'ArrowLeft') handlePrev();
      if (e.key === 'ArrowRight') handleNext();
      if (e.key === 'Escape') setIsFullScreenOpen(false);
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isFullScreenOpen]);

  const openFullScreen = (idx) => {
    setSelectedIndex(idx);
    setIsFullScreenOpen(true);
  };

  return (
    <div style={{ padding: '20px 24px', maxWidth: 1400, margin: '0 auto', color: '#f0ede8', fontFamily: 'Inter, system-ui, sans-serif' }}>
      
      {/* HEADER PESTAÑA AVATARES UNIFICADO PALETA HB GOLD */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 18, paddingBottom: 14, borderBottom: '1px solid rgba(212,175,106,0.15)' }}>
        <div>
          <span style={{ padding: '3px 10px', borderRadius: 16, background: 'rgba(212,175,106,0.1)', color: '#d4af6a', fontSize: 10, fontWeight: 800, letterSpacing: 1, border: '1px solid rgba(212,175,106,0.25)' }}>
            👑 PARRILLA OFICIAL DE AVATARES 3D (GUILLERMO AI)
          </span>
          <h2 style={{ fontSize: 22, fontWeight: 800, color: '#d4af6a', margin: '6px 0 2px 0' }}>
            Catálogo Tridimensional de Avatares Digitales
          </h2>
          <p style={{ fontSize: 12, color: '#a09d99', margin: 0 }}>
            {AVATAR_CATALOG.length} modelos oficiales de Guillermo AI. Haz clic en cualquier avatar para abrirlo a <strong>PANTALLA COMPLETA</strong>.
          </p>
        </div>

        <div style={{ background: '#161412', border: '1px solid rgba(212,175,106,0.2)', padding: '8px 14px', borderRadius: 8, textAlign: 'right' }}>
          <div style={{ color: '#d4af6a', fontSize: 12, fontWeight: 700 }}>Modelo Activo: {selectedAvatar.name}</div>
          <div style={{ color: '#6b6866', fontSize: 10 }}>{selectedAvatar.style}</div>
        </div>
      </div>

      {/* ─── PARRILLA HORIZONTAL DE 6 COLUMNAS CON IMÁGENES ESTÁTICAS CRISTALINAS ─── */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(6, 1fr)',
          gap: 14,
          maxHeight: '52vh',
          overflowY: 'auto',
          paddingRight: 4,
          paddingBottom: 14,
          marginBottom: 20
        }}
      >
        {AVATAR_CATALOG.map((av, idx) => {
          const isSelected = selectedIndex === idx;
          const isHovered = hoverId === av.id;

          return (
            <div
              key={av.id}
              onClick={() => openFullScreen(idx)}
              onMouseEnter={() => setHoverId(av.id)}
              onMouseLeave={() => setHoverId(null)}
              style={{
                cursor: 'pointer',
                borderRadius: 10,
                overflow: 'hidden',
                position: 'relative',
                background: isSelected ? 'rgba(212,175,106,0.08)' : '#161412',
                border: isSelected ? '2px solid #d4af6a' : (isHovered ? '1px solid #d4af6a' : '1px solid rgba(255,255,255,0.08)'),
                transition: 'all 0.2s ease',
                transform: isHovered ? 'translateY(-3px)' : 'none',
                boxShadow: isSelected ? '0 8px 20px rgba(212,175,106,0.2)' : '0 4px 10px rgba(0,0,0,0.5)',
                display: 'flex',
                flexDirection: 'column',
                height: 260
              }}
            >
              {/* Imagen Avatar Estática Limpia */}
              <div style={{ position: 'relative', width: '100%', height: 185, background: '#000', overflow: 'hidden' }}>
                <img
                  src={av.img}
                  alt={av.name}
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover',
                    objectPosition: 'top center',
                    filter: isHovered || isSelected ? 'brightness(1.05)' : 'brightness(0.9)',
                    transition: 'all 0.3s ease'
                  }}
                />
                
                {/* Badge Superior */}
                <div style={{ position: 'absolute', top: 6, left: 6, zIndex: 3, padding: '2px 6px', borderRadius: 4, background: av.badgeBg, color: '#fff', fontSize: 9, fontWeight: 900 }}>
                  <span>{av.badge}</span>
                </div>

                <div style={{ position: 'absolute', bottom: 6, right: 6, zIndex: 3, padding: '2px 6px', borderRadius: 4, background: 'rgba(0,0,0,0.7)', border: '1px solid #d4af6a', color: '#d4af6a', fontSize: 9, fontWeight: 800 }}>
                  🔍 PANTALLA COMPLETA
                </div>
              </div>

              {/* Info Inferior */}
              <div style={{ padding: '8px 10px', background: '#161412', flexGrow: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                <div style={{ color: isSelected ? '#d4af6a' : '#f0ede8', fontWeight: 700, fontSize: 11, marginBottom: 2, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {av.name}
                </div>
                <div style={{ color: '#6b6866', fontSize: 9, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {av.style}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* ─── INSPECTOR DEL MODELO SELECCIONADO ─── */}
      <div style={{ background: '#161412', border: '1px solid rgba(212,175,106,0.2)', borderRadius: 12, padding: '16px 20px', display: 'grid', gridTemplateColumns: '140px 1fr', gap: 20, alignItems: 'center' }}>
        <div 
          onClick={() => openFullScreen(selectedIndex)}
          style={{ height: 150, borderRadius: 8, overflow: 'hidden', background: '#000', border: '1px solid #d4af6a', cursor: 'pointer', position: 'relative' }}
        >
          <img src={selectedAvatar.img} alt={selectedAvatar.name} style={{ width: '100%', height: '100%', objectFit: 'cover', objectPosition: 'top center' }} />
          <div style={{ position: 'absolute', inset: 0, background: 'rgba(0,0,0,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: 0.8 }}>
            <span style={{ color: '#d4af6a', fontSize: 12, background: 'rgba(0,0,0,0.8)', padding: '2px 8px', borderRadius: 4, fontWeight: 800 }}>🔍 AMPLIFEST</span>
          </div>
        </div>

        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
            <span style={{ padding: '2px 8px', borderRadius: 4, background: selectedAvatar.badgeBg, color: '#fff', fontSize: 10, fontWeight: 900 }}>{selectedAvatar.badge}</span>
            <h3 style={{ fontSize: 18, fontWeight: 800, color: '#d4af6a', margin: 0 }}>{selectedAvatar.name}</h3>
          </div>

          <p style={{ color: '#a09d99', fontSize: 12, margin: '0 0 10px 0' }}>{selectedAvatar.style}</p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 10, fontSize: 11 }}>
            <div style={{ background: 'rgba(255,255,255,0.03)', padding: '6px 10px', borderRadius: 6, border: '1px solid rgba(255,255,255,0.05)' }}>
              <span style={{ color: '#6b6866', display: 'block', marginBottom: 1 }}>Malla Facial</span>
              <strong style={{ color: '#d4af6a' }}>{selectedAvatar.mesh}</strong>
            </div>

            <div style={{ background: 'rgba(255,255,255,0.03)', padding: '6px 10px', borderRadius: 6, border: '1px solid rgba(255,255,255,0.05)' }}>
              <span style={{ color: '#6b6866', display: 'block', marginBottom: 1 }}>Postura Rigging</span>
              <strong style={{ color: '#d4af6a' }}>{selectedAvatar.pose}</strong>
            </div>

            <div style={{ background: 'rgba(255,255,255,0.03)', padding: '6px 10px', borderRadius: 6, border: '1px solid rgba(255,255,255,0.05)' }}>
              <span style={{ color: '#6b6866', display: 'block', marginBottom: 1 }}>Canal Alfa</span>
              <strong style={{ color: '#4ade80' }}>Transparente RGBA</strong>
            </div>

            <div style={{ background: 'rgba(255,255,255,0.03)', padding: '6px 10px', borderRadius: 6, border: '1px solid rgba(255,255,255,0.05)' }}>
              <span style={{ color: '#6b6866', display: 'block', marginBottom: 1 }}>Audio Master</span>
              <strong style={{ color: '#d4af6a' }}>Voz Real FM 48kHz</strong>
            </div>
          </div>
        </div>
      </div>

      {/* ─── MODAL IMMERSIVO DE PANTALLA COMPLETA (100VW x 100VH) CON FLECHAS IZQ/DER ─── */}
      {isFullScreenOpen && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            zIndex: 99999,
            background: 'rgba(5, 5, 5, 0.96)',
            backdropFilter: 'blur(20px)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            padding: '24px 32px',
            color: '#fff'
          }}
        >
          {/* BARRA SUPERIOR DEL MODAL PANTALLA COMPLETA */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', zIndex: 10 }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <span style={{ padding: '3px 10px', borderRadius: 6, background: selectedAvatar.badgeBg, color: '#fff', fontSize: 11, fontWeight: 900 }}>
                  {selectedAvatar.badge}
                </span>
                <h2 style={{ fontSize: 22, fontWeight: 900, color: '#d4af6a', margin: 0 }}>
                  {selectedAvatar.name}
                </h2>
              </div>
              <p style={{ fontSize: 12, color: '#a09d99', margin: '4px 0 0 0' }}>
                Modelo {selectedIndex + 1} de {AVATAR_CATALOG.length} · {selectedAvatar.style}
              </p>
            </div>

            <button
              onClick={() => setIsFullScreenOpen(false)}
              style={{
                background: 'rgba(212,175,106,0.15)',
                border: '1px solid #d4af6a',
                color: '#d4af6a',
                fontSize: 18,
                fontWeight: 900,
                width: 44,
                height: 44,
                borderRadius: '50%',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                transition: 'all 0.2s ease'
              }}
            >
              ✕
            </button>
          </div>

          {/* CUERPO CENTRAL CON AVATAR EN PANTALLA COMPLETA Y FLECHAS IZQ/DER */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexGrow: 1, position: 'relative', margin: '20px 0' }}>
            
            {/* BOTÓN FLECHA IZQUIERDA (◀) */}
            <button
              onClick={handlePrev}
              style={{
                zIndex: 10,
                background: 'rgba(15, 15, 15, 0.85)',
                border: '2px solid #d4af6a',
                color: '#d4af6a',
                width: 60,
                height: 60,
                borderRadius: '50%',
                fontSize: 24,
                fontWeight: 900,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 8px 24px rgba(0,0,0,0.8)',
                transition: 'all 0.2s ease'
              }}
            >
              ◀
            </button>

            {/* CONTENEDOR DE LA IMAGEN EN ALTA RESOLUCIÓN */}
            <div style={{ position: 'relative', height: '72vh', maxWidth: '60vw', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <img
                src={selectedAvatar.img}
                alt={selectedAvatar.name}
                style={{
                  maxHeight: '100%',
                  maxWidth: '100%',
                  objectFit: 'contain',
                  filter: 'drop-shadow(0 16px 40px rgba(0,0,0,0.9))'
                }}
              />
            </div>

            {/* BOTÓN FLECHA DERECHA (▶) */}
            <button
              onClick={handleNext}
              style={{
                zIndex: 10,
                background: 'rgba(15, 15, 15, 0.85)',
                border: '2px solid #d4af6a',
                color: '#d4af6a',
                width: 60,
                height: 60,
                borderRadius: '50%',
                fontSize: 24,
                fontWeight: 900,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 8px 24px rgba(0,0,0,0.8)',
                transition: 'all 0.2s ease'
              }}
            >
              ▶
            </button>

          </div>

          {/* BARRA INFERIOR DE CONTROLES DEL MODAL */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(22,20,18,0.9)', border: '1px solid rgba(212,175,106,0.3)', padding: '12px 24px', borderRadius: 12, zIndex: 10 }}>
            <div style={{ display: 'flex', gap: 16, fontSize: 12 }}>
              <span style={{ color: '#a09d99' }}>Malla 3D: <strong style={{ color: '#d4af6a' }}>{selectedAvatar.mesh}</strong></span>
              <span style={{ color: '#a09d99' }}>Rigging: <strong style={{ color: '#d4af6a' }}>{selectedAvatar.pose}</strong></span>
              <span style={{ color: '#a09d99' }}>Formato: <strong style={{ color: '#4ade80' }}>PNG RGBA 1080p Transparent</strong></span>
            </div>

            <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
              <span style={{ fontSize: 11, color: '#6b6866' }}>Usa ◄ y ► en tu teclado para navegar</span>
              <button
                onClick={() => setIsFullScreenOpen(false)}
                style={{
                  background: 'linear-gradient(135deg, #d4af6a 0%, #b48a3c 100%)',
                  border: 'none',
                  color: '#000',
                  padding: '8px 20px',
                  borderRadius: 6,
                  fontWeight: 900,
                  fontSize: 12,
                  cursor: 'pointer'
                }}
              >
                CERRAR VISTA COMPLETA ✕
              </button>
            </div>
          </div>

        </div>
      )}

    </div>
  );
}
