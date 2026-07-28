import React, { useState, useRef, useEffect, useCallback, memo } from 'react'

// ─── CLOUD-FIRST ─────────────────────────────────────────────────────────────
const CLOUD_BASE = 'https://hb-jewelry-app.web.app'
const IS_PROD = window.location.hostname !== 'localhost'
const asset = (f) => IS_PROD ? `${CLOUD_BASE}/${f}` : `/${f}`

// ─── AVATARES OFICIALES GUILLERMO AI (Basados en avatar_pro.png auténtico) ──────
const AVATARS = [
  { id: 'guillermo_main', name: 'Guillermo — Principal', style: 'Avatar Oficial · HB Master', img: asset('avatar_pro.png'), accent: '#d4af6a', badge: '👑', badgeBg: '#b45309' },
  { id: 'studio',          name: 'Guillermo — Studio',    style: 'Presentador · Micrófono Pro', img: asset('avatar_pro.png'), accent: '#fbbf24', badge: '🎙️', badgeBg: '#7c3aed' },
  { id: 'casual',          name: 'Guillermo — Casual',    style: 'Confiado · Explicativo',     img: asset('avatar_pro.png'), accent: '#60a5fa', badge: '👔', badgeBg: '#1d4ed8' },
  { id: 'executive',       name: 'Guillermo — Ejecutivos',style: 'Corporativo · HB Gold',      img: asset('avatar_pro.png'), accent: '#e2e8f0', badge: '💼', badgeBg: '#374151' },
  { id: 'tech',            name: 'Guillermo — Técnico',   style: 'Demostración · AI Engine',   img: asset('avatar_pro.png'), accent: '#34d399', badge: '⚡', badgeBg: '#059669' },
  { id: 'showcase',        name: 'Guillermo — Showcase',  style: 'Joyería · Colección VIP',    img: asset('avatar_pro.png'), accent: '#f87171', badge: '💎', badgeBg: '#b91c1c' },
]

// ─── 4 VIDEOS ────────────────────────────────────────────────────────────────
const VIDEOS = [
  { id: 'tutorial',  src: asset('hb_tutorial_narrado_v1.mp4'),    title: 'Tutorial App',           tag: '📹', tagBg: '#7c3aed', accent: '#a78bfa', dur: '1:16',  vert: true },
  { id: 'qa',        src: asset('output_avatar_english_7qa.mp4'), title: 'Demo Técnico 7 Q&A',     tag: '🛠️', tagBg: '#059669', accent: '#34d399', dur: '0:15',  vert: true },
  { id: 'showcase',  src: asset('final_showcase.mp4'),            title: 'Showcase HB Jewelry',    tag: '💎', tagBg: '#b45309', accent: '#fbbf24', dur: '~30s',  vert: false },
  { id: 'avatar',    src: asset('avatar_base.mp4'),               title: 'Avatar Base Loop',       tag: '🤖', tagBg: '#6b7280', accent: '#d4af6a', dur: '0:15',  vert: true },
]

/* ═══════════════════════════════════════════════════════════════════════════
   SECTION HEADER — compacto, limpio, full-width
   ═══════════════════════════════════════════════════════════════════════════ */
const SectionHead = ({ icon, title, sub }) => (
  <div style={{ display:'flex', justifyContent:'space-between', alignItems:'baseline', marginBottom:10, paddingBottom:6, borderBottom:'1px solid rgba(212,175,106,0.18)' }}>
    <span style={{ color:'#d4af6a', fontWeight:700, fontSize:13 }}>{icon} {title}</span>
    {sub && <span style={{ color:'#555', fontSize:11 }}>{sub}</span>}
  </div>
)

/* ═══════════════════════════════════════════════════════════════════════════
   AVATAR CARD — imagen real, full-width, sin filtros
   ═══════════════════════════════════════════════════════════════════════════ */
