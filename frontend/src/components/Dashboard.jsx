import { useState, useEffect } from 'react';
import { devicesAPI, authAPI } from '../services/api';
import DeviceCard from './DeviceCard';
import LightControl from './LightControl';
import Scheduler from './Scheduler';
import '../styles/Dashboard.css';

function Dashboard({ userId, onLogout }) {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [showScheduler, setShowScheduler] = useState(false);
  const [showAddDevice, setShowAddDevice] = useState(false);
  const [newDeviceType, setNewDeviceType] = useState('light');
  const [newDeviceName, setNewDeviceName] = useState('');

  // Fetch devices
  const fetchDevices = async () => {
    try {
      const data = await devicesAPI.getDevices();
      setDevices(data);
      setError('');
    } catch (err) {
      setError(err.detail || 'Failed to fetch devices');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDevices();

    // Poll for updates every 5 seconds
    const interval = setInterval(fetchDevices, 5000);

    return () => clearInterval(interval);
  }, []);

  const handleLogout = async () => {
    try {
      await authAPI.logout();
      onLogout();
    } catch (err) {
      console.error('Logout error:', err);
      onLogout(); // Logout anyway
    }
  };

  const handleAddDevice = async (e) => {
    e.preventDefault();
    try {
      await devicesAPI.createDevice(newDeviceType, newDeviceName);
      setNewDeviceName('');
      setShowAddDevice(false);
      fetchDevices();
    } catch (err) {
      setError(err.detail || 'Failed to add device');
    }
  };

  const handleDeleteDevice = async (deviceId) => {
    if (window.confirm('Are you sure you want to delete this device?')) {
      try {
        await devicesAPI.deleteDevice(deviceId);
        fetchDevices();
      } catch (err) {
        setError(err.detail || 'Failed to delete device');
      }
    }
  };

  const handleDeviceClick = (device) => {
    if (device.device_type === 'light') {
      setSelectedDevice(device);
    }
  };

  const handleDeviceUpdate = () => {
    fetchDevices();
    setSelectedDevice(null);
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading">Loading devices...</div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Smart Home Dashboard</h1>
          <div className="header-actions">
            <button
              className="btn btn-secondary"
              onClick={() => setShowScheduler(!showScheduler)}
            >
              {showScheduler ? 'Hide Scheduler' : 'Show Scheduler'}
            </button>
            <button
              className="btn btn-secondary"
              onClick={() => setShowAddDevice(!showAddDevice)}
            >
              Add Device
            </button>
            <button className="btn btn-logout" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </div>
      </header>

      {error && (
        <div className="error-banner">
          {error}
          <button onClick={() => setError('')}>×</button>
        </div>
      )}

      {showAddDevice && (
        <div className="add-device-form">
          <h3>Add New Device</h3>
          <form onSubmit={handleAddDevice}>
            <div className="form-group">
              <label>Device Type:</label>
              <select
                value={newDeviceType}
                onChange={(e) => setNewDeviceType(e.target.value)}
              >
                <option value="light">Light</option>
                <option value="thermostat">Thermostat</option>
                <option value="security_camera">Security Camera</option>
              </select>
            </div>
            <div className="form-group">
              <label>Device Name:</label>
              <input
                type="text"
                value={newDeviceName}
                onChange={(e) => setNewDeviceName(e.target.value)}
                placeholder="Enter device name"
                required
              />
            </div>
            <div className="form-actions">
              <button type="submit" className="btn btn-primary">
                Add Device
              </button>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => setShowAddDevice(false)}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <main className="dashboard-main">
        {showScheduler ? (
          <Scheduler devices={devices} onTaskCreated={fetchDevices} />
        ) : selectedDevice ? (
          <LightControl
            device={selectedDevice}
            onUpdate={handleDeviceUpdate}
            onClose={() => setSelectedDevice(null)}
          />
        ) : (
          <div className="devices-grid">
            <h2>Your Devices ({devices.length})</h2>
            {devices.length === 0 ? (
              <div className="no-devices">
                <p>No devices found. Add a device to get started!</p>
              </div>
            ) : (
              <div className="devices-list">
                {devices.map((device) => (
                  <DeviceCard
                    key={device.device_id}
                    device={device}
                    onClick={() => handleDeviceClick(device)}
                    onDelete={() => handleDeleteDevice(device.device_id)}
                  />
                ))}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default Dashboard;
