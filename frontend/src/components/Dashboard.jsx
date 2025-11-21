import { useState, useEffect } from "react";
import { devicesAPI, authAPI } from "../services/api";
import DeviceCard from "./DeviceCard";
import LightControl from "./LightControl";
import Scheduler from "./Scheduler";
import Notifications from "./Notifications";
import Integrations from "./Integrations";
import "../styles/Dashboard.css";
import AddDeviceForm from "./AddDeviceForm";
import usePollingFetch from "../../hooks/usePollingFetch";

function Dashboard({ onLogout }) {
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [showScheduler, setShowScheduler] = useState(false);
  const [showAddDevice, setShowAddDevice] = useState(false);
  const [newDevice, setNewDevice] = useState({ type: "light", name: "" });
  const [showNotifications, setShowNotifications] = useState(false);
  const [showIntegrations, setShowIntegrations] = useState(false);

  const DEVICE_POLL_INTERVAL_MS = 5000;
  // Fetch devices
  const {
    data: devices,
    loading,
    error,
    setError,
    refetch: fetchDevices,
  } = usePollingFetch(devicesAPI.getDevices, DEVICE_POLL_INTERVAL_MS);

  useEffect(() => {
    fetchDevices();

    const interval = setInterval(fetchDevices, DEVICE_POLL_INTERVAL_MS);

    return () => clearInterval(interval);
  }, []);

  const handleLogout = async () => {
    try {
      await authAPI.logout();
      onLogout();
    } catch (err) {
      console.error("Logout error:", err);
      onLogout(); // Logout anyway
    }
  };

  const handleAddDevice = async (e) => {
    e.preventDefault();
    try {
      await devicesAPI.createDevice(newDevice.type, newDevice.name);
      setNewDevice({ type: "light", name: "" });
      setShowAddDevice(false);
      fetchDevices();
    } catch (err) {
      setError(getErrorMessage(err, "add device"));
    }
  };

  const handleDeleteDevice = async (deviceId) => {
    if (window.confirm("Are you sure you want to delete this device?")) {
      try {
        await devicesAPI.deleteDevice(deviceId);
        fetchDevices();
      } catch (err) {
        setError(getErrorMessage(err, "delete device"));
      }
    }
  };

  const isDeviceInteractive = (device) => {
    return device.device_type === "light";
  };

  const handleDeviceClick = (device) => {
    if (isDeviceInteractive(device)) {
      setSelectedDevice(device);
    }
  };

  const handleDeviceUpdate = () => {
    fetchDevices();
    setSelectedDevice(null);
  };

  const getErrorMessage = (err, action) => err.detail || `Failed to ${action}`;

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
              onClick={() => {
                setShowIntegrations(!showIntegrations);
                setShowNotifications(false);
                setShowScheduler(false);
                setSelectedDevice(null);
              }}
            >
              Integrations
            </button>
            <button
              className="btn btn-secondary"
              onClick={() => {
                setShowNotifications(!showNotifications);
                setShowIntegrations(false);
                setShowScheduler(false);
                setSelectedDevice(null);
              }}
            >
              {showNotifications ? "Hide Notifications" : "Show Notifications"}
            </button>
            <button
              className="btn btn-secondary"
              onClick={() => {
                setShowScheduler(!showScheduler);
                setShowIntegrations(false);
                setShowNotifications(false);
                setSelectedDevice(null);
              }}
            >
              {showScheduler ? "Hide Scheduler" : "Show Scheduler"}
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
          <button onClick={() => setError("")}>×</button>
        </div>
      )}

      {showAddDevice && (
        <AddDeviceForm
          handleAddDevice={handleAddDevice}
          setShowAddDevice={setShowAddDevice}
          newDevice={newDevice}
          setNewDevice={setNewDevice}
        />
      )}

      <main className="dashboard-main">
        {showIntegrations ? (
          <Integrations />
        ) : showNotifications ? (
          <Notifications isVisible={showNotifications} />
        ) : showScheduler ? (
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
