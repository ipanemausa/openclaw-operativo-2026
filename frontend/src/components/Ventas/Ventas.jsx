import React, { useState, useEffect } from "react";
import "../../styles/hb.css";

const Ventas = () => {
  const [ventas, setVentas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchVentas = async () => {
      try {
        const response = await fetch("/api/hb/ventas");
        const data = await response.json();
        setVentas(data.ventas || []);
      } catch (error) {
        console.error("Error al cargar ventas:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchVentas();
  }, []);

  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <h1 className="hb-page-title">Ventas</h1>
        <p className="hb-page-subtitle">Historial de ventas registradas</p>
      </div>

      {loading ? (
        <div className="hb-page-subtitle">Cargando ventas...</div>
      ) : (
        <div className="hb-table-wrap">
          <table className="hb-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Producto</th>
                <th>Cliente</th>
                <th>Fecha</th>
                <th>Total</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              {ventas.map((venta) => (
                <tr key={venta.id}>
                  <td>{venta.id}</td>
                  <td>{venta.producto}</td>
                  <td>{venta.cliente}</td>
                  <td>{venta.fecha}</td>
                  <td>{venta.total}</td>
                  <td>
                    {venta.estado === "completada" ? (
                      <span className="hb-badge hb-badge-green">Completada</span>
                    ) : (
                      <span className="hb-badge hb-badge-red">Pendiente</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Ventas;

