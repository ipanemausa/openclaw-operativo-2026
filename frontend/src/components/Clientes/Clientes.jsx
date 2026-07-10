import React, { useState, useEffect } from "react";
import "../../styles/hb.css";

const Clientes = () => {
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api/hb/clientes")
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Error HTTP: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        setClientes(data.clientes || []);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="hb-page">
        <div className="hb-page-header">
          <h1 className="hb-page-title">Clientes</h1>
          <p className="hb-page-subtitle">Cargando datos...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="hb-page">
        <div className="hb-page-header">
          <h1 className="hb-page-title">Clientes</h1>
          <p className="hb-page-subtitle">Error: {error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <h1 className="hb-page-title">Clientes</h1>
        <p className="hb-page-subtitle">Listado de clientes registrados</p>
      </div>
      <div className="hb-table-wrap">
        <table className="hb-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Email</th>
              <th>Teléfono</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            {clientes.map((cliente) => (
              <tr key={cliente.id}>
                <td>{cliente.id}</td>
                <td>{cliente.nombre}</td>
                <td>{cliente.email}</td>
                <td>{cliente.telefono}</td>
                <td>
                  <span
                    className={`hb-badge ${
                      cliente.activo ? "hb-badge-green" : "hb-badge-red"
                    }`}
                  >
                    {cliente.activo ? "Activo" : "Inactivo"}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Clientes;
