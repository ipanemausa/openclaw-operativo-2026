import React, { useState } from 'react';

// ─── CLOUD-FIRST PROTOCOL & CACHE BUSTING ──────────────────────────────────
const CLOUD_BASE_URL = 'https://hb-jewelry-app.web.app';
const IS_PROD = window.location.hostname !== 'localhost';
const cloudAsset = (f) => IS_PROD ? `${CLOUD_BASE_URL}/${f}?v=20260801_vModelStudio` : `/${f}?v=20260801_vModelStudio`;

// ─── CATÁLOGO DE 8 AVATARES OFICIALES GUILLERMO AI (IMÁGENES HD PNG ESTÁTICAS) ───
const AVATAR_CATALOG = [
  {
    id: 'master',
    name: 'Guillermo — Master Principal 3D',
    style: 'Identidad Raíz · HB Official Master',
    img: cloudAsset('avatar_pro.png'),
    accent: '#fbbf24',
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
    accent: '#60a5fa',
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
    accent: '#34d399',
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
    accent: '#e2e8f0',
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
    accent: '#f87171',
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
    accent: '#cbd5e1',
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
    accent: '#f43f5e',
    badge: '🔥 RED',
    badgeBg: '#9f1239',
    mesh: 'Gesticulación Vocal Activa',
    pose: 'Actitud Dinámica Redes'
  }
];

