import '../../styles/hb.css';

const Sidebar = ({ items, activeItem, onItemClick }) => {
  const sections = [
    { title: 'Principal', items: items.filter(item => ['Dashboard', 'Inicio', 'Resumen'].includes(item.label)) },
    { title: 'Operaciones', items: items.filter(item => ['Ventas', 'Compras', 'Inventario', 'Pedidos'].includes(item.label)) },
    { title: 'Sistema', items: items.filter(item => ['Usuarios', 'Roles', 'Auditoría'].includes(item.label)) },
    { title: 'Configuración', items: items.filter(item => ['Ajustes', 'Preferencias', 'Seguridad'].includes(item.label)) }
  ];

  return (
    <aside className="sidebar">
      {sections.map((section, idx) => (
        <div key={idx} className="sidebar-section">
          {idx > 0 && <hr className="sidebar-divider" />}
          <h3 className="sidebar-section-title">{section.title}</h3>
          <ul className="sidebar-menu">
            {section.items.map((item) => (
              <li
                key={item.id}
                className={`sidebar-item ${activeItem === item.id ? 'active' : ''}`}
                onClick={() => onItemClick(item.id)}
              >
                <span className="sidebar-icon">{item.icon}</span>
                <span className="sidebar-label">{item.label}</span>
              </li>
            ))}
          </ul>
        </div>
      ))}

      <style>{`
        .sidebar {
          background: #1a1a1a;
          color: #f0ede8;
          width: 250px;
          min-height: 100vh;
          padding: 1.5rem 0;
          border-right: 1px solid rgba(212, 175, 106, 0.15);
        }

        .sidebar-section {
          padding: 0 1.25rem;
        }

        .sidebar-divider {
          border: none;
          height: 1px;
          background: linear-gradient(90deg, transparent, #d4af6a, transparent);
          opacity: 0.25;
          margin: 1.25rem 0;
        }

        .sidebar-section-title {
          color: #d4af6a;
          font-size: 0.75rem;
          text-transform: uppercase;
          letter-spacing: 1.5px;
          font-weight: 600;
          margin: 0 0 0.75rem 0;
          padding: 0 0.5rem;
        }

        .sidebar-menu {
          list-style: none;
          padding: 0;
          margin: 0;
        }

        .sidebar-item {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          padding: 0.6rem 0.75rem;
          margin: 0.15rem 0;
          border-radius: 6px;
          cursor: pointer;
          transition: all 0.2s ease;
          font-size: 0.9rem;
        }

        .sidebar-item:hover {
          background: rgba(212, 175, 106, 0.08);
        }

        .sidebar-item.active {
          background: rgba(212, 175, 106, 0.15);
          border-left: 3px solid #d4af6a;
          font-weight: 500;
        }

        .sidebar-icon {
          color: #d4af6a;
          opacity: 0.7;
          font-size: 1.1rem;
          width: 20px;
          text-align: center;
        }

        .sidebar-item.active .sidebar-icon {
          opacity: 1;
        }

        .sidebar-label {
          color: #f0ede8;
        }
      `}</style>
    </aside>
  );
};

export default Sidebar;
