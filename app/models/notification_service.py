from typing import List, Protocol, Dict, Any
from queue import Queue
from datetime import datetime
from abc import ABC, abstractmethod


class Observer(ABC):
    """Observer interface for receiving notifications."""

    @abstractmethod
    def update(self, event: 'Event') -> None:
        """
        Receive update notification.

        Args:
            event: Event that occurred
        """
        pass


class Event:
    """Represents an event in the system."""

    def __init__(self, event_type: str, device_id: str, message: str, data: Dict[str, Any] = None):
        """
        Initialize an event.

        Args:
            event_type: Type of event (e.g., 'device_status_change', 'task_scheduled')
            device_id: ID of the device associated with the event
            message: Human-readable message describing the event
            data: Additional event data
        """
        self.event_type = event_type
        self.device_id = device_id
        self.message = message
        self.data = data or {}
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert event to dictionary.

        Returns:
            Dict containing event data
        """
        return {
            "event_type": self.event_type,
            "device_id": self.device_id,
            "message": self.message,
            "data": self.data,
            "timestamp": self.timestamp
        }


class NotificationService:
    """Service for managing notifications using Observer pattern."""

    def __init__(self):
        """Initialize the notification service."""
        self.subscribers: List[Observer] = []
        self.notifications: Queue = Queue()
        self.notification_history: List[Event] = []  # Store all notifications

    def subscribe(self, observer: Observer) -> None:
        """
        Subscribe an observer to receive notifications.

        Args:
            observer: Observer instance to subscribe
        """
        if observer not in self.subscribers:
            self.subscribers.append(observer)

    def unsubscribe(self, observer: Observer) -> bool:
        """
        Unsubscribe an observer.

        Args:
            observer: Observer instance to unsubscribe

        Returns:
            bool: True if unsubscribed, False if not found
        """
        if observer in self.subscribers:
            self.subscribers.remove(observer)
            return True
        return False

    def _create_event(self, event_type: str, device_id: str, message: str, data: Dict[str, Any] = None) -> Event:
        """
        Create an Event object with the specified parameters.

        Args:
            event_type: Type of event (e.g., 'device_status_change', 'task_scheduled')
            device_id: ID of the device associated with the event
            message: Human-readable message describing the event
            data: Additional event data

        Returns:
            Event instance
        """
        return Event(event_type, device_id, message, data)

    def notify(self, event: Event) -> None:
        """
        Notify all subscribers about an event.

        Args:
            event: Event to notify subscribers about
        """
        self.notifications.put(event)
        self.notification_history.append(event)  # Keep in history
        for subscriber in self.subscribers:
            subscriber.update(event)

    def send_notification(self, message: str, device_id: str = "", event_type: str = "general") -> None:
        """
        Send a notification message.

        Args:
            message: Notification message
            device_id: Optional device ID associated with notification
            event_type: Type of event
        """
        event = self._create_event(event_type, device_id, message)
        self.notifications.put(event)
        self.notification_history.append(event)  # Keep in history

    def get_notifications(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent notifications.

        Args:
            limit: Maximum number of notifications to return

        Returns:
            List of notification dictionaries (most recent first)
        """
        # Return the most recent notifications from history
        recent_notifications = self.notification_history[-limit:] if len(self.notification_history) > limit else self.notification_history
        # Reverse to show newest first
        recent_notifications = list(reversed(recent_notifications))
        
        return [notification.to_dict() for notification in recent_notifications if isinstance(notification, Event)]

