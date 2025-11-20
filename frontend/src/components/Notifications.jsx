import { useState, useEffect, useCallback } from 'react';
import { notificationsAPI } from '../services/api';
import '../styles/Notifications.css';

const EVENT_ICONS = {
  device_added: '➕',
  device_toggled: '🔄',
  brightness_changed: '💡',
  task_scheduled: '⏰',
  integration_created: '🔌',
  integration_toggled: '🔗',
  integration_activated: '✅',
  integration_deactivated: '❌',
  skill_added: '🎯',
};

const formatTimestamp = (timestamp) => new Date(timestamp).toLocaleString();

function Notifications({ isVisible }) {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchNotifications = useCallback(async () => {
    setLoading(true);
    try {
      const data = await notificationsAPI.getNotifications(20);
      setNotifications(data);
      setError('');
    } catch (err) {
      setError(err.detail || 'Failed to fetch notifications');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!isVisible) return;

    fetchNotifications();
    const interval = setInterval(fetchNotifications, 10000);
    return () => clearInterval(interval);

  }, [isVisible, fetchNotifications]);

  if (!isVisible) return null;

  return (
    <div className="notifications-panel">
      <div className="notifications-header">
        <h3>System Notifications</h3>
        <button
          className="refresh-btn"
          onClick={fetchNotifications}
          disabled={loading}
        >
          {loading ? '⟳' : '🔄'}
        </button>
      </div>

      {error && (
        <div className="notifications-error">
          {error}
        </div>
      )}

      <div className="notifications-list">
        {!loading && notifications.length === 0 ? (
          <div className="no-notifications">
            <p>No notifications yet</p>
          </div>
        ) : (
          notifications.map(({ event_type, message, timestamp }, idx) => (
            <div key={idx} className="notification-item">
              <div className="notification-icon">
                {EVENT_ICONS[event_type] || '📢'}
              </div>
              <div className="notification-content">
                <div className="notification-message">{message}</div>
                <div className="notification-meta">
                  <span className="notification-type">{event_type}</span>
                  <span className="notification-time">
                    {formatTimestamp(timestamp)}
                  </span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Notifications;
