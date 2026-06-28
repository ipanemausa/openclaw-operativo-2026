import React from 'react';
import '../../styles/hb.css';

const Workspace = () => {
  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <h1 className="hb-page-title">Workspace</h1>
        <p className="hb-page-subtitle">Manage your projects and tasks</p>
      </div>

      <div className="hb-form">
        <div className="hb-form-grid">
          <input type="text" className="hb-input" placeholder="Search workspace..." />
          <select className="hb-select">
            <option>All Projects</option>
            <option>Active</option>
            <option>Completed</option>
          </select>
          <button className="hb-btn">New Project</button>
        </div>
      </div>

      <div className="hb-table-wrap">
        <table className="hb-table">
          <thead>
            <tr>
              <th>Project Name</th>
              <th>Status</th>
              <th>Deadline</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <div className="hb-card">
                  <div className="hb-card-header">
                    <span className="hb-card-name">Earrings Collection</span>
                    <span className="hb-card-price">$12,000</span>
                  </div>
                  <div className="hb-card-meta">Design Phase - 65%</div>
                </div>
              </td>
              <td><span className="hb-badge hb-badge-green">Active</span></td>
              <td>2024-03-15</td>
              <td><button className="hb-btn hb-btn-sm">View</button></td>
            </tr>
            <tr>
              <td>
                <div className="hb-card">
                  <div className="hb-card-header">
                    <span className="hb-card-name">Necklace Prototype</span>
                    <span className="hb-card-price">$8,500</span>
                  </div>
                  <div className="hb-card-meta">Production - 90%</div>
                </div>
              </td>
              <td><span className="hb-badge hb-badge-green">Active</span></td>
              <td>2024-02-28</td>
              <td><button className="hb-btn hb-btn-sm">View</button></td>
            </tr>
            <tr>
              <td>
                <div className="hb-card">
                  <div className="hb-card-header">
                    <span className="hb-card-name">Bracelet Line</span>
                    <span className="hb-card-price">$6,200</span>
                  </div>
                  <div className="hb-card-meta">Completed - 100%</div>
                </div>
              </td>
              <td><span className="hb-badge hb-badge-red">Completed</span></td>
              <td>2024-01-10</td>
              <td><button className="hb-btn hb-btn-sm">View</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Workspace;