const AvatarCard = memo(({ av, onClick }) => {
  const [h, setH] = useState(false)
  const isMaster = av.id === 'guillermo_main'
  return (
    <div
      onClick={() => onClick(av)}
      onMouseEnter={() => setH(true)} onMouseLeave={() => setH(false)}
      style={{
        cursor:'pointer', borderRadius:12, overflow:'hidden', position:'relative',
        background:'#0a0a0a',
        border: isMaster ? '2px solid #d4af6a' : `1px solid ${h ? av.accent+'88' : 'rgba(255,255,255,0.06)'}`,
        transition:'all .22s ease',
        transform: h ? 'translateY(-4px)' : 'none',
        boxShadow: isMaster
          ? (h ? '0 16px 40px rgba(212,175,106,0.5)' : '0 4px 20px rgba(212,175,106,0.25)')
          : (h ? `0 12px 32px ${av.accent}30` : '0 2px 8px rgba(0,0,0,0.5)'),
      }}
    >
      {/* Thumbnail 16:9 estilo YouTube */}
      <div style={{ width:'100%', paddingTop:'56.25%', position:'relative', overflow:'hidden', background:'#000' }}>
        <img src={av.img} alt={av.name} loading="lazy"
          style={{ position:'absolute', inset:0, width:'100%', height:'100%', objectFit:'cover', objectPosition:'center 20%', display:'block', transition:'transform .3s', transform: h ? 'scale(1.04)' : 'scale(1)' }} />
      </div>
      {/* Badge */}
      <div style={{ position:'absolute', top:8, left:8, background:av.badgeBg, color:'#fff', padding:'2px 8px', borderRadius:20, fontSize:10, fontWeight:800 }}>
        {av.badge} {isMaster ? 'AVATAR MASTER' : av.id.toUpperCase()}
      </div>
      {/* Info inferior */}
      <div style={{ padding:'10px 10px 12px', background: isMaster ? 'linear-gradient(180deg, #141008 0%, #0a0a0a 100%)' : '#0a0a0a' }}>
        <div style={{ color: isMaster ? '#d4af6a' : '#fff', fontWeight:700, fontSize:12, marginBottom:2 }}>{av.name}</div>
        <div style={{ color: av.accent, fontSize:10, fontWeight:600 }}>{av.style}</div>
      </div>
      {/* Hover eye */}
      {h && <div style={{ position:'absolute', inset:0, display:'flex', alignItems:'center', justifyContent:'center', background:'rgba(0,0,0,0.35)', pointerEvents:'none' }}>
        <div style={{ width:48, height:48, borderRadius:'50%', background:'rgba(255,255,255,0.92)', display:'flex', alignItems:'center', justifyContent:'center', fontSize:20, boxShadow:'0 4px 16px rgba(0,0,0,0.4)' }}>👁️</div>
      </div>}
    </div>
  )
})

/* ═══════════════════════════════════════════════════════════════════════════
   AVATAR MODAL — fullscreen
   ═══════════════════════════════════════════════════════════════════════════ */
const AvatarModal = ({ av, onClose }) => {
  useEffect(() => { const h=e=>{if(e.key==='Escape')onClose()}; window.addEventListener('keydown',h); return ()=>window.removeEventListener('keydown',h) }, [onClose])
  return (
    <div id="av-modal-bg" onClick={e=>e.target.id==='av-modal-bg'&&onClose()}
      style={{ position:'fixed', inset:0, zIndex:9999, background:'rgba(0,0,0,0.94)', backdropFilter:'blur(10px)', display:'flex', alignItems:'center', justifyContent:'center', padding:20, animation:'fadeIn .2s ease' }}>
      <div style={{ position:'relative', maxWidth:800, width:'100%', borderRadius:20, overflow:'hidden', background:'#0a0a0a', border:`2px solid ${av.accent}55`, boxShadow:`0 24px 60px ${av.accent}30` }}>
        <button onClick={onClose} style={{ position:'absolute', top:12, right:12, zIndex:10, width:34, height:34, borderRadius:'50%', background:'rgba(0,0,0,0.7)', border:'1px solid rgba(255,255,255,0.2)', color:'#fff', fontSize:16, cursor:'pointer', display:'flex', alignItems:'center', justifyContent:'center' }}>✕</button>
        <img src={av.img} alt={av.name} style={{ width:'100%', aspectRatio:'16/9', objectFit:'cover', objectPosition:'center 20%', display:'block', background:'#000' }} />
        <div style={{ padding:'14px 18px 18px', borderTop:`1px solid ${av.accent}33` }}>
          <div style={{ display:'flex', gap:8, alignItems:'center', marginBottom:6 }}>
            <span style={{ background:av.badgeBg, color:'#fff', padding:'3px 10px', borderRadius:20, fontSize:11, fontWeight:800 }}>{av.badge} {av.id.toUpperCase()}</span>
          </div>
          <div style={{ color:'#fff', fontWeight:800, fontSize:18 }}>Guillermo AI — {av.name}</div>
          <div style={{ color:av.accent, fontSize:13, marginTop:2 }}>{av.style}</div>
          <div style={{ color:'#444', fontSize:11, marginTop:8 }}>ESC o clic fuera para cerrar</div>
        </div>
      </div>
    </div>
  )
}

