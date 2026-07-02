import React from 'react'
import '../../styles/hb.css'

export default function Header() {
  return (
    <header style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'0 1.5rem',height:'56px',background:'#111',borderBottom:'1px solid rgba(212,175,106,0.15)',flexShrink:0}}>
      <div style={{color:'#d4af6a',fontWeight:'700',fontSize:'18px'}}>HB Jewelry</div>
      <div style={{display:'flex',alignItems:'center',gap:'8px'}}>
        <span style={{width:'8px',height:'8px',borderRadius:'50%',background:'#4ade80',display:'inline-block'}}></span>
        <span style={{color:'#4ade80',fontSize:'13px'}}>Sistema operativo</span>
      </div>
    </header>
  )
}
