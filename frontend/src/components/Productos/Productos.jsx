import React, { useState, useEffect } from 'react'
import '../../styles/hb.css'

const API = ''
const CATEGORIAS = ['Collares', 'Aretes', 'Pulseras', 'Anillos', 'Sets']
const CANALES = ['Instagram', 'WhatsApp', 'Shopify', 'TikTok', 'Tienda']

export default function Productos() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [adding, setAdding] = useState(false)
  const [form, setForm] = useState({ nombre: '', categoria: '', material: '', precio: '', stock: '', descripcion: '' })

  useEffect(() => { loadProducts() }, [])

  async function loadProducts() {
    try {
      const r = await fetch(API + '/api/hb/productos')
      const d = await r.json()
      setProducts(d.productos || [])
    } catch(e) { console.error(e) }
    setLoading(false)
  }

  async function addProduct() {
    if (!form.nombre || !form.precio) return
    setAdding(true)
    try {
      const r = await fetch(API + '/api/hb/productos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form, precio: parseFloat(form.precio), stock: parseInt(form.stock) || 0 })
      })
      const d = await r.json()
      if (d.status === 'ok') {
        setForm({ nombre: '', categoria: '', material: '', precio: '', stock: '', descripcion: '' })
        setShowForm(false)
        loadProducts()
      }
    } catch(e) { console.error(e) }
    setAdding(false)
  }

  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <div>
          <div className="hb-page-title">Catálogo de productos</div>
          <div className="hb-page-subtitle">{products.length} productos activos</div>
        </div>
        <button className="hb-btn" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancelar' : '+ Agregar producto'}
        </button>
      </div>

      {showForm && (
        <div className="hb-form">
          <div className="hb-form-grid">
            <input className="hb-input" placeholder="Nombre *" value={form.nombre} onChange={e => setForm({...form, nombre: e.target.value})} />
            <select className="hb-select" value={form.categoria} onChange={e => setForm({...form, categoria: e.target.value})}>
              <option value="">Categoría</option>
              {CATEGORIAS.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
            <input className="hb-input" placeholder="Material" value={form.material} onChange={e => setForm({...form, material: e.target.value})} />
            <input className="hb-input" placeholder="Precio *" type="number" value={form.precio} onChange={e => setForm({...form, precio: e.target.value})} />
            <input className="hb-input" placeholder="Stock" type="number" value={form.stock} onChange={e => setForm({...form, stock: e.target.value})} />
            <input className="hb-input" placeholder="Descripción" value={form.descripcion} onChange={e => setForm({...form, descripcion: e.target.value})} />
          </div>
          <button className="hb-btn hb-btn-sm" onClick={addProduct} disabled={adding}>
            {adding ? 'Guardando...' : 'Guardar producto'}
          </button>
        </div>
      )}

      {loading ? (
        <p className="hb-empty">Cargando productos...</p>
      ) : products.length === 0 ? (
        <p className="hb-empty">No hay productos registrados.</p>
      ) : (
        <div className="hb-grid">
          {products.map(p => (
            <div key={p.id} className="hb-card">
              <div className="hb-card-header">
                <div className="hb-card-name">{p.nombre}</div>
                <div className="hb-card-price">${parseFloat(p.precio).toFixed(2)}</div>
              </div>
              <div className="hb-card-meta">{p.categoria}{p.material ? ` · ${p.material}` : ''}</div>
              {p.descripcion && <div className="hb-card-meta">{p.descripcion}</div>}
              <div className="hb-card-footer">
                <span className={`hb-badge ${parseInt(p.stock) < 6 ? 'hb-badge-red' : 'hb-badge-green'}`}>
                  Stock: {p.stock}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}



