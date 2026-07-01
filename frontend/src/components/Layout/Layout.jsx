import '../../styles/hb.css';

const Layout = ({ children }) => {
  return (
    <div className="hb-page">
      <StatusBar />
      <TopBar />
      <div className="hb-page-header">
        <SearchBar />
        <div className="hb-page-header-right">
          <div className="user-info">
            <span className="user-avatar">👤</span>
            <span className="user-name">Admin</span>
          </div>
        </div>
      </div>
      <div className="hb-page-body">
        <aside className="sidebar">
          <nav>
            <ul>
              <li><a href="/dashboard">Dashboard</a></li>
              <li><a href="/productos">Productos</a></li>
              <li><a href="/ventas">Ventas</a></li>
              <li><a href="/clientes">Clientes</a></li>
              <li><a href="/reportes">Reportes</a></li>
            </ul>
          </nav>
        </aside>
        <main className="hb-page-content">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;

