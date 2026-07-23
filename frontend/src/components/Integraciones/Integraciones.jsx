import React, { useState, useEffect, useRef } from 'react'

const WA_API = 'http://localhost:3001'
const POLL_INTERVAL = 3000

export default function Integraciones() {
  const [status, setStatus] = useState('disconnected')
  const [qr, setQr] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const pollRef = useRef(null)
  const qrCanvasRef = useRef(null)

  const fetchStatus = async () => {
    try {
      const res = await fetch(`${WA_API}/api/whatsapp/status`)
      const data = await res.json()
      setStatus(data.status)
      setQr(data.qr || null)
      setError(null)
    } catch (e) {
      setError('Servicio WhatsApp no disponible — ¿está docker compose up?')
    }
  }

  useEffect(() => {
    fetchStatus()
    pollRef.current = setInterval(fetchStatus, POLL_INTERVAL)
    return () => clearInterval(pollRef.current)
  }, [])

  useEffect(() => {
    if (qr && qrCanvasRef.current && window.QRCode) {
      window.QRCode.toCanvas(qrCanvasRef.current, qr, { width: 200, margin: 2 })
    }
  }, [qr])

  const conectar = async () => {
    setLoading(true)
    try {
      await fetch(`${WA_API}/api/whatsapp/connect`, { method: 'POST' })
      await fetchStatus()
    } catch (e) {
      setError('No se pudo iniciar conexión')
    }
    setLoading(false)
  }

  const statusColors = { disconnected: '#6b6866', connecting: '#d4af6a', connected: '#34d399' }
  const statusLabels = {
    disconnected: '⚪ Desconectado',
    connecting: '🟡 Conectando — Escanea el QR',
    connected: '🟢 Conectado'
  }

  return (
    <div style={{ maxWidth: 680, margin: '0 auto', padding: '0 4px' }}>
      <div style={{ marginBottom: 24 }}>
        <h2 style={{ fontSize: 18, fontWeight: 600, color: '#f0ede8', margin: 0 }}>
          📲 Integración WhatsApp Business
        </h2>
        <p style={{ fontSize: 13, color: '#a09d99', margin: '4px 0 0' }}>
          Costo $0 · Baileys · +1 (954) 684-4445 · Respuestas IA automáticas
        </p>
      </div>

      {/* Status Banner */}
      <div style={{
        background: '#111', border: `1px solid ${statusColors[status]}40`,
        borderRadius: 12, padding: '14px 20px',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        marginBottom: 20, transition: 'border-color 0.3s'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{
            width: 10, height: 10, borderRadius: '50%',
            background: statusColors[status],
            boxShadow: status === 'connected' ? '0 0 8px #34d399' : 'none',
            animation: status === 'connecting' ? 'blink 1s ease-in-out infinite' : 'none'
          }} />
          <div>
            <div style={{ fontSize: 13, fontWeight: 500, color: '#f0ede8' }}>
              {statusLabels[status]}
            </div>
            <div style={{ fontSize: 11, color: '#6b6866', marginTop: 2 }}>
              Número: +1 (954) 684-4445 · Motor: Agente bilingüe HB Jewelry
            </div>
          </div>
        </div>
        {status !== 'connected' && (
          <button onClick={conectar} disabled={loading || status === 'connecting'} style={{
            background: 'linear-gradient(135deg, #25d366, #128c7e)',
            color: '#fff', border: 'none', borderRadius: 8,
            padding: '8px 18px', fontSize: 13, fontWeight: 600,
            cursor: loading ? 'wait' : 'pointer', opacity: status === 'connecting' ? 0.6 : 1
          }}>
            {loading ? 'Iniciando...' : '📲 Conectar'}
          </button>
        )}
        {status === 'connected' && (
          <div style={{
            background: 'rgba(52,211,153,0.12)', border: '1px solid rgba(52,211,153,0.3)',
            borderRadius: 8, padding: '6px 14px', fontSize: 12, color: '#34d399', fontWeight: 600
          }}>✓ Activo</div>
        )}
      </div>

      {/* QR Code */}
      {status === 'connecting' && qr && (
        <div style={{
          background: '#111', border: '1px solid rgba(212,175,106,0.3)',
          borderRadius: 12, padding: 24, marginBottom: 20, textAlign: 'center'
        }}>
          <div style={{ fontSize: 14, fontWeight: 600, color: '#d4af6a', marginBottom: 8 }}>
            📷 Escanea con WhatsApp Business
          </div>
          <div style={{ fontSize: 12, color: '#6b6866', marginBottom: 16 }}>
            WhatsApp → Dispositivos vinculados → Vincular dispositivo
          </div>
          <div style={{ display: 'inline-block', background: '#fff', borderRadius: 12, padding: 12 }}>
            <canvas ref={qrCanvasRef} width={200} height={200} />
          </div>
          <div style={{ fontSize: 11, color: '#6b6866', marginTop: 12 }}>
            QR se regenera automáticamente cada 60s
          </div>
        </div>
      )}

      {error && (
        <div style={{
          background: 'rgba(251,113,133,0.08)', border: '1px solid rgba(251,113,133,0.25)',
          borderRadius: 10, padding: '12px 16px', marginBottom: 16, fontSize: 13, color: '#fb7185'
        }}>⚠️ {error}</div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 12, marginBottom: 20 }}>
        {[
          { icon: '💬', title: 'Respuestas Automáticas', desc: 'Agente IA bilingüe responde clientes en ES/EN via Gateway OpenClaw' },
          { icon: '🔗', title: 'Agente Conectado', desc: 'bilingual_cs — HB Jewelry sales agent con contexto de productos' },
          { icon: '💰', title: 'Costo $0', desc: 'Baileys: protocolo WhatsApp Web libre. Sin Meta Business API.' },
          { icon: '🔄', title: 'Auto-Reconexión', desc: 'Reconecta automáticamente sin intervención manual' }
        ].map((card, i) => (
          <div key={i} style={{
            background: '#111', border: '1px solid rgba(255,255,255,0.07)',
            borderRadius: 12, padding: '14px 16px'
          }}>
            <div style={{ fontSize: 22, marginBottom: 8 }}>{card.icon}</div>
            <div style={{ fontSize: 13, fontWeight: 600, color: '#f0ede8', marginBottom: 6 }}>{card.title}</div>
            <div style={{ fontSize: 12, color: '#6b6866', lineHeight: 1.5 }}>{card.desc}</div>
          </div>
        ))}
      </div>

      {status === 'disconnected' && (
        <div style={{ background: '#111', border: '1px solid rgba(255,255,255,0.06)', borderRadius: 12, padding: 20 }}>
          <div style={{ fontSize: 13, fontWeight: 500, color: '#a09d99', marginBottom: 12 }}>
            ⚙️ Para activar WhatsApp:
          </div>
          <ol style={{ margin: 0, paddingLeft: 20, color: '#6b6866', fontSize: 13, lineHeight: 2 }}>
            <li>Asegúrate que el stack esté corriendo: <code style={{ background: '#1a1a1a', padding: '2px 6px', borderRadius: 4, color: '#d4af6a' }}>docker compose up -d</code></li>
            <li>Haz clic en <strong style={{ color: '#25d366' }}>📲 Conectar</strong></li>
            <li>Escanea el QR con WhatsApp Business del número <strong style={{ color: '#f0ede8' }}>+1 (954) 684-4445</strong></li>
            <li>¡Listo! El agente IA responderá automáticamente</li>
          </ol>
        </div>
      )}
      <style>{`@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }`}</style>
    </div>
  )
}
