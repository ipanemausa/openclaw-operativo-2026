import "../../styles/hb.css";

const Workspace = () => {
  const recentFiles = [
    { name: 'anillo-diamante.png', type: 'Imagen', date: '2024-12-05', size: '2.4 MB' },
    { name: 'collar-perlas.3mf', type: 'Modelo 3D', date: '2024-12-04', size: '5.1 MB' },
    { name: 'pendiente-esmeralda.png', type: 'Imagen', date: '2024-12-03', size: '1.8 MB' },
    { name: 'pulsera-oro.wrl', type: 'Prototipo', date: '2024-12-02', size: '3.6 MB' },
  ];

  const activities = [
    { action: 'Exportación completada', project: 'Anillo Diamante', time: 'hace 2 min', status: 'success' },
    { action: 'Error de renderizado', project: 'Collar Perlas', time: 'hace 15 min', status: 'error' },
    { action: 'Archivo subido', project: 'Pendiente Esmeralda', time: 'hace 1 hora', status: 'info' },
    { action: 'Optimización de malla', project: 'Pulsera Oro', time: 'hace 2 horas', status: 'warning' },
    { action: 'Cambio de textura', project: 'Anillo Diamante', time: 'hace 3 horas', status: 'info' },
  ];

  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <h1 className="hb-page-title">Espacio de Trabajo</h1>
        <p className="hb-page-subtitle">Proyecto: Colección Navidad 2024</p>
      </div>

      <div style={{ display: 'flex', gap: '1.5rem', marginTop: '1.5rem' }}>
        {/* Panel izquierdo - Métricas principales */}
        <div style={{ flex: '0 0 30%' }}>
          <div className="hb-card" style={{ marginBottom: '1rem' }}>
            <div className="hb-card-header">
              <span className="hb-card-name">Estado del Proyecto</span>
            </div>
            <div style={{ padding: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.8rem' }}>
                <span>Archivos totales</span>
                <span>24</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.8rem' }}>
                <span>Versión actual</span>
                <span>v3.2.1</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.8rem' }}>
                <span>Último guardado</span>
                <span>10:45 AM</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.8rem' }}>
                <span>Espacio usado</span>
                <span>156 MB / 500 MB</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span>Proyectos activos</span>
                <span>4</span>
              </div>
            </div>
          </div>

          <div className="hb-card">
            <div className="hb-card-header">
              <span className="hb-card-name">Acciones Rápidas</span>
            </div>
            <div style={{ padding: '1rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <button className="hb-btn">Nuevo Archivo</button>
              <button className="hb-btn">Exportar Proyecto</button>
              <button className="hb-btn hb-btn-sm">Guardar Progreso</button>
            </div>
          </div>
        </div>

        {/* Panel central - Archivos recientes */}
        <div style={{ flex: 1 }}>
          <div className="hb-card">
            <div className="hb-card-header">
              <span className="hb-card-name">Archivos Recientes</span>
              <span className="hb-badge">4 archivos</span>
            </div>
            <div className="hb-table-wrap">
              <table className="hb-table">
                <thead>
                  <tr>
                    <th>Nombre</th>
                    <th>Tipo</th>
                    <th>Fecha</th>
                    <th>Tamaño</th>
                  </tr>
                </thead>
                <tbody>
                  {recentFiles.map((file, index) => (
                    <tr key={index}>
                      <td>{file.name}</td>
                      <td>{file.type}</td>
                      <td>{file.date}</td>
                      <td>{file.size}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Panel derecho - Actividad del sistema */}
        <div style={{ flex: '0 0 30%' }}>
          <div className="hb-card">
            <div className="hb-card-header">
              <span className="hb-card-name">Actividad del Sistema</span>
              <span className="hb-badge hb-badge-green">En vivo</span>
            </div>
            <div style={{ padding: '1rem', maxHeight: '400px', overflowY: 'auto' }}>
              {activities.map((activity, index) => (
                <div key={index} style={{
                  padding: '0.8rem 0',
                  borderBottom: index < activities.length - 1 ? '1px solid rgba(212,175,106,0.2)' : 'none',
                  marginBottom: index < activities.length - 1 ? '0.5rem' : '0',
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.3rem' }}>
                    <span style={{ fontWeight: 'bold', color: '#d4af6a' }}>{activity.action}</span>
                    <span className={`hb-badge ${activity.status === 'error' ? 'hb-badge-red' : activity.status === 'success' ? 'hb-badge-green' : ''}`}>
                      {activity.status === 'error' ? 'Error' : activity.status === 'success' ? 'OK' : 'Info'}
                    </span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
                    <span>{activity.project}</span>
                    <span>{activity.time}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Workspace;








