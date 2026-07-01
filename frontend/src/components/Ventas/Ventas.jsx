import React, { useState, useEffect } from 'react'
import '../../../styles/hb.css'

const API = ''
const CANALES = ['Instagram', 'WhatsApp', 'Shopify', 'TikTok', 'Tienda']
const CANAL_COLORS = {
  Instagram: '#a78bfa', WhatsApp: '#4ade80', Shopify: '#34d399',
  TikTok: '#fb7185', Tienda: '#60a5fa'
}

export default function Ventas() {
  const [ventas, setVentas] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [adding, setAdding] = useState(false)
  const [form, setForm] = useState({ producto: '', cantidad: 1, precio: '', cliente: '', canal: 'Instagram' })

  useEffect(() => { loadVentas() }, [])

  async function loadVentas() {
    try {
      const r = await fetch(API + '/api/hb/ventas')
      const d = await r.json()
      setVentas(d.ventas || [])
    } catch(e) { console.error(e) }
    setLoading(false)
  }

  async function addVenta() {
    if (!form.producto || !form.precio || !form.cliente) return
    setAdding(true)
    try {
      const r = await fetch(API + '/api/hb/ventas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form, cantidad: parseInt(form.cantidad), precio: parseFloat(form.precio) })
      })
      const d = await r.json()
      if (d.status === 'ok') {
        setForm({ producto: '', cantidad: 1, precio: '', cliente: '', canal: 'Instagram' })
        setShowForm(false)
        loadVentas()
      }
    } catch(e) { console.error(e) }
    setAdding(false)
  }

  const totalVentas = ventas.reduce((a, v) => a + (parseFloat(v.precio) * parseInt(v.cantidad || 1)), 0)
  const total = (parseFloat(form.precio) || 0) * (parseInt(form.cantidad) || 0)

  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <div>
          <div className="hb-page-title">Ventas</div>
          <div className="hb-page-subtitle">
            {ventas.length} ventas · Total: <span style={{color:'#d4af6a',fontWeight:'600'}}>${totalVentas.toFixed(2)}</span>
          </div>
        </div>
        <button className="hb-btn" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancelar' : '+ Registrar venta'}
        </button>
      </div>

      {showForm && (
        <div className="hb-form">
          <div className="hb-form-grid">
            <input className="hb-input" placeholder="Producto *" value={form.producto} onChange={e => setForm({...form, producto: e.target.value})} />
            <input className="hb-input" placeholder="Cliente *" value={form.cliente} onChange={e => setForm({...form, cliente: e.target.value})} />
            <input className="hb-input" placeholder="Precio *" type="number" value={form.precio} onChange={e => setForm({...form, precio: e.target.value})} />
            <input className="hb-input" placeholder="Cantidad" type="number" min="1" value={form.cantidad} onChange={e => setForm({...form, cantidad: e.target.value})} />
            <select className="hb-select" value={form.canal} onChange={e => setForm({...form, canal: e.target.value})}>
              {CANALES.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          {total > 0 && <div className="hb-total">Total: ${total.toFixed(2)}</div>}
          <button className="hb-btn hb-btn-sm" onClick={addVenta} disabled={adding}>
            {adding ? 'Guardando...' : 'Registrar venta'}
          </button>
        </div>
      )}

      {loading ? (
        <p className="hb-empty">Cargando ventas...</p>
      ) : ventas.length === 0 ? (
        <p className="hb-empty">No hay ventas registradas.</p>
      ) : (
        <div className="hb-table-wrap">
          <table className="hb-table">
            <thead>
              <tr>
                <th>Producto</th>
                <th>Cliente</th>
                <th>Total</th>
                <th>Canal</th>
                <th>Fecha</th>
              </tr>
            </thead>
            <tbody>
              {ventas.map(v => (
                <tr key={v.id}>
                  <td className="td-main">{v.producto}</td>
                  <td className="td-muted">{v.cliente}</td>
                  <td className="td-gold">${(parseFloat(v.precio) * parseInt(v.cantidad || 1)).toFixed(2)}</td>
                  <td>
                    <span className="hb-canal" style={{
                      background: `${CANAL_COLORS[v.canal] || '#a09d99'}20`,
                      color: CANAL_COLORS[v.canal] || '#a09d99'
                    }}>{v.canal}</span>
                  </td>
                  <td className="td-dim">{v.fecha?.slice(0,10)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}




