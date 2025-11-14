import { useState, useEffect } from 'react';
import { devicesAPI } from '../services/api';
import '../styles/LightControl.css';

function LightControl({ device, onUpdate, onClose }) {
  const [brightness, setBrightness] = useState(device.brightness || 0);
  const [isOn, setIsOn] = useState(device.is_on || false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    setBrightness(device.brightness || 0);
    setIsOn(device.is_on || false);
  }, [device]);

  const handleBrightnessChange = async (newBrightness) => {
    setBrightness(newBrightness);

    // Debounce API calls
    if (handleBrightnessChange.timeout) {
      clearTimeout(handleBrightnessChange.timeout);
    }

    handleBrightnessChange.timeout = setTimeout(async () => {
      setLoading(true);
      setError('');

      try {
        await devicesAPI.setBrightness(device.device_id, parseInt(newBrightness));
        setIsOn(newBrightness > 0);
        onUpdate();
      } catch (err) {
        setError(err.detail || 'Failed to set brightness');
      } finally {
        setLoading(false);
      }
    }, 300);
  };

  const handleToggle = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await devicesAPI.toggleDevice(device.device_id);
      setIsOn(response.is_on);
      setBrightness(response.is_on ? 100 : 0);
      onUpdate();
    } catch (err) {
      setError(err.detail || 'Failed to toggle device');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="light-control">
      <div className="light-control-header">
        <h2>💡 {device.device_name}</h2>
        <button className="close-btn" onClick={onClose}>
          ×
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <div className="light-control-body">
        <div className="light-preview">
          <div
            className={`light-bulb ${isOn ? 'light-on' : 'light-off'}`}
            style={{
              opacity: isOn ? 0.3 + (brightness / 100) * 0.7 : 0.3,
            }}
          >
            <span className="bulb-icon">💡</span>
          </div>
          <p className="light-status">
            {isOn ? `On - ${brightness}%` : 'Off'}
          </p>
        </div>

        <div className="controls">
          <div className="toggle-control">
            <button
              className={`toggle-btn ${isOn ? 'btn-on' : 'btn-off'}`}
              onClick={handleToggle}
              disabled={loading}
            >
              {loading ? 'Updating...' : isOn ? 'Turn Off' : 'Turn On'}
            </button>
          </div>

          <div className="brightness-control">
            <label htmlFor="brightness-slider">
              <strong>Brightness</strong>
            </label>

            <div className="slider-container">
              <span className="slider-label">0%</span>
              <input
                id="brightness-slider"
                type="range"
                min="0"
                max="100"
                value={brightness}
                onChange={(e) => handleBrightnessChange(e.target.value)}
                className="brightness-slider"
                disabled={loading}
              />
              <span className="slider-label">100%</span>
            </div>

            <div className="brightness-value">
              {brightness}%
            </div>
          </div>

          <div className="quick-controls">
            <h4>Quick Settings</h4>
            <div className="quick-buttons">
              <button
                className="quick-btn"
                onClick={() => handleBrightnessChange(25)}
                disabled={loading}
              >
                25%
              </button>
              <button
                className="quick-btn"
                onClick={() => handleBrightnessChange(50)}
                disabled={loading}
              >
                50%
              </button>
              <button
                className="quick-btn"
                onClick={() => handleBrightnessChange(75)}
                disabled={loading}
              >
                75%
              </button>
              <button
                className="quick-btn"
                onClick={() => handleBrightnessChange(100)}
                disabled={loading}
              >
                100%
              </button>
            </div>
          </div>
        </div>

        <div className="device-info">
          <p><strong>Device ID:</strong> {device.device_id}</p>
          <p><strong>Type:</strong> {device.device_type}</p>
          <p><strong>Status:</strong> {device.status}</p>
        </div>
      </div>
    </div>
  );
}

export default LightControl;
