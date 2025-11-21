import "../styles/Dashboard.css";

const AddDeviceForm = ({
  handleAddDevice,
  setShowAddDevice,
  newDevice,
  setNewDevice,
}) => (
  <div className="add-device-form">
    <h3>Add New Device</h3>
    <form onSubmit={handleAddDevice}>
      <div className="form-group">
        <label>Device Type:</label>
        <select
          value={newDevice.type}
          onChange={(e) => setNewDevice({ ...newDevice, type: e.target.value })}
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
          value={newDevice.name}
          onChange={(e) => setNewDevice({ ...newDevice, name: e.target.value })}
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
);

export default AddDeviceForm;
