const DeviceDetails = ({ device }) => {
  if (device.device_type === "light" && device.brightness !== undefined) {
    return (
      <div className="device-details">
        <p>Brightness: {device.brightness}%</p>
      </div>
    );
  }

  if (device.device_type === "thermostat") {
    return (
      <div className="device-details">
        <p>Temperature: {device.temperature}°C</p>
        <p>Target: {device.target_temperature}°C</p>
      </div>
    );
  }

  return null;
};

export default DeviceDetails;
