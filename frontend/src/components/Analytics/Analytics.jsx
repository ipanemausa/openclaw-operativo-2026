import React, { useState, useEffect } from 'react';
import "../../styles/hb.css";

const Analytics = () => {
  const [ventasData, setVentasData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/hb/ventas')
      .then(res => res.json())
      .then(data => {
        setVentasData(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching ventas:', err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="hb-page" style={{ color: '#f0ede8' }}>
        <p>Cargando analíticas...</p>
      </div>
    );
  }

  if (!ventasData) {
    return (
      <div className="hb-page" style={{ color: '#f0ede8' }}>
        <p>Error al cargar datos.</p>
      </div>
    );
  }

  // Datos de ejemplo para el gráfico y tarjetas
  const canales = ventasData.canales || ['Online', 'Tienda', 'Mayoreo', 'Otros'];
  const ventasPorCanal = ventasData.porCanal || [45000, 32000, 18000, 7000];
  const totalVentas = ventasData.totalVentas || 102000;
  const tendencias = ventasData.tendencias || { mesActual: 15, mesAnterior: 8 };

  const maxVenta = Math.max(...ventasPorCanal);

  // Datos de ejemplo para tarjetas de métricas
  const metricas = [
    { label: 'Ventas Totales', valor: `$${totalVentas.toLocaleString()}`, tendencia: '+12%' },
    { label: 'Pedidos', valor: ventasData.pedidos || 342, tendencia: '+8%' },
    { label: 'Ticket Promedio', valor: `$${ventasData.ticketPromedio || 298}`, tendencia: '+5%' },
    { label: 'Clientes Nuevos', valor: ventasData.clientesNuevos || 87, tendencia: '+23%' }
  ];

  return (
    <div className="hb-page" style={{ color: '#f0ede8' }}>
      <div className="hb-page-header">
        <h1 className="hb-page-title" style={{ color: '#d4af6a' }}>Analíticas de Ventas</h1>
        <p className="hb-page-subtitle">Resumen de rendimiento y tendencias</p>
      </div>

      {/* Tarjetas de Métricas */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginBottom: '40px' }}>
        {metricas.map((metrica, index) => (
          <div key={index} className="hb-card" style={{
            background: '#1a1a1a',
            border: '1px solid #d4af6a',
            padding: '24px',
            borderRadius: '8px'
          }}>
            <div className="hb-card-name" style={{ color: '#d4af6a', fontSize: '14px', marginBottom: '8px' }}>
              {metrica.label}
            </div>
            <div style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>
              {metrica.valor}
            </div>
            <span className="hb-badge hb-badge-green" style={{ background: '#1a3a1a', color: '#4caf50' }}>
              {metrica.tendencia}
            </span>
          </div>
        ))}
      </div>

      {/* Gráfico de Ventas por Canal */}
      <div style={{ marginBottom: '40px' }}>
        <h2 style={{ color: '#d4af6a', marginBottom: '20px', fontSize: '20px' }}>Ventas por Canal</h2>
        <div style={{
          display: 'flex',
          alignItems: 'flex-end',
          gap: '20px',
          padding: '20px',
          background: '#1a1a1a',
          border: '1px solid #d4af6a',
          borderRadius: '8px',
          minHeight: '200px'
        }}>
          {canales.map((canal, index) => (
            <div key={index} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <div style={{
                width: '100%',
                height: `${(ventasPorCanal[index] / maxVenta) * 180}px`,
                background: 'linear-gradient(180deg, #d4af6a 0%, #b8963a 100%)',
                borderRadius: '4px 4px 0 0',
                transition: 'height 0.3s ease'
              }} />
              <div style={{ marginTop: '8px', textAlign: 'center' }}>
                <div style={{ color: '#f0ede8', fontWeight: 'bold' }}>{canal}</div>
                <div style={{ color: '#d4af6a', fontSize: '12px' }}>${ventasPorCanal[index].toLocaleString()}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Tendencias */}
      <div style={{ marginBottom: '40px' }}>
        <h2 style={{ color: '#d4af6a', marginBottom: '20px', fontSize: '20px' }}>Tendencias Mensuales</h2>
        <div className="hb-card" style={{
          background: '#1a1a1a',
          border: '1px solid #d4af6a',
          padding: '24px',
          borderRadius: '8px'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-around', marginBottom: '20px' }}>
            <div>
              <div style={{ color: '#d4af6a', fontSize: '14px', marginBottom: '4px' }}>Mes Anterior</div>
              <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{tendencias.mesAnterior}%</div>
            </div>
            <div>
              <div style={{ color: '#d4af6a', fontSize: '14px', marginBottom: '4px' }}>Mes Actual</div>
              <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{tendencias.mesActual}%</div>
            </div>
          </div>
          <div style={{ position: 'relative', height: '40px', background: '#2a2a2a', borderRadius: '20px', overflow: 'hidden' }}>
            <div style={{
              width: `${(tendencias.mesActual / (tendencias.mesActual + tendencias.mesAnterior)) * 100}%`,
              height: '100%',
              background: 'linear-gradient(90deg, #d4af6a, #b8963a)',
              borderRadius: '20px',
              transition: 'width 0.5s ease'
            }} />
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '8px', color: '#f0ede8' }}>
            <span>0%</span>
            <span>100%</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;





