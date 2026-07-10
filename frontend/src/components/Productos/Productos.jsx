import React, { useState, useEffect } from "react";
import "../../styles/hb.css";

const Productos = () => {
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProductos = async () => {
      try {
        const response = await fetch("/api/hb/productos");
        const data = await response.json();
        setProductos(data.productos || []);
      } catch (error) {
        console.error("Error al cargar productos:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProductos();
  }, []);

  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <h1 className="hb-page-title">Productos</h1>
        <p className="hb-page-subtitle">Listado de productos disponibles</p>
      </div>

      {loading ? (
        <div className="hb-page-subtitle">Cargando productos...</div>
      ) : (
        <div className="hb-table-wrap">
          <table className="hb-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Categoría</th>
                <th>Precio</th>
                <th>Stock</th>
              </tr>
            </thead>
            <tbody>
              {productos.map((producto) => (
                <tr key={producto.id}>
                  <td>{producto.id}</td>
                  <td>{producto.nombre}</td>
                  <td>{producto.categoria}</td>
                  <td>{producto.precio}</td>
                  <td>{producto.stock}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Productos;
