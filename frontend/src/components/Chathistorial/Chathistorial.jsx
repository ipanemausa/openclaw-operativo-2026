import React, { useState, useEffect } from 'react';
import '../../styles/hb.css';

// Tarea 1: ChatHistorial
const ChatHistorial = () => {
  const [historial, setHistorial] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistorial = async () => {
      try {
        const response = await fetch('/api/hb/historial');
        const data = await response.json();
        setHistorial(data);
      } catch (error) {
        console.error('Error fetching historial:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchHistorial();
  }, []);

  if (loading) {
    return (
      <div className="hb-page" style={{ color: '#d4af6a', textAlign: 'center', padding: '2rem' }}>
        <p>Cargando historial...</p>
      </div>
    );
  }

  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <h2 className="hb-page-title" style={{ color: '#d4af6a' }}>Historial de Conversaciones</h2>
      </div>
      <div className="hb-table-wrap">
        <table className="hb-table">
          <thead>
            <tr>
              <th style={{ color: '#d4af6a' }}>Fecha</th>
              <th style={{ color: '#d4af6a' }}>Usuario</th>
              <th style={{ color: '#d4af6a' }}>Mensaje</th>
            </tr>
          </thead>
          <tbody>
            {historial.length === 0 ? (
              <tr>
                <td colSpan="3" style={{ color: '#f0ede8', textAlign: 'center' }}>Sin conversaciones previas</td>
              </tr>
            ) : (
              historial.map((item, index) => (
                <tr key={index}>
                  <td style={{ color: '#f0ede8' }}>{item.fecha || 'N/A'}</td>
                  <td style={{ color: '#f0ede8' }}>{item.usuario || 'Anónimo'}</td>
                  <td style={{ color: '#f0ede8' }}>{item.mensaje || 'Sin contenido'}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// Tarea 2: Settings
const Settings = () => {
  const [modelo, setModelo] = useState('gpt-4');
  const [idioma, setIdioma] = useState('es');
  const [tema, setTema] = useState('oscuro');

  const handleSave = (e) => {
    e.preventDefault();
    console.log('Configuración guardada:', { modelo, idioma, tema });
  };

  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <h2 className="hb-page-title" style={{ color: '#d4af6a' }}>Configuración del Sistema</h2>
        <p className="hb-page-subtitle" style={{ color: '#f0ede8' }}>Ajusta las preferencias del asistente</p>
      </div>
      <div className="hb-card" style={{ backgroundColor: '#1a1a1a', border: '1px solid #d4af6a' }}>
        <form className="hb-form" onSubmit={handleSave}>
          <div className="hb-form-grid">
            <div>
              <label style={{ color: '#d4af6a', display: 'block', marginBottom: '0.5rem' }}>Modelo Activo</label>
              <select
                className="hb-select"
                value={modelo}
                onChange={(e) => setModelo(e.target.value)}
                style={{ width: '100%' }}
              >
                <option value="gpt-4">GPT-4</option>
                <option value="gpt-3.5">GPT-3.5</option>
                <option value="claude">Claude</option>
              </select>
            </div>
            <div>
              <label style={{ color: '#d4af6a', display: 'block', marginBottom: '0.5rem' }}>Idioma</label>
              <select
                className="hb-select"
                value={idioma}
                onChange={(e) => setIdioma(e.target.value)}
                style={{ width: '100%' }}
              >
                <option value="es">Español</option>
                <option value="en">Inglés</option>
                <option value="fr">Francés</option>
              </select>
            </div>
            <div>
              <label style={{ color: '#d4af6a', display: 'block', marginBottom: '0.5rem' }}>Tema</label>
              <select
                className="hb-select"
                value={tema}
                onChange={(e) => setTema(e.target.value)}
                style={{ width: '100%' }}
              >
                <option value="oscuro">Oscuro</option>
                <option value="claro">Claro</option>
                <option value="dorado">Dorado</option>
              </select>
            </div>
          </div>
          <button type="submit" className="hb-btn" style={{ backgroundColor: '#d4af6a', color: '#1a1a1a', marginTop: '1rem' }}>
            Guardar Configuración
          </button>
        </form>
      </div>
    </div>
  );
};

// Tarea 3: Notificaciones
const Notificaciones = () => {
  const [notificaciones] = useState([
    { id: 1, mensaje: 'Nuevo pedido recibido', tipo: 'info', fecha: '2024-01-15' },
    { id: 2, mensaje: 'Actualización del sistema completada', tipo: 'success', fecha: '2024-01-14' },
    { id: 3, mensaje: 'Alerta: baja disponibilidad de inventario', tipo: 'warning', fecha: '2024-01-13' },
  ]);
  const conteo = notificaciones.length;

  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <h2 className="hb-page-title" style={{ color: '#d4af6a' }}>
          Notificaciones <span className="hb-badge" style={{ backgroundColor: '#d4af6a', color: '#1a1a1a' }}>{conteo}</span>
        </h2>
        <p className="hb-page-subtitle" style={{ color: '#f0ede8' }}>Alertas recientes del sistema</p>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        {notificaciones.length === 0 && (
          <p style={{ color: '#f0ede8', textAlign: 'center' }}>No hay notificaciones nuevas</p>
        )}
        {notificaciones.map((notif) => (
          <div
            key={notif.id}
            className="hb-card"
            style={{
              backgroundColor: '#1a1a1a',
              border: '1px solid #d4af6a',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '1rem',
            }}
          >
            <div>
              <p className="hb-card-name" style={{ color: '#f0ede8' }}>{notif.mensaje}</p>
              <p className="hb-card-meta" style={{ color: '#d4af6a' }}>{notif.fecha}</p>
            </div>
            <span
              className={`hb-badge ${notif.tipo === 'success' ? 'hb-badge-green' : notif.tipo === 'warning' ? 'hb-badge-red' : ''}`}
              style={{ backgroundColor: notif.tipo === 'info' ? '#d4af6a' : undefined, color: '#1a1a1a' }}
            >
              {notif.tipo}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

// Tarea 4: Analytics
const Analytics = () => {
  const [ventas, setVentas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchVentas = async () => {
      try {
        const response = await fetch('/api/hb/ventas');
        const data = await response.json();
        setVentas(data.ventas || []);
      } catch (error) {
        console.error('Error fetching ventas:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchVentas();
  }, []);

  if (loading) {
    return (
      <div className="hb-page" style={{ color: '#d4af6a', textAlign: 'center', padding: '2rem' }}>
        <p>Cargando analytics...</p>
      </div>
    );
  }

  // Simulación de datos para gráfico si la API no devuelve nada
  const datosGrafico = ventas.length > 0 ? ventas : [
    { canal: 'Online', valor: 35000 },
    { canal: 'Tienda Física', valor: 28000 },
    { canal: 'Marketplace', valor: 15000 },
    { canal: 'WhatsApp', valor: 12000 },
    { canal: 'Corporativo', valor: 8000 },
  ];

  const maxValor = Math.max(...datosGrafico.map(d => d.valor), 1);

  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <h2 className="hb-page-title" style={{ color: '#d4af6a' }}>Analytics de Ventas por Canal</h2>
        <p className="hb-page-subtitle" style={{ color: '#f0ede8' }}>Distribución de ventas en el último mes</p>
      </div>
      <div className="hb-card" style={{ backgroundColor: '#1a1a1a', border: '1px solid #d4af6a' }}>
        <div style={{ padding: '1rem' }}>
          {datosGrafico.map((item, index) => (
            <div key={index} style={{ marginBottom: '1.5rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.3rem' }}>
                <span style={{ color: '#f0ede8', fontWeight: 'bold' }}>{item.canal}</span>
                <span style={{ color: '#d4af6a' }}>${item.valor.toLocaleString()}</span>
              </div>
              <div style={{ backgroundColor: '#333', borderRadius: '4px', height: '20px', overflow: 'hidden' }}>
                <div
                  style={{
                    width: `${(item.valor / maxValor) * 100}%`,
                    backgroundColor: '#d4af6a',
                    height: '100%',
                    borderRadius: '4px',
                    transition: 'width 0.5s ease',
                  }}
                />
              </div>
            </div>
          ))}
          <div style={{ marginTop: '1rem', textAlign: 'center', borderTop: '1px solid #d4af6a', paddingTop: '0.5rem' }}>
            <p style={{ color: '#d4af6a', fontSize: '0.9rem' }}>Total: ${datosGrafico.reduce((sum, d) => sum + d.valor, 0).toLocaleString()}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export { ChatHistorial, Settings, Notificaciones, Analytics };