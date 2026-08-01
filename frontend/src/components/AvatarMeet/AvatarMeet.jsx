import React, { useState } from 'react';

// ─── CLOUD-FIRST PROTOCOL & CACHE BUSTING ──────────────────────────────────
const CLOUD_BASE_URL = 'https://hb-jewelry-app.web.app';
const IS_PROD = window.location.hostname !== 'localhost';
const cloudAsset = (f) => IS_PROD ? `${CLOUD_BASE_URL}/${f}?v=20260801_v6Grid` : `/${f}?v=20260801_v6Grid`;

// ─── CATÁLOGO DE AVATARES OFICIALES GUILLERMO AI ─────────────────────────────
const AVATAR_CATALOG = [
  { id: 'master',    name: 'Guillermo — Master Principal 3D', style: 'Identidad Raíz · HB Official Master', img: cloudAsset('avatar_pro.png'), accent: '#fbbf24', badge: '👑', badgeBg: '#b45309', isPpal: true },
  { id: 'studio',    name: 'Guillermo — Studio 3D (De Pie)',  style: 'Cuerpo Entero · Micrófono Boom · Jeans', img: cloudAsset('avatars/studio_mic.png'), accent: '#d4af6a', badge: '🎙️', badgeBg: '#7c3aed' },
  { id: 'desk',      name: 'Guillermo — Escritorio 3D',       style: 'Silla Ejecutiva · Micrófono al Frente', img: cloudAsset('avatars/desk_mic.png'), accent: '#60a5fa', badge: '🎧', badgeBg: '#1d4ed8' },
  { id: 'casual',    name: 'Guillermo — Casual Azul 3D',      style: 'Confiado · Blue Jeans · Logo HB', img: cloudAsset('avatars/azul.png'), accent: '#34d399', badge: '👔', badgeBg: '#059669' },
  { id: 'premium',   name: 'Guillermo — Premium Blanco 3D',   style: 'Elegante · Blue Jeans · Logo HB', img: cloudAsset('avatars/blanco.png'), accent: '#e2e8f0', badge: '⭐', badgeBg: '#475569' },
  { id: 'vip',       name: 'Guillermo — VIP Gold 3D',         style: 'Colección HB 18k · Malla Volumétrica', img: cloudAsset('avatars/dorado.png'), accent: '#f87171', badge: '👑', badgeBg: '#b91c1c' },
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
            Visualización limpia en 6 columnas con scroll vertical expansivo e imágenes PNG transparentes RGBA
          </p>
        </div>

        <div style={{ background: 'rgba(15,23,42,0.8)', border: '1px solid rgba(251,191,36,0.3)', padding: '10px 18px', borderRadius: 12, textAlign: 'right' }}>
          <div style={{ color: '#fbbf24', fontSize: 13, fontWeight: 800 }}>Modelo Activo: {selectedAvatar.name}</div>
          <div style={{ color: '#94a3b8', fontSize: 11 }}>{selectedAvatar.style}</div>
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
                height: 290
              }}
            >
              {/* Imagen Avatar */}
              <div style={{ position: 'relative', width: '100%', height: 210, background: 'radial-gradient(circle at center, #1a1a2e 0%, #050505 100%)', overflow: 'hidden' }}>
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
                  <span>{av.badge}</span> <span>{av.id.toUpperCase()}</span>
                </div>

                {isSelected && (
                  <div style={{ position: 'absolute', bottom: 8, right: 8, zIndex: 3, padding: '2px 8px', borderRadius: 6, background: '#fbbf24', color: '#000', fontSize: 10, fontWeight: 900 }}>
                    SELECCIONADO
                  </div>
                )}
              </div>

              {/* Info Inferior */}
              <div style={{ padding: '10px 12px', background: '#0a0a0a', flexGrow: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                <div style={{ color: isSelected ? '#fbbf24' : '#ffffff', fontWeight: 800, fontSize: 12, marginBottom: 2, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {av.name}
                </div>
                <div style={{ color: '#888', fontSize: 10, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {av.style}
                </div>
              </div>
            </div>
          );
        })}
      </div>

    </div>
  );
}
