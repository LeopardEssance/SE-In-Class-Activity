import "../styles/DeviceCard.css";
import DeviceDetails from "./DeviceDetails";

function DeviceCard({ device, onClick, onDelete }) {
  const getDeviceIcon = (type) => {
    const icons = {
      light: "💡",
      thermostat: "🌡️",
      security_camera: "📷",
    };
    return icons[type] || "🔌";
  };

  const getStatusColor = (status) => {
    const colors = {
      on: "#4CAF50",
      off: "#757575",
    };
    return colors[status] || colors.off;
  };

  return (
    <div className="device-card" onClick={onClick}>
      <div className="device-card-header">
        <span className="device-icon">{getDeviceIcon(device.device_type)}</span>
        <button
          className="delete-btn"
          onClick={(e) => {
            e.stopPropagation();
            onDelete();
          }}
          title="Delete device"
        >
          ×
        </button>
      </div>

      <div className="device-card-body">
        <h3>{device.device_name}</h3>
        <p className="device-type">{device.device_type}</p>

        <div className="device-status">
          <span
            className="status-indicator"
            style={{ backgroundColor: getStatusColor(device.status) }}
          ></span>
          <span className="status-text">
            {device.status === "on" ? "On" : "Off"}
          </span>
        </div>

        <DeviceDetails device={device} />

        {device.device_type === "thermostat" && (
          <div className="device-details">
            <p>Temperature: {device.temperature}°C</p>
            <p>Target: {device.target_temperature}°C</p>
          </div>
        )}
      </div>

      {device.device_type === "light" && (
        <div className="device-card-footer">
          <span className="click-hint">Click to control</span>
        </div>
      )}
    </div>
  );
}

export default DeviceCard;
