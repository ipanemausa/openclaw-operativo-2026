import React, { useState, useEffect } from "react";
import "../../styles/hb.css";

const Productos = () => {
  const [productos, setProductos] = useState([]);
  const [formData, setFormData] = useState({
    nombre: "",
    precio: "",
    categoria: "",
    talla: "",
    stock: ""
  });

  useEffect(() => {
    fetch("/api/hb/productos")
      .then((res) => res.json())
      .then((data) => setProductos(data))
      .catch((err) => console.error("Error al cargar productos", err));
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("/api/hb/productos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });
      if (res.ok) {
        const nuevoProducto = await res.json();
        setProductos([...productos, nuevoProducto]);
        setFormData({ nombre: "", precio: "", categoria: "", talla: "", stock: "" });
      }
    } catch (err) {
      console.error("Error al agregar producto", err);
    }
  };

  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <h1 className="hb-page-title">Productos HB Jewelry</h1>
        <p className="hb-page-subtitle">Administración de productos</p>
      </div>

      <form className="hb-form" onSubmit={handleSubmit}>
        <div className="hb-form-grid">
          <input
            className="hb-input"
            name="nombre"
            placeholder="Nombre"
            value={formData.nombre}
            onChange={handleChange}
            required
          />
          <input
            className="hb-input"
            name="precio"
            placeholder="Precio"
            type="number"
            step="0.01"
            value={formData.precio}
            onChange={handleChange}
            required
          />
          <select
            className="hb-select"
            name="categoria"
            value={formData.categoria}
            onChange={handleChange}
            required
          >
            <option value="">Categoría</option>
            <option value="anillos">Anillos</option>
            <option value="collares">Collares</option>
            <option value="pulseras">Pulseras</option>
            <option value="aretes">Aretes</option>
          </select>
          <input
            className="hb-input"
            name="talla"
            placeholder="Talla"
            value={formData.talla}
            onChange={handleChange}
            required
          />
          <input
            className="hb-input"
            name="stock"
            placeholder="Stock"
            type="number"
            value={formData.stock}
            onChange={handleChange}
            required
          />
        </div>
        <button className="hb-btn" type="submit">Agregar Producto</button>
      </form>

      <div className="hb-table-wrap">
        <table className="hb-table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Precio</th>
              <th>Categoría</th>
              <th>Talla</th>
              <th>Stock</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            {productos.map((prod, idx) => (
              <tr key={idx}>
                <td>{prod.nombre}</td>
                <td>${parseFloat(prod.precio).toFixed(2)}</td>
                <td>{prod.categoria}</td>
                <td>{prod.talla}</td>
                <td>{prod.stock}</td>
                <td>
                  <span className={prod.stock > 0 ? "hb-badge-green" : "hb-badge-red"}>
                    {prod.stock > 0 ? "Disponible" : "Agotado"}
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

export default Productos;