export default function AvatarMeet() {
  const [selectedAvatar, setSelectedAvatar] = useState(AVATAR_CATALOG[0]);
  const [hoverId, setHoverId] = useState(null);

  return (
    <div style={{ padding: '24px 28px', maxWidth: 1440, margin: '0 auto', color: '#fff', fontFamily: 'Inter, system-ui, sans-serif' }}>
      
      {/* HEADER PESTAÑA AVATARES */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20, paddingBottom: 16, borderBottom: '1px solid rgba(212,175,106,0.2)' }}>
        <div>
          <span style={{ padding: '4px 12px', borderRadius: 20, background: 'linear-gradient(135deg, #b45309 0%, #78350f 100%)', color: '#fbbf24', fontSize: 11, fontWeight: 800, letterSpacing: 1, border: '1px solid #fbbf24' }}>
            👑 PARRILLA OFICIAL DE AVATARES 3D (GUILLERMO AI)
          </span>
          <h2 style={{ fontSize: 24, fontWeight: 900, color: '#ffffff', margin: '8px 0 4px 0' }}>
            Catálogo Tridimensional de Avatares Digitales
          </h2>
          <p style={{ fontSize: 13, color: '#94a3b8', margin: 0 }}>
            {AVATAR_CATALOG.length} modelos con fotos estáticas en alta definición, malla FLAME 3D y canal alfa transparente RGBA
          </p>
        </div>

        <div style={{ background: 'rgba(15,23,42,0.8)', border: '1px solid rgba(251,191,36,0.3)', padding: '10px 18px', borderRadius: 12, textAlign: 'right' }}>
          <div style={{ color: '#fbbf24', fontSize: 13, fontWeight: 800 }}>Modelo Activo: {selectedAvatar.name}</div>
          <div style={{ color: '#94a3b8', fontSize: 11 }}>{selectedAvatar.style}</div>
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
          paddingRight: 6,
          paddingBottom: 16,
          marginBottom: 24
        }}
      >
        {AVATAR_CATALOG.map((av) => {
          const isSelected = selectedAvatar.id === av.id;
          const isHovered = hoverId === av.id;

          return (
            <div
              key={av.id}
              onClick={() => setSelectedAvatar(av)}
              onMouseEnter={() => setHoverId(av.id)}
              onMouseLeave={() => setHoverId(null)}
              style={{
                cursor: 'pointer',
                borderRadius: 14,
                overflow: 'hidden',
                position: 'relative',
                background: isSelected ? 'linear-gradient(145deg, #1e1b4b 0%, #0f172a 100%)' : '#090d16',
                border: isSelected ? '2px solid #fbbf24' : (isHovered ? `1px solid ${av.accent}` : '1px solid rgba(255,255,255,0.08)'),
                transition: 'all 0.25s ease',
                transform: isHovered ? 'translateY(-4px)' : 'none',
                boxShadow: isSelected
                  ? '0 12px 30px rgba(251,191,36,0.35)'
                  : (isHovered ? `0 10px 24px ${av.accent}33` : '0 4px 12px rgba(0,0,0,0.5)'),
                display: 'flex',
                flexDirection: 'column',
                height: 270
              }}
            >
              {/* Imagen Avatar Estática Limpia (NUNCA VIDEO BORROSO) */}
              <div style={{ position: 'relative', width: '100%', height: 190, background: 'radial-gradient(circle at center, #1a1a2e 0%, #050505 100%)', overflow: 'hidden' }}>
                <img
                  src={av.img}
                  alt={av.name}
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover',
                    objectPosition: 'top center',
                    filter: isHovered || isSelected ? 'brightness(1.08)' : 'brightness(0.9)',
                    transition: 'all 0.3s ease'
                  }}
                />
                
                {/* Badge Superior */}
                <div style={{ position: 'absolute', top: 8, left: 8, zIndex: 3, padding: '3px 8px', borderRadius: 20, background: av.badgeBg, color: '#fff', fontSize: 10, fontWeight: 900, display: 'flex', alignItems: 'center', gap: 4, boxShadow: '0 2px 8px rgba(0,0,0,0.6)' }}>
                  <span>{av.badge}</span>
                </div>

                {isSelected && (
                  <div style={{ position: 'absolute', bottom: 8, right: 8, zIndex: 3, padding: '2px 8px', borderRadius: 6, background: '#fbbf24', color: '#000', fontSize: 10, fontWeight: 900 }}>
                    ACTIVO
                  </div>
                )}
              </div>

              {/* Info Inferior */}
              <div style={{ padding: '10px 12px', background: '#0a0a0a', flexGrow: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                <div style={{ color: isSelected ? '#fbbf24' : '#ffffff', fontWeight: 800, fontSize: 11, marginBottom: 2, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {av.name}
                </div>
                <div style={{ color: '#888', fontSize: 9, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {av.style}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* ─── INSPECTOR 3D DEL MODELO SELECCIONADO ─── */}
      <div style={{ background: 'rgba(15,23,42,0.85)', backdropFilter: 'blur(12px)', border: '1px solid rgba(251,191,36,0.3)', borderRadius: 16, padding: '20px 24px', display: 'grid', gridTemplateColumns: '180px 1fr', gap: 24, alignItems: 'center' }}>
        <div style={{ height: 180, borderRadius: 12, overflow: 'hidden', background: '#000', border: `2px solid ${selectedAvatar.accent}` }}>
          <img src={selectedAvatar.img} alt={selectedAvatar.name} style={{ width: '100%', height: '100%', objectFit: 'cover', objectPosition: 'top center' }} />
        </div>

        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
            <span style={{ padding: '3px 10px', borderRadius: 6, background: selectedAvatar.badgeBg, color: '#fff', fontSize: 11, fontWeight: 900 }}>{selectedAvatar.badge}</span>
            <h3 style={{ fontSize: 20, fontWeight: 900, color: '#ffffff', margin: 0 }}>{selectedAvatar.name}</h3>
          </div>

          <p style={{ color: '#cbd5e1', fontSize: 13, margin: '0 0 14px 0' }}>{selectedAvatar.style}</p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12, fontSize: 11 }}>
            <div style={{ background: 'rgba(255,255,255,0.04)', padding: '8px 12px', borderRadius: 8 }}>
              <span style={{ color: '#94a3b8', display: 'block', marginBottom: 2 }}>Malla Facial</span>
              <strong style={{ color: '#fbbf24' }}>{selectedAvatar.mesh}</strong>
            </div>

            <div style={{ background: 'rgba(255,255,255,0.04)', padding: '8px 12px', borderRadius: 8 }}>
              <span style={{ color: '#94a3b8', display: 'block', marginBottom: 2 }}>Postura Rigging</span>
              <strong style={{ color: '#60a5fa' }}>{selectedAvatar.pose}</strong>
            </div>

            <div style={{ background: 'rgba(255,255,255,0.04)', padding: '8px 12px', borderRadius: 8 }}>
              <span style={{ color: '#94a3b8', display: 'block', marginBottom: 2 }}>Canal Alfa</span>
              <strong style={{ color: '#34d399' }}>Transparente RGBA</strong>
            </div>

            <div style={{ background: 'rgba(255,255,255,0.04)', padding: '8px 12px', borderRadius: 8 }}>
              <span style={{ color: '#94a3b8', display: 'block', marginBottom: 2 }}>Audio Master</span>
              <strong style={{ color: '#ef4444' }}>Voz Real FM 48kHz</strong>
            </div>
          </div>
        </div>
      </div>

    </div>
  );
}
