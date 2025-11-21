import { useState, useEffect } from 'react';
import { schedulerAPI } from '../services/api';
import '../styles/Scheduler.css';

const TASK_ACTIONS = [
  { value: 'turn_on', label: 'Turn On' },
  { value: 'turn_off', label: 'Turn Off' },
  { value: 'set_brightness', label: 'Set Brightness' }
];

function Scheduler({ devices, onTaskCreated }) {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showAddTask, setShowAddTask] = useState(false);

  // Form state
  const [selectedDevice, setSelectedDevice] = useState('');
  const [selectedAction, setSelectedAction] = useState('turn_on');
  const [scheduledDate, setScheduledDate] = useState('');
  const [scheduledTime, setScheduledTime] = useState('');

  const fetchTasks = async () => {
    try {
      const data = await schedulerAPI.getTasks();
      setTasks(data);
      setError('');
    } catch (err) {
      setError(err.detail || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();

    // Poll for updates every 10 seconds
    const interval = setInterval(fetchTasks, 10000);

    return () => clearInterval(interval);
  }, []);

  const combineDateTimeToISO = (date, time) => {
    return new Date(`${date}T${time}`).toISOString();
  };

  const resetTaskForm = () => {
    setSelectedDevice('');
    setSelectedAction('turn_on');
    setScheduledDate('');
    setScheduledTime('');
    setShowAddTask(false);
  };

  const handleAddTask = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const scheduledDateTime = combineDateTimeToISO(scheduledDate, scheduledTime);
      await schedulerAPI.createTask(selectedDevice, selectedAction, scheduledDateTime);

      resetTaskForm();
      fetchTasks();
      onTaskCreated();
    } catch (err) {
      setError(err.detail || 'Failed to create task');
    }
  };

  const handleCancelTask = async (taskId) => {
    if (window.confirm('Are you sure you want to cancel this task?')) {
      try {
        await schedulerAPI.cancelTask(taskId);
        fetchTasks();
      } catch (err) {
        setError(err.detail || 'Failed to cancel task');
      }
    }
  };

  const formatDateTime = (isoString) => {
    try {
      const date = new Date(isoString);
      return date.toLocaleString();
    } catch {
      return isoString;
    }
  };

  const getDeviceName = (targetDeviceId) => {
    const device = devices.find((device) => device.device_id === targetDeviceId);
    return device ? device.device_name : targetDeviceId;
  };

  const getActionLabel = (actionValue) => {
    const action = TASK_ACTIONS.find((a) => a.value === actionValue);
    return action ? action.label : actionValue;
  };

  if (loading) {
    return (
      <div className="scheduler">
        <div className="loading">Loading scheduled tasks...</div>
      </div>
    );
  }

  return (
    <div className="scheduler">
      <div className="scheduler-header">
        <h2>⏰ Task Scheduler</h2>
        <button
          className="btn btn-primary"
          onClick={() => setShowAddTask(!showAddTask)}
        >
          {showAddTask ? 'Cancel' : 'Schedule New Task'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
          <button onClick={() => setError('')}>×</button>
        </div>
      )}

      {showAddTask && (
        <div className="add-task-form">
          <h3>Schedule New Task</h3>
          <form onSubmit={handleAddTask}>
            <div className="form-group">
              <label>Device:</label>
              <select
                value={selectedDevice}
                onChange={(e) => setSelectedDevice(e.target.value)}
                required
              >
                <option value="">Select a device</option>
                {devices.map((device) => (
                  <option key={device.device_id} value={device.device_id}>
                    {device.device_name} ({device.device_type})
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Action:</label>
              <select
                value={selectedAction}
                onChange={(e) => setSelectedAction(e.target.value)}
                required
              >
                {TASK_ACTIONS.map((action) => (
                  <option key={action.value} value={action.value}>
                    {action.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Date:</label>
                <input
                  type="date"
                  value={scheduledDate}
                  onChange={(e) => setScheduledDate(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label>Time:</label>
                <input
                  type="time"
                  value={scheduledTime}
                  onChange={(e) => setScheduledTime(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-actions">
              <button type="submit" className="btn btn-primary">
                Schedule Task
              </button>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => setShowAddTask(false)}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="tasks-list">
        <h3>Scheduled Tasks ({tasks.length})</h3>

        {tasks.length === 0 ? (
          <div className="no-tasks">
            <p>No scheduled tasks. Create one to get started!</p>
          </div>
        ) : (
          <div className="tasks-grid">
            {tasks.map((task) => (
              <div
                key={task.task_id}
                className={`task-card ${task.executed ? 'task-executed' : 'task-pending'}`}
              >
                <div className="task-header">
                  <span className="task-icon">
                    {task.executed ? '✅' : '⏱️'}
                  </span>
                  <button
                    className="delete-btn"
                    onClick={() => handleCancelTask(task.task_id)}
                    title="Cancel task"
                  >
                    ×
                  </button>
                </div>

                <div className="task-body">
                  <h4>{getDeviceName(task.device_id)}</h4>
                  <p className="task-action">{getActionLabel(task.action)}</p>
                  <p className="task-time">
                    {formatDateTime(task.scheduled_time)}
                  </p>

                  <div className="task-status">
                    <span className={`status-badge ${task.executed ? 'executed' : 'pending'}`}>
                      {task.executed ? 'Executed' : 'Pending'}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Scheduler;