/* ═══════════════════════════════════════════════════════════════════════════
   VIDEO CARD — miniatura real del video
   ═══════════════════════════════════════════════════════════════════════════ */
const VidCard = memo(({ v, onClick }) => {
  const [h, setH] = useState(false)
  const ref = useRef(null)
  const [loaded, setLoaded] = useState(false)
  useEffect(() => { const el=ref.current; if(!el)return; el.currentTime=0.1; el.addEventListener('loadeddata',()=>setLoaded(true),{once:true}) }, [])
  return (
    <div onClick={()=>onClick(v)} onMouseEnter={()=>setH(true)} onMouseLeave={()=>setH(false)}
      style={{ cursor:'pointer', borderRadius:12, overflow:'hidden', background:'#0a0a0a', border:`1px solid ${h?v.accent+'66':'rgba(255,255,255,0.06)'}`, transition:'all .22s ease', transform:h?'translateY(-3px)':'none', boxShadow:h?`0 8px 24px ${v.accent}22`:'0 2px 8px rgba(0,0,0,0.4)' }}>
      <div style={{ position:'relative', paddingTop:'56.25%', background:'#000' }}>
        <video ref={ref} src={v.src} muted preload="metadata" playsInline style={{ position:'absolute', inset:0, width:'100%', height:'100%', objectFit:v.vert?'contain':'cover', opacity:loaded?1:0, transition:'opacity .3s' }} />
        {!loaded && <div style={{ position:'absolute', inset:0, display:'flex', alignItems:'center', justifyContent:'center' }}><div style={{ width:24, height:24, border:`2px solid ${v.accent}`, borderTopColor:'transparent', borderRadius:'50%', animation:'spin 1s linear infinite' }} /></div>}
        {h && <div style={{ position:'absolute', inset:0, background:'rgba(0,0,0,0.4)', display:'flex', alignItems:'center', justifyContent:'center' }}><div style={{ width:40, height:40, borderRadius:'50%', background:'rgba(255,255,255,0.92)', display:'flex', alignItems:'center', justifyContent:'center' }}><div style={{ width:0, height:0, borderStyle:'solid', borderWidth:'8px 0 8px 14px', borderColor:'transparent transparent transparent #111', marginLeft:3 }}/></div></div>}
        <div style={{ position:'absolute', top:6, left:6, background:v.tagBg, color:'#fff', padding:'2px 7px', borderRadius:20, fontSize:9, fontWeight:800 }}>{v.tag}</div>
        <div style={{ position:'absolute', bottom:5, right:5, background:'rgba(0,0,0,0.85)', color:'#fff', padding:'1px 6px', borderRadius:3, fontSize:10, fontWeight:700 }}>{v.dur}</div>
      </div>
      <div style={{ padding:'8px 10px 10px' }}>
        <div style={{ color:'#fff', fontWeight:700, fontSize:11, lineHeight:'1.3' }}>{v.title}</div>
      </div>
    </div>
  )
})

