import { useState, useEffect, useCallback, useMemo } from 'react';
import PropTypes from 'prop-types';
import { notificationsAPI } from '../services/api';
import '../styles/Notifications.css';

// C1: Extract constants to module scope for better maintainability
const POLL_INTERVAL = 10000; // 10 seconds
const DEFAULT_FETCH_LIMIT = 20;

// C2: Extract event icon mapping to a separate constant object
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
  default: '📢',
};

// C3: Extract utility functions outside component to prevent recreation on each render
const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleString();
};

const getEventIcon = (eventType) => EVENT_ICONS[eventType] || EVENT_ICONS.default;

function Notifications({ isVisible }) {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // C4: Memoize fetchNotifications with useCallback to prevent unnecessary re-creation
  const fetchNotifications = useCallback(async () => {
    try {
      setLoading(true);
      const data = await notificationsAPI.getNotifications(DEFAULT_FETCH_LIMIT);
      setNotifications(data);
      setError('');
    } catch (err) {
      // C5: Improved error handling with fallback message
      setError(err?.detail || err?.message || 'Failed to fetch notifications');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (isVisible) {
      fetchNotifications();

      // Poll for new notifications every 10 seconds
      const interval = setInterval(fetchNotifications, POLL_INTERVAL);

      return () => clearInterval(interval);
    }
  }, [isVisible, fetchNotifications]);

  // C6: Memoize empty state component to prevent unnecessary re-renders
  const emptyState = useMemo(
    () => (
      <div className="no-notifications">
        <p>No notifications yet</p>
      </div>
    ),
    []
  );

  // C7: Extract notification item rendering with better key management
  const renderNotificationItem = (notification, index) => (
    <div 
      key={notification.id || `notification-${index}`} 
      className="notification-item"
    >
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
  );

  //  C8: Early return for better readability
  if (!isVisible) return null;

  return (
    <div className="notifications-panel">
      <div className="notifications-header">
        <h3>System Notifications</h3>
        <button
          className="refresh-btn"
          onClick={fetchNotifications}
          disabled={loading}
          aria-label="Refresh notifications" //C9: Add aria-label for accessibility
        >
          {loading ? '⟳' : '🔄'}
        </button>
      </div>

      {error && (
        <div className="notifications-error" role="alert"> {/* C9: Add role="alert" for accessibility */}
          {error}
        </div>
      )}

      <div className="notifications-list">
        {notifications.length === 0 && !loading
          ? emptyState
          : notifications.map(renderNotificationItem)}
      </div>
    </div>
  );
}

// C10: Add PropTypes for type checking and documentation
Notifications.propTypes = {
  isVisible: PropTypes.bool.isRequired,
};

export default Notifications;
