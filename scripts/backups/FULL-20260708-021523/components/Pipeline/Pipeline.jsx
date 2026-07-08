import "../../styles/hb.css";

const Pipeline = () => {
  const steps = [
    { id: 1, name: 'Build', status: 'completed' },
    { id: 2, name: 'Test', status: 'pending' },
    { id: 3, name: 'Deploy', status: 'failed' },
    { id: 4, name: 'Verify', status: 'pending' },
  ];

  const getBadgeClass = (status) => {
    switch (status) {
      case 'completed':
        return 'hb-badge hb-badge-green';
      case 'pending':
        return 'hb-badge';
      case 'failed':
        return 'hb-badge hb-badge-red';
      default:
        return 'hb-badge';
    }
  };

  const getBadgeText = (status) => {
    switch (status) {
      case 'completed':
        return 'Completed';
      case 'pending':
        return 'Pending';
      case 'failed':
        return 'Failed';
      default:
        return status;
    }
  };

  return (
    <div className="hb-page">
      <div className="hb-page-header">
        <h1 className="hb-page-title">Pipeline CI/CD</h1>
        <p className="hb-page-subtitle">Continuous Integration / Continuous Deployment Pipeline</p>
      </div>

      <div className="hb-card" style={{ margin: '2rem 0', padding: '2rem' }}>
        <div className="hb-card-header">
          <h3 className="hb-card-name">Deployment Pipeline</h3>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-around', margin: '2rem 0', alignItems: 'center' }}>
          {steps.map((step, index) => (
            <div key={step.id} style={{ textAlign: 'center', flex: 1, position: 'relative' }}>
              <div
                style={{
                  width: '60px',
                  height: '60px',
                  borderRadius: '50%',
                  backgroundColor: step.status === 'completed' ? '#4caf50' : step.status === 'failed' ? '#f44336' : '#d4af6a',
                  color: '#1a1a1a',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 0.5rem auto',
                  fontWeight: 'bold',
                  fontSize: '1.2rem',
                }}
              >
                {step.id}
              </div>
              <div style={{ fontWeight: 'bold', color: '#f0ede8', marginBottom: '0.3rem' }}>{step.name}</div>
              <span className={getBadgeClass(step.status)}>{getBadgeText(step.status)}</span>
              {index < steps.length - 1 && (
                <div
                  style={{
                    position: 'absolute',
                    top: '30px',
                    right: '-50%',
                    width: '100%',
                    height: '2px',
                    backgroundColor: '#d4af6a',
                    zIndex: -1,
                  }}
                />
              )}
            </div>
          ))}
        </div>
      </div>

      <div style={{ textAlign: 'center', marginTop: '2rem' }}>
        <button className="hb-btn" style={{ padding: '12px 30px', fontSize: '1.1rem' }}>
          Ejecutar Nuevo Deploy
        </button>
      </div>
    </div>
  );
};

export default Pipeline;





