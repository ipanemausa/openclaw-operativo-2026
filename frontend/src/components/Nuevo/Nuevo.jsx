import React, { useState, useEffect } from 'react';
import '../../styles/hb.css';

const PlanDiario = () => {
  const [plan, setPlan] = useState([
    { bloque: 1, titulo: 'Instalar OpenClaw 2026.6.10', completo: false },
    { bloque: 2, titulo: 'Conectar OpenClaw con DeepSeek', completo: false },
    { bloque: 3, titulo: 'Historial real con Redis', completo: false },
    { bloque: 4, titulo: 'Navegación mejorada (scroll, adjuntos)', completo: false },
    { bloque: 5, titulo: 'Deploy Cloud Run', completo: false },
    { bloque: 6, titulo: 'Cierre y contexto 2026-06-30', completo: false },
  ]);

  const toggleBloque = (bloque) => {
    setPlan(prev =>
      prev.map(item =>
        item.bloque === bloque ? { ...item, completo: !item.completo } : item
      )
    );
  };

  const bloquesCompletos = plan.filter(b => b.completo).length;

  return (
    <div className="hb-page" style={{ padding: '2rem' }}>
      <div className="hb-page-header">
        <h1 className="hb-page-title">📋 Plan Diario — OpenClaw 2026</h1>
        <p className="hb-page-subtitle">
          Fecha: 2026-06-29 | Progreso: {bloquesCompletos}/{plan.length} bloques
        </p>
      </div>

      <div style={{ marginBottom: '2rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
        <button
          className="hb-btn"
          style={{ background: '#d4af6a', color: '#1a1a1a', border: 'none', padding: '0.75rem 1.5rem', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}
          onClick={() => setPlan(plan.map(p => ({ ...p, completo: false })))}
        >
          🔄 Resetear todo
        </button>

        <button
          className="hb-btn"
          style={{ background: '#d4af6a', color: '#1a1a1a', border: 'none', padding: '0.75rem 1.5rem', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}
          onClick={() => navigator.clipboard.writeText(JSON.stringify(plan, null, 2))}
        >
          📋 Copiar estado
        </button>

        <span className="hb-badge" style={{ alignSelf: 'center', fontSize: '1.1rem' }}>
          {bloquesCompletos === plan.length ? '✅ COMPLETADO' : `${bloquesCompletos}/${plan.length} completados`}
        </span>
      </div>

      <div className="hb-form">
        {plan.map((bloque) => (
          <div
            key={bloque.bloque}
            className="hb-card"
            style={{
              marginBottom: '1rem',
              cursor: 'pointer',
              opacity: bloque.completo ? 0.8 : 1,
              border: bloque.completo ? '2px solid #4caf50' : '2px solid transparent',
              transition: 'all 0.3s ease',
            }}
            onClick={() => toggleBloque(bloque.bloque)}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '1rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <span
                  className={`hb-badge ${bloque.completo ? 'hb-badge-green' : 'hb-badge-red'}`}
                  style={{ minWidth: '60px', textAlign: 'center' }}
                >
                  BLOQUE {bloque.bloque}
                </span>
                <span style={{ color: bloque.completo ? '#4caf50' : '#f0ede8', fontWeight: 'bold', fontSize: '1.1rem' }}>
                  {bloque.titulo}
                </span>
              </div>
              <span style={{ fontSize: '1.5rem' }}>
                {bloque.completo ? '✅' : '⬜'}
              </span>
            </div>
          </div>
        ))}
      </div>

      <div className="hb-card" style={{ marginTop: '2rem', padding: '1.5rem' }}>
        <h3 style={{ color: '#d4af6a', marginBottom: '1rem' }}>🎯 Próximo paso sugerido</h3>
        <p style={{ color: '#f0ede8' }}>
          {bloquesCompletos === 0 && 'Arrancar con Bloque 1: Instalar OpenClaw 2026.6.10'}
          {bloquesCompletos === 1 && 'Continuar con Bloque 2: Conectar DeepSeek'}
          {bloquesCompletos === 2 && 'Siguiente: Bloque 3 — Historial real con Redis'}
          {bloquesCompletos === 3 && 'Avanzar: Bloque 4 — Navegación mejorada'}
          {bloquesCompletos === 4 && 'Preparar: Bloque 5 — Deploy Cloud Run'}
          {bloquesCompletos === 5 && 'Último: Bloque 6 — Cierre y contexto'}
          {bloquesCompletos === 6 && '🎉 Plan completado. ¿Generar reporte de logros?'}
        </p>
      </div>
    </div>
  );
};

export default PlanDiario;