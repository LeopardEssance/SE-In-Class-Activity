import { useState, useEffect } from 'react';
import { notificationsAPI } from '../services/api';
import '../styles/Notifications.css';

function Notifications({ isVisible }) {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchNotifications = async () => {
    try {
      setLoading(true);
      const data = await notificationsAPI.getNotifications(20);
      setNotifications(data);
      setError('');
    } catch (err) {
      setError(err.detail || 'Failed to fetch notifications');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isVisible) {
      fetchNotifications();

      // Poll for new notifications every 10 seconds
      const interval = setInterval(fetchNotifications, 10000);

      return () => clearInterval(interval);
    }
  }, [isVisible]);

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  const getEventIcon = (eventType) => {
    switch (eventType) {
      case 'device_added':
        return '➕';
      case 'device_toggled':
        return '🔄';
      case 'brightness_changed':
        return '💡';
      case 'task_scheduled':
        return '⏰';
      case 'integration_created':
        return '🔌';
      case 'integration_toggled':
        return '🔗';
      case 'integration_activated':
        return '✅';
      case 'integration_deactivated':
        return '❌';
      case 'skill_added':
        return '🎯';
      default:
        return '📢';
    }
  };

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
        {notifications.length === 0 && !loading ? (
          <div className="no-notifications">
            <p>No notifications yet</p>
          </div>
        ) : (
          notifications.map((notification, index) => (
            <div key={index} className="notification-item">
              <div className="notification-icon">
                {getEventIcon(notification.event_type)}
              </div>
              <div className="notification-content">
                <div className="notification-message">
                  {notification.message}
                </div>
                <div className="notification-meta">
                  <span className="notification-type">{notification.event_type}</span>
                  <span className="notification-time">
                    {formatTimestamp(notification.timestamp)}
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
