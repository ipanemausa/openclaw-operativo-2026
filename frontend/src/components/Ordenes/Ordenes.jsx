import React, { useState, useEffect } from 'react'
import '../../styles/hb.css'

const API = ''
const ESTADOS = ['Pendiente', 'Confirmado', 'En proceso', 'Enviado', 'Entregado', 'Cancelado']
const ESTADO_COLORS = {
  'Pendiente': '#fbbf24', 'Confirmado': '#60a5fa', 'En proceso': '#a78bfa',
  'Enviado': '#34d399', 'Entregado': '#4ade80', 'Cancelado': '#fb7185'
}
const CANALES = ['Instagram', 'WhatsApp', 'Shopify', 'TikTok', 'Tienda']

export default function Ordenes() {
  const [ordenes, setOrdenes] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [adding, setAdding] = useState(false)
  const [filtro, setFiltro] = useState('Todos')
  const [form, setForm] = useState({
    cliente: '', producto: '', cantidad: 1, precio: '',
    canal: 'Instagram', estado: 'Pendiente', notas: ''
  })

  useEffect(() => { loadOrdenes() }, [])

  async function loadOrdenes() {
    try {
      const r = await fetch(API + '/api/hb/ordenes')
      const d = await r.json()
      setOrdenes(d.ordenes || [])
    } catch(e) { console.error(e) }
    setLoading(false)
  }

  async function addOrden() {
    if (!form.cliente || !form.producto || !form.precio) return
    setAdding(true)
    try {
      const r = await fetch(API + '/api/hb/ordenes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form, cantidad: parseInt(form.cantidad), precio: parseFloat(form.precio) })
      })
      const d = await r.json()
      if (d.status === 'ok') {
        setForm({ cliente: '', producto: '', cantidad: 1, precio: '', canal: 'Instagram', estado: 'Pendiente', notas: '' })
        setShowForm(false)
        loadOrdenes()
      }
    } catch(e) { console.error(e) }
    setAdding(false)
  }

  async function updateEstado(id, estado) {
    try {
      await fetch(API + '/api/hb/ordenes/' + id, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ estado })
      })
      loadOrdenes()
    } catch(e) { console.error(e) }
  }

  const ordenesFiltradas = filtro === 'Todos' ? ordenes : ordenes.filter(o => o.estado === filtro)

  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <div>
          <div className="hb-page-title">Órdenes</div>
          <div className="hb-page-subtitle">{ordenes.length} órdenes totales</div>
        </div>
        <button className="hb-btn" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancelar' : '+ Nueva orden'}
        </button>
      </div>

      {showForm && (
        <div className="hb-form">
          <div className="hb-form-grid">
            <input className="hb-input" placeholder="Cliente *" value={form.cliente} onChange={e => setForm({...form, cliente: e.target.value})} />
            <input className="hb-input" placeholder="Producto *" value={form.producto} onChange={e => setForm({...form, producto: e.target.value})} />
            <input className="hb-input" placeholder="Precio *" type="number" value={form.precio} onChange={e => setForm({...form, precio: e.target.value})} />
            <input className="hb-input" placeholder="Cantidad" type="number" min="1" value={form.cantidad} onChange={e => setForm({...form, cantidad: e.target.value})} />
            <select className="hb-select" value={form.canal} onChange={e => setForm({...form, canal: e.target.value})}>
              {CANALES.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
            <select className="hb-select" value={form.estado} onChange={e => setForm({...form, estado: e.target.value})}>
              {ESTADOS.map(e => <option key={e} value={e}>{e}</option>)}
            </select>
          </div>
          <input className="hb-input" placeholder="Notas (opcional)" value={form.notas} onChange={e => setForm({...form, notas: e.target.value})} style={{marginBottom:'12px'}} />
          <button className="hb-btn hb-btn-sm" onClick={addOrden} disabled={adding}>
            {adding ? 'Guardando...' : 'Crear orden'}
          </button>
        </div>
      )}

      <div style={{display:'flex', gap:'8px', marginBottom:'16px', flexWrap:'wrap'}}>
        {['Todos', ...ESTADOS].map(e => (
          <button key={e} onClick={() => setFiltro(e)} className="hb-btn hb-btn-sm"
            style={{
              background: filtro === e ? 'rgba(212,175,106,0.15)' : 'transparent',
              borderColor: filtro === e ? '#d4af6a' : 'rgba(255,255,255,0.1)',
              color: filtro === e ? '#d4af6a' : '#a09d99',
              padding: '4px 12px'
            }}>
            {e}
          </button>
        ))}
      </div>

      {loading ? (
        <p className="hb-empty">Cargando órdenes...</p>
      ) : ordenesFiltradas.length === 0 ? (
        <p className="hb-empty">No hay órdenes {filtro !== 'Todos' ? 'con estado ' + filtro : 'registradas'}.</p>
      ) : (
        <div style={{display:'flex', flexDirection:'column', gap:'10px'}}>
          {ordenesFiltradas.map(o => (
            <div key={o.id} className="hb-card">
              <div className="hb-card-header" style={{marginBottom:'10px'}}>
                <div>
                  <div className="hb-card-name">{o.cliente}</div>
                  <div className="hb-card-meta" style={{marginTop:'2px'}}>{o.producto} · x{o.cantidad}</div>
                </div>
                <div style={{textAlign:'right'}}>
                  <div className="hb-card-price">${(parseFloat(o.precio) * parseInt(o.cantidad || 1)).toFixed(2)}</div>
                  <div className="hb-badge-gray" style={{fontSize:'11px',marginTop:'2px'}}>{o.fecha?.slice(0,10)}</div>
                </div>
              </div>
              <div style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
                <span className="hb-badge-gray">{o.canal}</span>
                <select value={o.estado} onChange={e => updateEstado(o.id, e.target.value)}
                  style={{
                    background: `${ESTADO_COLORS[o.estado]}15`,
                    border: `1px solid ${ESTADO_COLORS[o.estado]}40`,
                    borderRadius: '6px', padding: '3px 8px', fontSize: '12px',
                    color: ESTADO_COLORS[o.estado], fontFamily: 'inherit', cursor: 'pointer'
                  }}>
                  {ESTADOS.map(e => <option key={e} value={e}>{e}</option>)}
                </select>
              </div>
              {o.notas && <div className="hb-card-meta" style={{marginTop:'8px', paddingTop:'8px', borderTop:'1px solid rgba(255,255,255,0.04)'}}>{o.notas}</div>}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}






