import React from 'react';
import '../../styles/hb.css';

const PushSync = () => {
  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <h1 className="hb-page-title">Push & Sync</h1>
        <p className="hb-page-subtitle">Sincronización con GitHub completada</p>
      </div>

      <div className="hb-card">
        <div className="hb-card-header">
          <span className="hb-card-name">Commit: docs: contexto 2026-06-29 + DeepSeek IDE funcional</span>
          <span className="hb-badge-green">Push exitoso</span>
        </div>

        <div className="hb-table-wrap">
          <table className="hb-table">
            <thead>
              <tr>
                <th>Hash</th>
                <th>Archivos</th>
                <th>Branch</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>2d65af4</td>
                <td>Historial.jsx, Nuevo.jsx</td>
                <td>main</td>
                <td><span className="hb-badge-green">✓ Sincronizado</span></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="hb-form" style={{ marginTop: '1rem' }}>
          <div className="hb-form-grid">
            <input
              type="text"
              className="hb-input"
              placeholder="Mensaje del commit"
              value="docs: contexto 2026-06-29 + DeepSeek IDE funcional"
              readOnly
            />
            <button className="hb-btn hb-btn-sm" disabled>
              Push & Sync
            </button>
          </div>
        </div>
      </div>

      <div className="hb-card" style={{ marginTop: '1rem' }}>
        <div className="hb-card-header">
          <span className="hb-card-name">Logs Docker Desktop</span>
          <span className="hb-badge">docker-desktop://dashboard/logs</span>
        </div>
        <pre style={{ color: '#f0ede8', background: '#1a1a1a', padding: '1rem', borderRadius: '4px', fontSize: '0.85rem', overflow: 'auto' }}>
{`Enumerating objects: 13, done.
Counting objects: 100% (13/13), done.
Delta compression using up to 8 threads
Compressing objects: 100% (7/7), done.
Writing objects: 100% (9/9), 2.82 KiB | 577.00 KiB/s, done.
Total 9 (delta 4), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (4/4), completed with 4 local objects.
To https://github.com/ipanemausa/openclaw-operativo-2026.git
   d6735e9..2d65af4  main -> main`}
        </pre>
      </div>

      <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
        <span className="hb-badge-green">Commit en main</span>
        <span className="hb-badge">2d65af4</span>
        <span className="hb-badge">LF -> CRLF</span>
      </div>
    </div>
  );
};

export default PushSync;