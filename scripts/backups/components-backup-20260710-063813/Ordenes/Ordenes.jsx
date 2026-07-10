import React, { useState, useEffect } from "react";
import "../../styles/hb.css";

const Ordenes = () => {
  const [ordenes, setOrdenes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchOrdenes = async () => {
      try {
        const response = await fetch("/api/hb/ordenes");
        if (!response.ok) throw new Error("Error al cargar órdenes");
        const data = await response.json();
        setOrdenes(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchOrdenes();
  }, []);

  if (loading) return <div className="hb-page"><p>Cargando órdenes...</p></div>;
  if (error) return <div className="hb-page"><p>Error: {error}</p></div>;

  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <h1 className="hb-page-title">Órdenes</h1>
        <p className="hb-page-subtitle">Listado de órdenes de clientes</p>
      </div>

      <div className="hb-table-wrap">
        <table className="hb-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Cliente</th>
              <th>Producto</th>
              <th>Total</th>
              <th>Estado</th>
              <th>Fecha</th>
            </tr>
          </thead>
          <tbody>
            {ordenes.map((orden) => (
              <tr key={orden.id}>
                <td>{orden.id}</td>
                <td>{orden.cliente}</td>
                <td>{orden.producto}</td>
                <td>${orden.total?.toFixed(2)}</td>
                <td>
                  <span
                    className={`hb-badge ${
                      orden.estado === "completada"
                        ? "hb-badge-green"
                        : orden.estado === "cancelada"
                        ? "hb-badge-red"
                        : ""
                    }`}
                  >
                    {orden.estado}
                  </span>
                </td>
                <td>{new Date(orden.fecha).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Ordenes;