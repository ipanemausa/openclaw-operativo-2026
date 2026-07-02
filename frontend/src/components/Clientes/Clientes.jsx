import "../../styles/hb.css";

const Clientes = () => {
  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <h1 className="hb-page-title">Clientes</h1>
        <p className="hb-page-subtitle">Gestión de clientes HB Jewelry</p>
      </div>
      <div className="hb-table-wrap">
        <table className="hb-table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Contacto</th>
              <th>Canal</th>
              <th>Historial de Compras</th>
              <th style={{ color: '#d4af6a' }}>Total Gastado</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>María García</td>
              <td>maria@email.com</td>
              <td>Instagram</td>
              <td>3 compras</td>
              <td style={{ color: '#d4af6a', fontWeight: 'bold' }}>$1,250.00</td>
            </tr>
            <tr>
              <td>Carlos López</td>
              <td>carlos@email.com</td>
              <td>WhatsApp</td>
              <td>5 compras</td>
              <td style={{ color: '#d4af6a', fontWeight: 'bold' }}>$3,480.00</td>
            </tr>
            <tr>
              <td>Ana Martínez</td>
              <td>ana@email.com</td>
              <td>Facebook</td>
              <td>2 compras</td>
              <td style={{ color: '#d4af6a', fontWeight: 'bold' }}>$890.00</td>
            </tr>
            <tr>
              <td>Pedro Sánchez</td>
              <td>pedro@email.com</td>
              <td>Tienda Física</td>
              <td>8 compras</td>
              <td style={{ color: '#d4af6a', fontWeight: 'bold' }}>$6,230.00</td>
            </tr>
            <tr>
              <td>Laura Torres</td>
              <td>laura@email.com</td>
              <td>Instagram</td>
              <td>1 compra</td>
              <td style={{ color: '#d4af6a', fontWeight: 'bold' }}>$450.00</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Clientes;





