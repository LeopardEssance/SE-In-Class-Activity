import { useState, useEffect } from 'react';
import { devicesAPI } from '../services/api';
import '../styles/LightControl.css';
import { useDebounce } from '../hooks/useDebounce';
import QuickBrightnessControls from './QuickBrightnessControls';

const DEBOUNCE_DELAY_MS = 300;
const MIN_BRIGHTNESS = 0;
const MAX_BRIGHTNESS = 100;
const OPACITY_MIN = 0.3;
const OPACITY_RANGE = 0.7;
const BRIGHTNESS_PRESETS = [25, 50, 75, 100];

function LightControl({ device, onUpdate, onClose }) {
  const [brightness, setBrightness] = useState(device.brightness || MIN_BRIGHTNESS);
  const [isOn, setIsOn] = useState(device.is_on || false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    setBrightness(device.brightness || MIN_BRIGHTNESS);
    setIsOn(device.is_on || false);
  }, [device]);

  // Helper function to wrap API calls with loading and error handling
  const withLoadingAndError = async (apiCall, errorMessage) => {
    setLoading(true);
    setError('');

    try {
      await apiCall();
    } catch (err) {
      setError(err.detail || errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const debouncedAPICall = useDebounce(async (newBrightness) => {
    await withLoadingAndError(async () => {
      await devicesAPI.setBrightness(device.device_id, parseInt(newBrightness));
      setIsOn(newBrightness > 0);
      onUpdate();
    }, 'Failed to set brightness');
  }, DEBOUNCE_DELAY_MS);

  const handleBrightnessChange = (newBrightness) => {
    setBrightness(newBrightness);
    debouncedAPICall(newBrightness);
  };

  const handleToggle = async () => {
    await withLoadingAndError(async () => {
      const response = await devicesAPI.toggleDevice(device.device_id);
      setIsOn(response.is_on);
      setBrightness(response.is_on ? MAX_BRIGHTNESS : MIN_BRIGHTNESS);
      onUpdate();
    }, 'Failed to toggle device');
  };

  // Helper function to calculate bulb opacity
  const calculateBulbOpacity = (isOn, brightness) => {
    const baseOpacity = OPACITY_MIN;
    if (!isOn) return baseOpacity;

    const brightnessRatio = brightness / MAX_BRIGHTNESS;
    const additionalOpacity = brightnessRatio * OPACITY_RANGE;
    return baseOpacity + additionalOpacity;
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
              opacity: calculateBulbOpacity(isOn, brightness),
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
              <span className="slider-label">{MIN_BRIGHTNESS}%</span>
              <input
                id="brightness-slider"
                type="range"
                min={MIN_BRIGHTNESS}
                max={MAX_BRIGHTNESS}
                value={brightness}
                onChange={(e) => handleBrightnessChange(e.target.value)}
                className="brightness-slider"
                disabled={loading}
              />
              <span className="slider-label">{MAX_BRIGHTNESS}%</span>
            </div>

            <div className="brightness-value">
              {brightness}%
            </div>
          </div>

          <QuickBrightnessControls
            onBrightnessChange={handleBrightnessChange}
            disabled={loading}
            presets={BRIGHTNESS_PRESETS}
          />
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
