import './../../styles/hb.css';
import React, { useState, useEffect } from 'react';

const Monitor = () => {
  const [containers, setContainers] = useState([]);

  useEffect(() => {
    const fetchContainers = async () => {
      try {
        const response = await fetch('/api/docker/containers');
        const data = await response.json();
        setContainers(data);
      } catch (error) {
        console.error('Error fetching containers:', error);
      }
    };

    fetchContainers();
    const interval = setInterval(fetchContainers, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <h1 className="hb-page-title">Docker Monitor</h1>
        <p className="hb-page-subtitle">Estado en tiempo real de contenedores</p>
      </div>
      <div className="hb-table-wrap">
        <table className="hb-table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Estado</th>
              <th>Uptime</th>
            </tr>
          </thead>
          <tbody>
            {containers.map((container, index) => (
              <tr key={index}>
                <td>{container.name}</td>
                <td>
                  <span className={`hb-badge ${container.state === 'running' ? 'hb-badge-green' : 'hb-badge-red'}`}>
                    {container.state === 'running' ? 'Running' : 'Stopped'}
                  </span>
                </td>
                <td>{container.uptime || 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Monitor;




