import "../../styles/hb.css";

const Dashboard = ({ actividades = [] }) => {
  const recientes = actividades.slice(-5).reverse();

  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <h1 className="hb-page-title">Dashboard</h1>
        <p className="hb-page-subtitle">Panel principal del sistema</p>
      </div>

      <div className="hb-card">
        <div className="hb-card-header">Actividad reciente</div>
        <div className="hb-table-wrap">
          <table className="hb-table">
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>Evento</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              {recientes.map((act, idx) => (
                <tr key={idx}>
                  <td>{act.timestamp}</td>
                  <td>{act.evento}</td>
                  <td>
                    <span className={act.estado === 'completado' ? 'hb-badge hb-badge-green' : 'hb-badge hb-badge-red'}>
                      {act.estado}
                    </span>
                  </td>
                </tr>
              ))}
              {recientes.length === 0 && (
                <tr>
                  <td colSpan="3" style={{ textAlign: 'center', padding: '1rem', color: '#f0ede8' }}>
                    No hay actividad reciente
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      <div className="hb-card">
        <div className="hb-card-header">Acciones rápidas</div>
        <div style={{ padding: '1rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          <button className="hb-btn hb-btn-sm">Agregar producto</button>
          <button className="hb-btn hb-btn-sm">Ver pedidos</button>
          <button className="hb-btn hb-btn-sm">Reportes</button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;



