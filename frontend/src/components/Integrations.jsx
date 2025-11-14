import { useState, useEffect } from 'react';
import { integrationsAPI } from '../services/api';
import '../styles/Integrations.css';

function Integrations() {
  const [integrations, setIntegrations] = useState([]);
  const [stats, setStats] = useState({ connected_count: 0, total_count: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [newIntegration, setNewIntegration] = useState({
    name: '',
    description: '',
    features: '',
    commands: ''
  });

  const fetchIntegrations = async () => {
    try {
      setLoading(true);
      const [integrationsData, statsData] = await Promise.all([
        integrationsAPI.getIntegrations(),
        integrationsAPI.getStats()
      ]);
      setIntegrations(integrationsData);
      setStats(statsData);
      setError('');
    } catch (err) {
      setError(err.detail || 'Failed to fetch integrations');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchIntegrations();
  }, []);

  const handleCreateIntegration = async (e) => {
    e.preventDefault();
    try {
      const features = newIntegration.features
        ? newIntegration.features.split(',').map(f => f.trim()).filter(f => f)
        : [];
      const commands = newIntegration.commands
        ? newIntegration.commands.split(',').map(c => c.trim()).filter(c => c)
        : [];

      await integrationsAPI.createIntegration({
        name: newIntegration.name,
        description: newIntegration.description,
        features: features.length > 0 ? features : undefined,
        commands: commands.length > 0 ? commands : undefined
      });

      setNewIntegration({ name: '', description: '', features: '', commands: '' });
      setShowAddForm(false);
      fetchIntegrations();
    } catch (err) {
      setError(err.detail || 'Failed to create integration');
    }
  };

  const handleToggle = async (name) => {
    try {
      await integrationsAPI.toggleIntegration(name);
      fetchIntegrations();
    } catch (err) {
      setError(err.detail || 'Failed to toggle integration');
    }
  };

  const handleActivate = async (name) => {
    try {
      await integrationsAPI.activateIntegration(name);
      fetchIntegrations();
    } catch (err) {
      setError(err.detail || 'Failed to activate integration');
    }
  };

  const handleDeactivate = async (name) => {
    try {
      await integrationsAPI.deactivateIntegration(name);
      fetchIntegrations();
    } catch (err) {
      setError(err.detail || 'Failed to deactivate integration');
    }
  };

  const getStatusBadge = (status) => {
    const statusColors = {
      active: 'status-active',
      inactive: 'status-inactive',
      error: 'status-error'
    };
    return <span className={`status-badge ${statusColors[status] || 'status-inactive'}`}>{status}</span>;
  };

  if (loading) {
    return (
      <div className="integrations-container">
        <div className="loading">Loading integrations...</div>
      </div>
    );
  }

  return (
    <div className="integrations-container">
      <div className="integrations-header">
        <div>
          <h2>Integrations</h2>
          <p className="stats">
            {stats.connected_count} of {stats.total_count} connected
          </p>
        </div>
        <button
          className="btn btn-primary"
          onClick={() => setShowAddForm(!showAddForm)}
        >
          {showAddForm ? 'Cancel' : '+ Add Integration'}
        </button>
      </div>

      {error && (
        <div className="error-banner">
          {error}
          <button onClick={() => setError('')}>×</button>
        </div>
      )}

      {showAddForm && (
        <div className="add-integration-form">
          <h3>Create New Integration</h3>
          <form onSubmit={handleCreateIntegration}>
            <div className="form-group">
              <label>Name *</label>
              <input
                type="text"
                value={newIntegration.name}
                onChange={(e) => setNewIntegration({ ...newIntegration, name: e.target.value })}
                placeholder="e.g., Alexa, Google Home"
                required
              />
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea
                value={newIntegration.description}
                onChange={(e) => setNewIntegration({ ...newIntegration, description: e.target.value })}
                placeholder="Integration description"
                rows="3"
              />
            </div>
            <div className="form-group">
              <label>Features (comma-separated)</label>
              <input
                type="text"
                value={newIntegration.features}
                onChange={(e) => setNewIntegration({ ...newIntegration, features: e.target.value })}
                placeholder="e.g., voice control, automation"
              />
            </div>
            <div className="form-group">
              <label>Commands (comma-separated)</label>
              <input
                type="text"
                value={newIntegration.commands}
                onChange={(e) => setNewIntegration({ ...newIntegration, commands: e.target.value })}
                placeholder="e.g., turn on, turn off, set brightness"
              />
            </div>
            <div className="form-actions">
              <button type="submit" className="btn btn-primary">
                Create Integration
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="integrations-grid">
        {integrations.length === 0 ? (
          <div className="no-integrations">
            <p>No integrations found. Create one to get started!</p>
          </div>
        ) : (
          integrations.map((integration) => (
            <div key={integration.name} className="integration-card">
              <div className="integration-header">
                <h3>{integration.name}</h3>
                {getStatusBadge(integration.status)}
              </div>
              <p className="integration-description">{integration.description || 'No description'}</p>
              
              <div className="integration-details">
                <div className="detail-section">
                  <strong>Features:</strong>
                  {integration.features.length > 0 ? (
                    <ul>
                      {integration.features.map((feature, idx) => (
                        <li key={idx}>{feature}</li>
                      ))}
                    </ul>
                  ) : (
                    <span className="empty">None</span>
                  )}
                </div>
                
                <div className="detail-section">
                  <strong>Commands:</strong>
                  {integration.commands.length > 0 ? (
                    <ul>
                      {integration.commands.map((command, idx) => (
                        <li key={idx}>{command}</li>
                      ))}
                    </ul>
                  ) : (
                    <span className="empty">None</span>
                  )}
                </div>

                {integration.skills.length > 0 && (
                  <div className="detail-section">
                    <strong>Skills:</strong>
                    <ul>
                      {integration.skills.map((skill, idx) => (
                        <li key={idx}>{skill}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              <div className="integration-actions">
                <button
                  className={`btn btn-sm ${integration.connected ? 'btn-warning' : 'btn-success'}`}
                  onClick={() => handleToggle(integration.name)}
                >
                  {integration.connected ? 'Disconnect' : 'Connect'}
                </button>
                {integration.status === 'inactive' ? (
                  <button
                    className="btn btn-sm btn-primary"
                    onClick={() => handleActivate(integration.name)}
                  >
                    Activate
                  </button>
                ) : (
                  <button
                    className="btn btn-sm btn-secondary"
                    onClick={() => handleDeactivate(integration.name)}
                  >
                    Deactivate
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Integrations;

