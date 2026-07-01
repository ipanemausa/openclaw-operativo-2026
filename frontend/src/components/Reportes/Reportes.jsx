import '../../styles/hb.css';
import React from 'react';

const Reportes = () => {
  const resumen = {
    totalVentas: 125400.75,
    totalOrdenes: 342,
    productosActivos: 89
  };

  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <h1 className="hb-page-title">Reportes Ejecutivos</h1>
        <p className="hb-page-subtitle">Resumen General del Negocio</p>
      </div>

      <div className="hb-form-grid" style={{ gap: '24px', marginTop: '32px' }}>
        <div className="hb-card" style={{ background: '#1a1a1a', border: '2px solid #d4af6a' }}>
          <div className="hb-card-header" style={{ borderBottom: '1px solid #d4af6a' }}>
            <span className="hb-card-name" style={{ color: '#d4af6a' }}>Ventas Totales</span>
          </div>
          <div style={{ padding: '20px', textAlign: 'center' }}>
            <h2 className="hb-card-price" style={{ fontSize: '2.5rem', margin: 0, color: '#d4af6a' }}>
              ${resumen.totalVentas.toLocaleString()}
            </h2>
            <p style={{ color: '#f0ede8', marginTop: '8px', opacity: 0.8 }}>Ingresos acumulados</p>
          </div>
        </div>

        <div className="hb-card" style={{ background: '#1a1a1a', border: '2px solid #d4af6a' }}>
          <div className="hb-card-header" style={{ borderBottom: '1px solid #d4af6a' }}>
            <span className="hb-card-name" style={{ color: '#d4af6a' }}>Órdenes Activas</span>
          </div>
          <div style={{ padding: '20px', textAlign: 'center' }}>
            <h2 className="hb-card-price" style={{ fontSize: '2.5rem', margin: 0, color: '#d4af6a' }}>
              {resumen.totalOrdenes}
            </h2>
            <p style={{ color: '#f0ede8', marginTop: '8px', opacity: 0.8 }}>Órdenes en proceso</p>
          </div>
        </div>

        <div className="hb-card" style={{ background: '#1a1a1a', border: '2px solid #d4af6a' }}>
          <div className="hb-card-header" style={{ borderBottom: '1px solid #d4af6a' }}>
            <span className="hb-card-name" style={{ color: '#d4af6a' }}>Productos Activos</span>
          </div>
          <div style={{ padding: '20px', textAlign: 'center' }}>
            <h2 className="hb-card-price" style={{ fontSize: '2.5rem', margin: 0, color: '#d4af6a' }}>
              {resumen.productosActivos}
            </h2>
            <p style={{ color: '#f0ede8', marginTop: '8px', opacity: 0.8 }}>Productos disponibles</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Reportes;