/* ═══════════════════════════════════════════════════════════════════════════
   VIDEO MODAL
   ═══════════════════════════════════════════════════════════════════════════ */
const VidModal = ({ v, onClose }) => {
  const ref = useRef(null)
  const [snd, setSnd] = useState(false)
  useEffect(() => { const h=e=>{if(e.key==='Escape')onClose()}; window.addEventListener('keydown',h); return ()=>window.removeEventListener('keydown',h) }, [onClose])
  useEffect(() => { const el=ref.current; if(el){el.muted=true; el.play().catch(()=>{})} }, [])
  const unlock = () => { const el=ref.current; if(el){el.muted=false; setSnd(true); el.play().catch(()=>{})} }
  return (
    <div id="vid-modal-bg" onClick={e=>e.target.id==='vid-modal-bg'&&onClose()}
      style={{ position:'fixed', inset:0, zIndex:9999, background:'rgba(0,0,0,0.94)', backdropFilter:'blur(10px)', display:'flex', alignItems:'center', justifyContent:'center', padding:20, animation:'fadeIn .2s ease' }}>
      <div style={{ position:'relative', width:'100%', maxWidth:v.vert?400:1000, borderRadius:16, overflow:'hidden', background:'#000', boxShadow:'0 24px 60px rgba(0,0,0,0.8)' }}>
        <button onClick={onClose} style={{ position:'absolute', top:10, right:10, zIndex:10, width:32, height:32, borderRadius:'50%', background:'rgba(0,0,0,0.7)', border:'1px solid rgba(255,255,255,0.2)', color:'#fff', fontSize:15, cursor:'pointer', display:'flex', alignItems:'center', justifyContent:'center' }}>✕</button>
        {!snd && <div onClick={unlock} style={{ position:'absolute', inset:0, zIndex:8, cursor:'pointer', display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center', background:'rgba(0,0,0,0.55)' }}>
          <div style={{ fontSize:40, marginBottom:6 }}>🔊</div>
          <div style={{ color:'#fff', fontWeight:800, fontSize:15 }}>Clic para sonido</div>
        </div>}
        <video ref={ref} src={v.src} muted playsInline controls autoPlay style={{ width:'100%', maxHeight:'85vh', display:'block', objectFit:'contain', background:'#000' }} />
        <div style={{ padding:'8px 12px', background:'rgba(0,0,0,0.9)', borderTop:'1px solid rgba(255,255,255,0.06)' }}>
          <div style={{ color:'#fff', fontWeight:700, fontSize:12 }}>{v.title} · {v.dur}</div>
        </div>
      </div>
    </div>
  )
}

/* ═══════════════════════════════════════════════════════════════════════════
   STATS PANEL (limpio)
   ═══════════════════════════════════════════════════════════════════════════ */
const Stats = ({ stack, tareas, gateway }) => {
  const ec = s => ({ completada:'#4ade80', pendiente:'#fbbf24', en_cola:'#60a5fa', ejecutando:'#fb923c' }[s]||'#888')
  const card = { background:'rgba(255,255,255,0.03)', border:'1px solid rgba(212,175,106,0.12)', borderRadius:10, padding:14 }
  return (
    <div style={{ display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:12 }}>
      <div style={card}>
        <div style={{ color:'#d4af6a', fontSize:10, letterSpacing:2, fontWeight:700, marginBottom:10 }}>CONTENEDORES</div>
        {stack.map(c => <div key={c.name} style={{ display:'flex', justifyContent:'space-between', padding:'4px 0', borderBottom:'1px solid rgba(255,255,255,0.03)', fontSize:11 }}>
          <span><span style={{ width:6, height:6, borderRadius:'50%', background:c.status==='running'?'#4ade80':'#fb7185', display:'inline-block', marginRight:5 }}/>{c.name}</span>
          <span style={{ color:c.status==='running'?'#4ade80':'#fb7185', fontSize:10 }}>{c.status}</span>
        </div>)}
      </div>
      <div style={card}>
        <div style={{ color:'#d4af6a', fontSize:10, letterSpacing:2, fontWeight:700, marginBottom:10 }}>GATEWAY</div>
        <div style={{ display:'flex', justifyContent:'space-between', padding:'4px 0', fontSize:11, marginBottom:4 }}><span>estado</span><span style={{ color:gateway.status==='ok'?'#4ade80':'#fb7185' }}>{gateway.status||'—'}</span></div>
        {(gateway.agents||[]).map(a => <div key={a} style={{ display:'flex', justifyContent:'space-between', padding:'4px 0', borderBottom:'1px solid rgba(255,255,255,0.03)', fontSize:11 }}><span style={{ color:'#d4af6a' }}>{a}</span><span style={{ color:'#4ade80', fontSize:10 }}>activo</span></div>)}
      </div>
      <div style={card}>
        <div style={{ color:'#d4af6a', fontSize:10, letterSpacing:2, fontWeight:700, marginBottom:10 }}>DAG TAREAS</div>
        {Object.entries(tareas).map(([k,v]) => <div key={k} style={{ display:'flex', justifyContent:'space-between', padding:'4px 0', borderBottom:'1px solid rgba(255,255,255,0.03)', fontSize:11 }}>
          <span style={{ color:'#ccc' }}>{k.replace(/_/g,' ')}</span>
          <span style={{ fontSize:9, padding:'2px 7px', borderRadius:4, color:ec(v.estado), border:`1px solid ${ec(v.estado)}33`, background:`${ec(v.estado)}15` }}>{v.estado}</span>
        </div>)}
      </div>
    </div>
  )
}

/* ═══════════════════════════════════════════════════════════════════════════
   DASHBOARD PRINCIPAL — full-width, scroll interno por sección
   ═══════════════════════════════════════════════════════════════════════════ */
export default function Dashboard({ onNavigate }) {
  const [stack, setStack]   = useState([])
  const [tareas, setTareas] = useState({})
  const [gateway, setGateway] = useState({})
  const [loading, setLoading] = useState(true)
  const [avModal, setAvModal] = useState(null)
  const [vidModal, setVidModal] = useState(null)

  useEffect(() => {
    async function load() {
      const [s,t,g] = await Promise.allSettled([
        fetch('/stack').then(r=>r.json()).catch(()=>({ containers:[{name:'gateway',status:'running'},{name:'orchestrator',status:'running'},{name:'deepfake_node',status:'running'},{name:'rag_worker',status:'running'}] })),
        fetch('/api/tareas').then(r=>r.json()).catch(()=>({ tareas:{sincronizacion_rclone:{estado:'completada'},vectorizacion_rag:{estado:'completada'},inferencia_v2v:{estado:'ejecutando'}} })),
        fetch('/api/mcp/status').then(r=>r.json()).catch(()=>({ status:'ok', agents:['Omnilingual Voice','Deepfake V2V','Financial RAG'] })),
      ])
      if(s.status==='fulfilled') setStack(s.value.containers||[])
      if(t.status==='fulfilled') setTareas(t.value.tareas||{})
      if(g.status==='fulfilled') setGateway(g.value)
      setLoading(false)
    }
    load(); const iv=setInterval(load,10000); return ()=>clearInterval(iv)
  }, [])

  if (loading) return <div style={{ padding:'2rem', color:'#d4af6a', fontSize:14 }}>⚙️ Cargando…</div>

  return (
    <div style={{ padding:'12px 16px', width:'100%', boxSizing:'border-box' }}>

      {/* HEADER — full-width */}
      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:16, paddingBottom:10, borderBottom:'1px solid rgba(212,175,106,0.2)' }}>
        <div>
          <h1 style={{ margin:0, color:'#d4af6a', fontSize:18, fontWeight:800 }}>💎 HB Jewelry — Dashboard</h1>
          <span style={{ color:'#555', fontSize:11 }}>Auto-refresh 10s · Cloud-First</span>
        </div>
        <div style={{ display:'flex', alignItems:'center', gap:5, background:'rgba(52,211,153,0.08)', border:'1px solid rgba(52,211,153,0.25)', borderRadius:20, padding:'4px 12px' }}>
          <div style={{ width:7, height:7, borderRadius:'50%', background:'#34d399', animation:'pulse-d 2s infinite' }} />
          <span style={{ color:'#34d399', fontSize:11, fontWeight:700 }}>{IS_PROD ? 'Firebase' : 'Dev'}</span>
        </div>
      </div>

      {/* ══════════════ AVATAR SECTION — scroll interno ══════════════ */}
      <div style={{ marginBottom:20 }}>
        <SectionHead icon="👤" title="Avatar Personal — Guillermo AI" sub="6 variantes · Clic para ver en grande" />
        <div id="av-shelf" style={{
          display:'grid', gridTemplateColumns:'repeat(auto-fill, minmax(280px, 1fr))', gap:14,
          maxHeight:440, overflowY:'auto', overflowX:'hidden',
          paddingRight:4, scrollbarWidth:'thin', scrollbarColor:'#d4af6a44 transparent',
        }}>
          {AVATARS.map(av => <AvatarCard key={av.id} av={av} onClick={setAvModal} />)}
        </div>
      </div>

      {/* ══════════════ VIDEO SECTION — scroll interno ══════════════ */}
      <div style={{ marginBottom:20 }}>
        <SectionHead icon="🎬" title="Videos HB Jewelry" sub="4 videos · Clic para reproducir" />
        <div id="vid-shelf" style={{
          display:'grid', gridTemplateColumns:'repeat(auto-fill, minmax(280px, 1fr))', gap:14,
          maxHeight:440, overflowY:'auto', overflowX:'hidden',
          paddingRight:4, scrollbarWidth:'thin', scrollbarColor:'#d4af6a44 transparent',
        }}>
          {VIDEOS.map(v => <VidCard key={v.id} v={v} onClick={setVidModal} />)}
        </div>
      </div>

      {/* ══════════════ STATS — full-width ══════════════ */}
      <div style={{ marginBottom:16 }}>
        <SectionHead icon="📊" title="Estado del Sistema" />
        <Stats stack={stack} tareas={tareas} gateway={gateway} />
      </div>

      {/* ACCIONES RÁPIDAS */}
      <div style={{ display:'flex', gap:8, flexWrap:'wrap', paddingTop:12, borderTop:'1px solid rgba(255,255,255,0.04)' }}>
        {[['➕ Producto','productos'],['📦 Pedidos','ordenes'],['📈 Reportes','reportes'],['🤖 Avatar AI','avatar-meet'],['📊 Analytics','analytics']].map(([l,s])=>(
          <button key={s} onClick={()=>onNavigate&&onNavigate(s)}
            style={{ background:'rgba(212,175,106,0.06)', border:'1px solid rgba(212,175,106,0.25)', color:'#d4af6a', padding:'6px 14px', borderRadius:8, fontSize:11, fontWeight:600, cursor:'pointer' }}>{l}</button>
        ))}
      </div>

      {/* MODALES */}
      {avModal && <AvatarModal av={avModal} onClose={()=>setAvModal(null)} />}
      {vidModal && <VidModal v={vidModal} onClose={()=>setVidModal(null)} />}

      {/* CSS */}
      <style>{`
        @keyframes fadeIn { from{opacity:0;transform:scale(.97)} to{opacity:1;transform:scale(1)} }
        @keyframes spin { to{transform:rotate(360deg)} }
        @keyframes pulse-d { 0%,100%{opacity:1} 50%{opacity:.4} }
        #av-shelf::-webkit-scrollbar, #vid-shelf::-webkit-scrollbar { width:5px }
        #av-shelf::-webkit-scrollbar-track, #vid-shelf::-webkit-scrollbar-track { background:transparent }
        #av-shelf::-webkit-scrollbar-thumb, #vid-shelf::-webkit-scrollbar-thumb { background:#d4af6a44; border-radius:3px }
        #av-shelf::-webkit-scrollbar-thumb:hover, #vid-shelf::-webkit-scrollbar-thumb:hover { background:#d4af6a }
      `}</style>
    </div>
  )
}
