import '../../styles/hb.css';

const Header = () => {
  const [activeLink, setActiveLink] = React.useState('inicio');

  const navItems = ['Inicio', 'Catalogo', 'Promociones', 'Contacto'];

  return (
    <header className="hb-page-header" style={{ background: '#1a1a1a', borderBottom: '1px solid #d4af6a' }}>
      <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem 2rem' }}>
        <div className="logo" style={{ color: '#d4af6a', fontWeight: 'bold', fontSize: '1.5rem' }}>
          HB Jewelry
        </div>
        <nav style={{ display: 'flex', gap: '0.5rem' }}>
          {navItems.map((item) => (
            <button
              key={item}
              onClick={() => setActiveLink(item.toLowerCase())}
              className="hb-btn"
              style={{
                background: 'transparent',
                border: `1px solid ${activeLink === item.toLowerCase() ? '#d4af6a' : 'rgba(212, 175, 106, 0.4)'}`,
                color: '#f0ede8',
                padding: '0.5rem 1.2rem',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '0.9rem',
                transition: 'all 0.3s ease',
                boxShadow: activeLink === item.toLowerCase() ? '0 0 10px rgba(212, 175, 106, 0.3)' : 'none',
                fontWeight: activeLink === item.toLowerCase() ? '600' : '400'
              }}
              onMouseEnter={(e) => {
                e.target.style.borderColor = '#d4af6a';
                e.target.style.boxShadow = '0 0 8px rgba(212, 175, 106, 0.2)';
              }}
              onMouseLeave={(e) => {
                if (activeLink !== item.toLowerCase()) {
                  e.target.style.borderColor = 'rgba(212, 175, 106, 0.4)';
                  e.target.style.boxShadow = 'none';
                }
              }}
            >
              {item}
            </button>
          ))}
        </nav>
      </div>
    </header>
  );
};

export default Header;

