import '../../styles/hb.css';

const Inventario = () => {
  const productos = [
    { id: 1, nombre: 'Anillo Diamante', precio: 4500, stock: 12, categoria: 'Anillos' },
    { id: 2, nombre: 'Collar Perla', precio: 3200, stock: 3, categoria: 'Collares' },
    { id: 3, nombre: 'Pendientes Rubí', precio: 2800, stock: 8, categoria: 'Pendientes' },
    { id: 4, nombre: 'Pulsera Oro', precio: 5600, stock: 2, categoria: 'Pulseras' },
    { id: 5, nombre: 'Anillo Zafiro', precio: 3900, stock: 6, categoria: 'Anillos' },
    { id: 6, nombre: 'Collar Esmeralda', precio: 7200, stock: 1, categoria: 'Collares' },
  ];

  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <h1 className="hb-page-title">Inventario</h1>
        <p className="hb-page-subtitle">Control de stock - HB Jewelry</p>
      </div>

      <div className="hb-table-wrap">
        <table className="hb-table">
          <thead>
            <tr>
              <th>Producto</th>
              <th>Categoría</th>
              <th>Precio</th>
              <th>Stock</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            {productos.map(producto => (
              <tr key={producto.id}>
                <td>{producto.nombre}</td>
                <td>{producto.categoria}</td>
                <td style={{ color: '#d4af6a', fontWeight: 'bold' }}>
                  ${producto.precio.toLocaleString()}
                </td>
                <td>{producto.stock}</td>
                <td>
                  {producto.stock < 5 ? (
                    <span className="hb-badge hb-badge-red">Stock bajo</span>
                  ) : (
                    <span className="hb-badge hb-badge-green">Disponible</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Inventario;


