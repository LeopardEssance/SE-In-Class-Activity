from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid


class ScheduledTask:
    """Represents a scheduled task for a device."""

    def __init__(self, task_id: str, device_id: str, action: str, scheduled_time: str):
        """
        Initialize a scheduled task.

        Args:
            task_id: Unique identifier for the task
            device_id: ID of the device to control
            action: Action to perform (e.g., 'turn_on', 'turn_off', 'set_brightness')
            scheduled_time: ISO format time string when task should execute
        """
        self.task_id = task_id
        self.device_id = device_id
        self.action = action
        self.scheduled_time = scheduled_time
        self.executed = False
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert task to dictionary representation.

        Returns:
            Dict containing task data
        """
        return {
            "task_id": self.task_id,
            "device_id": self.device_id,
            "action": self.action,
            "scheduled_time": self.scheduled_time,
            "executed": self.executed,
            "created_at": self.created_at
        }


class Scheduler:
    """Manages scheduled tasks for devices."""

    def __init__(self):
        """Initialize the scheduler with an empty task list."""
        self.tasks: List[ScheduledTask] = []

    def schedule_task(self, task: ScheduledTask) -> bool:
        """
        Schedule a new task.

        Args:
            task: ScheduledTask instance to schedule

        Returns:
            bool: True if scheduled successfully
        """
        self.tasks.append(task)
        return True

    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a scheduled task.

        Args:
            task_id: ID of the task to cancel

        Returns:
            bool: True if cancelled successfully, False if not found
        """
        initial_length = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.task_id != task_id]
        return len(self.tasks) < initial_length

    def _parse_task_time(self, scheduled_time: str) -> Optional[datetime]:
        """
        Parse a scheduled time string to a datetime object.

        Args:
            scheduled_time: ISO format time string

        Returns:
            Parsed datetime object if valid, None otherwise
        """
        try:
            return datetime.fromisoformat(scheduled_time)
        except ValueError:
            # Invalid time format
            return None

    def execute_tasks(self) -> List[ScheduledTask]:
        """
        Execute tasks that are due (simplified - just returns tasks).
        In production, this would check scheduled_time and execute actions.

        Returns:
            List of tasks that should be executed
        """
        current_time = datetime.now()
        due_tasks = []

        for task in self.tasks:
            if not task.executed:
                task_time = self._parse_task_time(task.scheduled_time)
                if task_time and task_time <= current_time:
                    task.executed = True
                    due_tasks.append(task)

        return due_tasks

    def get_scheduled_tasks(self) -> List[Dict[str, Any]]:
        """
        Get all scheduled tasks.

        Returns:
            List of task dictionaries
        """
        return [task.to_dict() for task in self.tasks]

    def get_task(self, task_id: str) -> Optional[ScheduledTask]:
        """
        Get a specific task by ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            ScheduledTask if found, None otherwise
        """
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None