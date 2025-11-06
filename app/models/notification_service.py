from typing import List
from queue import Queue


class Observer:
    pass


class Event:
    pass


class NotificationService:
    subscribers: List[Observer]
    notifications: Queue

    def __init__(self):
        self.subscribers = []
        self.notifications = Queue()

    def subscribe(self, observer: Observer) -> None:
        """Subscribe an observer to receive notifications."""
        self.subscribers.append(observer)

    def notify(self, event: Event) -> None:
        """Notify all subscribers about an event."""
        for subscriber in self.subscribers:
            self.notifications.put(event)

    def sendNotification(self, message: str) -> None:
        """Send a notification message."""
        self.notifications.put(message)

